from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from flask_login import login_required
from models.member_index import MemberIndex
from extensions import db
from models.user import User
from models.conversation import Conversation
from models.conversation_member import ConversationMember
from utils.auth import admin_required

users_bp = Blueprint("users", __name__)


# ==========================================
# Users List
# ==========================================
@users_bp.route("/users")
@login_required
@admin_required
def users():

    users = User.query.order_by(
        User.full_name
    ).all()

    return render_template(
        "users/index.html",
        users=users
    )


# ==========================================
# Add User
# ==========================================
@users_bp.route("/users/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_user():

    if request.method == "POST":
        existing_user = User.query.filter_by(
            email=request.form["email"]
        ).first()

        if existing_user:
            flash(
                "A user with this email already exists.",
                "danger"
            )
            return redirect(url_for("users.add_user"))

        user = User(
            full_name=request.form["full_name"],
            email=request.form["email"],
            role=request.form["role"]
        )

        user.set_password(request.form["password"])

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("users.users"))

    return render_template("users/add.html")
# ==========================================
# Edit User
# ==========================================
@users_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(user_id):

    user = User.query.get_or_404(user_id)

    if request.method == "POST":

        user.full_name = request.form["full_name"]
        user.email = request.form["email"]
        user.role = request.form["role"]

        db.session.commit()

        return redirect(url_for("users.users"))

    return render_template(
        "users/edit.html",
        user=user
    )

# ==========================================
# ==========================================
# Delete User
# ==========================================
@users_bp.route("/users/<int:user_id>/delete", methods=["GET", "POST"])
@login_required
@admin_required
def delete_user(user_id):

    user = User.query.get_or_404(user_id)

    if request.method == "POST":

        # Prevent deletion of the main administrator
        if user.email == "admin@usted.edu.gh":
            flash(
                "The main administrator account cannot be deleted.",
                "danger"
            )
            return redirect(url_for("users.users"))

        # Remove references from MemberIndex
        member_indexes = MemberIndex.query.filter_by(
            used_by=user.id
        ).all()

        for member_index in member_indexes:
            member_index.used_by = None
            member_index.used = False
            member_index.used_at = None

        # Delete the user's conversation memberships first
        ConversationMember.query.filter_by(
            user_id=user.id
        ).delete(synchronize_session=False)

        # Delete conversations created by this user
        Conversation.query.filter_by(
            created_by=user.id
        ).delete(synchronize_session=False)

        # Finally delete the user
        db.session.delete(user)

        db.session.commit()

        flash("User deleted successfully.", "success")

        return redirect(url_for("users.users"))

    return render_template(
        "users/delete.html",
        user=user
    )
# ==========================================
# Activate / Deactivate User
# ==========================================
@users_bp.route("/users/<int:user_id>/toggle")
@login_required
@admin_required
def toggle_user(user_id):

    user = User.query.get_or_404(user_id)

    # Prevent disabling the main administrator
    if user.email == "admin@usted.edu.gh":
        flash(
            "The main administrator account cannot be disabled.",
            "danger"
        )
        return redirect(url_for("users.users"))

    user.is_active = not user.is_active

    db.session.commit()

    flash("User status updated successfully.", "success")

    return redirect(url_for("users.users"))
# ==========================================
# Reset Password
# ==========================================
@users_bp.route("/users/<int:user_id>/reset-password", methods=["GET", "POST"])
@login_required
@admin_required
def reset_password(user_id):

    user = User.query.get_or_404(user_id)

    if request.method == "POST":

        user.set_password(request.form["password"])

        db.session.commit()

        flash("Password reset successfully.", "success")

        return redirect(url_for("users.users"))

    return render_template(
        "users/reset_password.html",
        user=user
    )

@users_bp.route("/view-username/<int:user_id>")
@login_required
@admin_required
def view_username(user_id):

    user = User.query.get_or_404(user_id)

    return render_template(
        "users/view_username.html",
        user=user
    )