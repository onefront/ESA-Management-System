from flask import Blueprint, render_template
from flask_login import login_required


from utils.auth import roles_required
from flask import redirect, url_for, flash
from flask_login import current_user

from extensions import db
from models.user import User
from models.chat_block import ChatBlock
chat_block_bp = Blueprint(
    "chat_block",
    __name__,
    url_prefix="/chat-blocks"
)


@chat_block_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def index():

    blocked_users = (
        ChatBlock.query
        .order_by(ChatBlock.blocked_at.desc())
        .all()
    )

    return render_template(
        "chat_admin/blocked_users.html",
        blocked_users=blocked_users
    )

# ==========================================
# Block User
# ==========================================
@chat_block_bp.route("/block/<int:user_id>")
@login_required
@roles_required("Administrator", "General Secretary")
def block_user(user_id):

    user = User.query.get_or_404(user_id)

    # Prevent blocking yourself
    if user.id == current_user.id:
        flash("You cannot block yourself.", "danger")
        return redirect(url_for("users.users"))

    # Already blocked?
    existing = ChatBlock.query.filter_by(user_id=user.id).first()

    if existing:
        flash("User is already blocked.", "warning")
        return redirect(url_for("users.users"))

    block = ChatBlock(
        user_id=user.id,
        blocked_by=current_user.id,
        reason="Blocked by administrator"
    )

    db.session.add(block)
    db.session.commit()

    flash(f"{user.full_name} has been blocked from ESA VIBES.", "success")

    return redirect(url_for("users.users"))


# ==========================================
# Unblock User
# ==========================================
@chat_block_bp.route("/unblock/<int:user_id>")
@login_required
@roles_required("Administrator", "General Secretary")
def unblock_user(user_id):

    block = ChatBlock.query.filter_by(user_id=user_id).first_or_404()

    db.session.delete(block)
    db.session.commit()

    flash("User has been unblocked.", "success")

    return redirect(url_for("users.users"))