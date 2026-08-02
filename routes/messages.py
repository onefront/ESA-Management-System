import os
from werkzeug.utils import secure_filename
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    current_app,
    jsonify,
    abort
)

from flask_login import login_required, current_user
from flask import flash, redirect, url_for
from models.user import User

messages_bp = Blueprint(
    "messages",
    __name__,
    url_prefix="/messages"
)

from extensions import db
from models.chat_block import ChatBlock
from models.user import User
from models.conversation import Conversation
from models.conversation_member import ConversationMember
from models.message import Message
from models.message_read import MessageRead
from models.attachment import Attachment




@messages_bp.route("/")
@login_required
def inbox():

    from models.chat_setting import ChatSetting

    settings = ChatSetting.query.first()

    if settings and not settings.chat_enabled:

        flash(
            "ESA VIBES is currently disabled by the administrator.",
            "warning"
        )

        return render_template(
            "messages/chat_disabled.html"
        )

    conversations = sorted(
        ConversationMember.query.filter_by(
            user_id=current_user.id
        ).all(),
        key=lambda c: (
            c.conversation.messages[-1].created_at
            if c.conversation.messages
            else c.conversation.created_at
        ),
        reverse=True
    )

    unread_counts = {}

    for membership in conversations:

        conversation = membership.conversation

        unread = 0

        for message in conversation.messages:

            if message.sender_id == current_user.id:
                continue

            read = MessageRead.query.filter_by(
                message_id=message.id,
                user_id=current_user.id
            ).first()

            if not read:
                unread += 1

        unread_counts[conversation.id] = unread

    if current_user.role in ["Administrator", "General Secretary"]:
        return render_template(
            "messages/admin/inbox.html",
            conversations=conversations,
            unread_counts=unread_counts
        )

    return render_template(
        "messages/inbox.html",
        conversations=conversations,
        unread_counts=unread_counts
    )







@messages_bp.route("/contacts")
@login_required
def contacts():

    users = (
        User.query
        .filter(User.id != current_user.id)
        .order_by(User.role, User.full_name)
        .all()
    )

    return render_template(
        "messages/contacts.html",
        users=users
    )


@messages_bp.route("/chat/<int:user_id>")
@login_required
def start_chat(user_id):
    blocked = ChatBlock.query.filter_by(user_id=current_user.id).first()

    if blocked:
        flash(
            "Your access to ESA VIBES has been suspended.",
            "danger"
        )

        return redirect(url_for("messages.inbox"))

    other_user = User.query.get_or_404(user_id)

    # Prevent chatting with yourself
    if other_user.id == current_user.id:
        return redirect(url_for("messages.contacts"))

    # Find all conversations for current user
    memberships = ConversationMember.query.filter_by(
        user_id=current_user.id
    ).all()

    # Check whether a private conversation already exists
    for membership in memberships:

        conversation = membership.conversation

        if conversation.conversation_type != "private":
            continue

        participant_ids = {
            member.user_id
            for member in conversation.members
        }

        if participant_ids == {current_user.id, other_user.id}:

            return redirect(
                url_for(
                    "messages.view_conversation",
                    conversation_id=conversation.id
                )
            )

    # Create new private conversation
    conversation = Conversation(
        conversation_type="private",
        created_by=current_user.id
    )

    db.session.add(conversation)
    db.session.flush()

    db.session.add(
        ConversationMember(
            conversation_id=conversation.id,
            user_id=current_user.id
        )
    )

    db.session.add(
        ConversationMember(
            conversation_id=conversation.id,
            user_id=other_user.id
        )
    )

    db.session.commit()

    return redirect(
        url_for(
            "messages.view_conversation",
            conversation_id=conversation.id
        )
    )



@messages_bp.route(
    "/conversation/<int:conversation_id>",
    methods=["GET", "POST"]
)
@login_required
def view_conversation(conversation_id):

    blocked = ChatBlock.query.filter_by(user_id=current_user.id).first()

    if blocked:
        flash(
            "Your access to ESA VIBES has been suspended.",
            "danger"
        )

        return redirect(url_for("messages.inbox"))


    conversation = Conversation.query.get_or_404(conversation_id)

    # Security: Ensure current user belongs to the conversation
    if current_user.id not in [m.user_id for m in conversation.members]:
        return redirect(url_for("messages.contacts"))

    if request.method == "POST":

        text = request.form.get("message", "").strip()
        uploaded_file = request.files.get("attachment")

        reply_to_id = request.form.get("reply_to_id")

        if reply_to_id:
            reply_to_id = int(reply_to_id)
        else:
            reply_to_id = None

        # Don't allow an empty submission
        if not text and (not uploaded_file or uploaded_file.filename == ""):
            return redirect(
                url_for(
                    "messages.view_conversation",
                    conversation_id=conversation.id
                )
            )

        new_message = Message(
            conversation_id=conversation.id,
            sender_id=current_user.id,
            message=text,
            reply_to_id=reply_to_id
        )


        db.session.add(new_message)
        db.session.commit()

        # Save attachment (if any)
        if uploaded_file and uploaded_file.filename:
            filename = secure_filename(uploaded_file.filename)

            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "messages"
            )

            os.makedirs(upload_folder, exist_ok=True)

            filepath = os.path.join(upload_folder, filename)

            uploaded_file.save(filepath)

            attachment = Attachment(
                message_id=new_message.id,
                filename=filename,
                filepath=f"uploads/messages/{filename}",
                filetype=uploaded_file.content_type,
                filesize=os.path.getsize(filepath)
            )

            db.session.add(attachment)
            db.session.commit()

        return redirect(
            url_for(
                "messages.view_conversation",
                conversation_id=conversation.id
            )
        )


    other_user = next(
        (
            m.user
            for m in conversation.members
            if m.user_id != current_user.id
        ),
        None
    )

    # Load messages in chronological order
    messages = (
        Message.query
        .filter_by(conversation_id=conversation.id)
        .order_by(Message.created_at.asc())
        .all()
    )

    # Mark incoming unread messages as read
    for message in messages:

        if message.sender_id == current_user.id:
            continue

        already_read = MessageRead.query.filter_by(
            message_id=message.id,
            user_id=current_user.id
        ).first()

        if not already_read:
            db.session.add(
                MessageRead(
                    message_id=message.id,
                    user_id=current_user.id
                )
            )

    db.session.commit()

    if current_user.role in ["Administrator", "General Secretary"]:
        return render_template(
            "messages/admin/conversation.html",
            conversation=conversation,
            other_user=other_user,
            messages=messages
        )
    return render_template(
        "messages/member/conversation.html",
        conversation=conversation,
        other_user=other_user,
        messages=messages
    )
    # return render_template(
    #     "conversation.html",
    #     conversation=conversation,
    #     other_user=other_user,
    #     messages=messages
    # )




@messages_bp.route(
    "/conversation/<int:conversation_id>/voice",
    methods=["POST"]
)
@login_required
def upload_voice(conversation_id):

    conversation = Conversation.query.get_or_404(conversation_id)

    if current_user.id not in [m.user_id for m in conversation.members]:
        abort(403)

    voice = request.files.get("voice")

    if not voice:
        return ("No voice uploaded", 400)

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "messages",
        "voice"
    )

    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(
        f"{current_user.id}_{int(__import__('time').time())}.webm"
    )

    filepath = os.path.join(upload_folder, filename)

    voice.save(filepath)

    message = Message(
        conversation_id=conversation.id,
        sender_id=current_user.id,
        message=""
    )

    db.session.add(message)
    db.session.commit()

    attachment = Attachment(
        message_id=message.id,
        filename=filename,
        filepath=f"uploads/messages/voice/{filename}",
        filetype="audio/webm",
        filesize=os.path.getsize(filepath)
    )

    db.session.add(attachment)
    db.session.commit()

    return ("OK", 200)


@messages_bp.route("/conversation/<int:conversation_id>/messages")
@login_required
def conversation_messages(conversation_id):

    conversation = Conversation.query.get_or_404(conversation_id)

    if current_user.id not in [m.user_id for m in conversation.members]:
        abort(403)

    data = []

    for message in conversation.messages:

        attachments = []

        for attachment in message.attachments:
            attachments.append({
                "filename": attachment.filename,
                "filepath": url_for(
                    "static",
                    filename=attachment.filepath
                )
            })

        data.append({
            "id": message.id,
            "sender_id": message.sender_id,
            "message": message.message,
            "created_at": message.created_at.strftime("%d %b %Y %I:%M %p"),
            "attachments": attachments
        })

    return jsonify(data)



# ==========================================
# Delete Message
# ==========================================
@messages_bp.route("/delete/<int:message_id>", methods=["POST"])
@login_required
def delete_message(message_id):

    message = Message.query.get_or_404(message_id)

    # Only the sender or an Administrator can delete
    if (
        message.sender_id != current_user.id
        and current_user.role != "Administrator"
    ):
        abort(403)

    conversation_id = message.conversation_id

    db.session.delete(message)
    db.session.commit()

    flash("Message deleted successfully.", "success")

    return redirect(
        url_for(
            "messages.view_conversation",
            conversation_id=conversation_id
        )
    )

# ==========================================
# Edit Message
# ==========================================
@messages_bp.route("/edit/<int:message_id>", methods=["POST"])
@login_required
def edit_message(message_id):

    message = Message.query.get_or_404(message_id)

    # Only sender or Administrator can edit
    if (
        message.sender_id != current_user.id
        and current_user.role != "Administrator"
    ):
        abort(403)

    new_text = request.form.get("message", "").strip()

    if not new_text:
        flash("Message cannot be empty.", "warning")
        return redirect(
            url_for(
                "messages.view_conversation",
                conversation_id=message.conversation_id
            )
        )

    message.message = new_text
    message.edited = True
    message.edited_at = db.func.now()

    db.session.commit()

    flash("Message updated successfully.", "success")

    return redirect(
        url_for(
            "messages.view_conversation",
            conversation_id=message.conversation_id
        )
    )