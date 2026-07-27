from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required


from models.conversation_member import ConversationMember
from models.user import User
from models.conversation import Conversation
from models.message import Message
from flask_login import current_user
from utils.auth import roles_required
from extensions import db
chat_admin_bp = Blueprint(
    "chat_admin",
    __name__,
    url_prefix="/chat-admin"
)


# ==========================================
# Chat Management Dashboard
# ==========================================
@chat_admin_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def dashboard():

    return render_template(
        "chat_admin/dashboard.html"
    )


# ==========================================
# Chat Settings
# ==========================================
@chat_admin_bp.route("/settings", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def settings():

    from models.chat_setting import ChatSetting

    settings = ChatSetting.query.first()

    if not settings:
        settings = ChatSetting()
        db.session.add(settings)
        db.session.commit()

    if request.method == "POST":
        settings.chat_enabled = "chat_enabled" in request.form
        settings.maintenance_mode = "maintenance_mode" in request.form
        settings.member_to_member = "member_to_member" in request.form
        settings.member_to_admin = "member_to_admin" in request.form
        settings.allow_attachments = "allow_attachments" in request.form

        settings.max_upload_mb = int(
            request.form.get("max_upload_mb", 10)
        )

        settings.max_message_length = int(
            request.form.get("max_message_length", 5000)
        )

        settings.welcome_message = request.form.get(
            "welcome_message",
            ""
        )

        db.session.commit()

        flash(
            "Chat settings updated successfully.",
            "success"
        )

        return redirect(
            url_for("chat_admin.settings")
        )
    return render_template(
        "chat_admin/settings.html",
        settings=settings
    )

# ==========================================
# Broadcast Messages
@chat_admin_bp.route("/broadcast", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def broadcast():

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        broadcast_type = request.form.get("broadcast_type")
        message = request.form.get("message", "").strip()

        if not title:
            flash("Broadcast title is required.", "danger")
            return redirect(url_for("chat_admin.broadcast"))

        if not message:
            flash("Broadcast message is required.", "danger")
            return redirect(url_for("chat_admin.broadcast"))

        conversation = Conversation(
            conversation_type="broadcast",
            title=title,
            created_by=current_user.id
        )

        db.session.add(conversation)
        db.session.flush()

        message_record = Message(
            conversation_id=conversation.id,
            sender_id=current_user.id,
            message=message
        )

        db.session.add(message_record)

        # Add every active user to the broadcast conversation
        active_users = User.query.filter_by(is_active=True).all()

        for user in active_users:
            member = ConversationMember(
                conversation_id=conversation.id,
                user_id=user.id,
                is_admin=(user.id == current_user.id)
            )
            db.session.add(member)

        db.session.commit()
        print("=" * 50)
        print("Creating broadcast for users...")

        active_users = User.query.filter_by(is_active=True).all()
        print(f"Active users found: {len(active_users)}")

        for user in active_users:
            print(f"Adding: {user.username} ({user.id})")
            member = ConversationMember(
                conversation_id=conversation.id,
                user_id=user.id,
                is_admin=(user.id == current_user.id)
            )
            db.session.add(member)

        print("Finished adding conversation members.")
        print("=" * 50)

        flash(
            "Broadcast created successfully.",
            "success"
        )

        return redirect(url_for("chat_admin.broadcast"))

    broadcasts = (
        Conversation.query
        .filter_by(conversation_type="broadcast")
        .order_by(Conversation.created_at.desc())
        .all()
    )

    return render_template(
        "chat_admin/broadcast.html",
        broadcasts=broadcasts
    )
@chat_admin_bp.route("/broadcast/<int:conversation_id>/delete", methods=["POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def delete_broadcast(conversation_id):

    conversation = Conversation.query.get_or_404(conversation_id)

    if conversation.conversation_type != "broadcast":
        flash(
            "Only broadcast conversations can be deleted.",
            "danger"
        )
        return redirect(url_for("chat_admin.broadcast"))

    db.session.delete(conversation)
    db.session.commit()

    flash(
        "Broadcast deleted successfully.",
        "success"
    )

    return redirect(url_for("chat_admin.broadcast"))