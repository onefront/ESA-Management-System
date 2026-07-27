from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for
)
from flask_login import (
    login_required,
    current_user
)

from extensions import db
from models.notification import Notification

notifications_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/notifications"
)


@notifications_bp.route("/")
@login_required
def index():

    notifications = (
        Notification.query
        .filter_by(user_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    template = (
        "member_portal/notifications.html"
        if current_user.role == "Member"
        else "notifications/index.html"
    )

    return render_template(
        template,
        notifications=notifications
    )



@notifications_bp.route("/latest")
@login_required
def latest():

    notifications = (
        Notification.query
        .filter_by(user_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "notifications/dropdown.html",
        notifications=notifications
    )



@notifications_bp.route("/read/<int:id>")
@login_required
def read(id):

    notification = Notification.query.get_or_404(id)

    if notification.user_id != current_user.id:
        return redirect(url_for("notifications.index"))

    notification.is_read = True
    db.session.commit()

    if notification.link:
        return redirect(notification.link)

    return redirect(url_for("notifications.index"))