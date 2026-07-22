from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required

from extensions import db

from models.notice import Notice

from utils.auth import roles_required

from utils.audit import log_activity


notices_bp = Blueprint(
    "notices",
    __name__,
    url_prefix="/notices"
)


# ==========================================
# Notice Dashboard
# ==========================================
@notices_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def notices():

    notices = Notice.query.order_by(
        Notice.created_at.desc()
    ).all()

    return render_template(
        "notices/index.html",
        notices=notices
    )


# ==========================================
# Add Notice
# ==========================================
@notices_bp.route("/add", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def add_notice():

    if request.method == "POST":

        notice = Notice(

            title=request.form["title"],

            message=request.form["message"],

            category=request.form["category"],

            status=request.form["status"],

            is_pinned=True if request.form.get("is_pinned") else False

        )

        db.session.add(notice)
        db.session.commit()

        print("=== BEFORE AUDIT ===")

        log_activity(
            module="Notice Board",
            action="Created Notice",
            description=notice.title
        )

        print("=== AFTER AUDIT ===")

        flash(
            "Notice created successfully.",
            "success"
        )

        return redirect(
            url_for("notices.notices")
        )

    return render_template(
        "notices/add.html"
    )