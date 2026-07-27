from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from extensions import db
from services.notification_service import notify_class_members
from models.class_notice import ClassNotice
from models.class_group import ClassGroup
from models.member import Member
from models.course_rep import CourseRep


class_notices_bp = Blueprint(
    "class_notices",
    __name__,
    url_prefix="/class-notices"
)


@class_notices_bp.route("/create/<int:class_group_id>",
                        methods=["GET", "POST"])
@login_required
def create(class_group_id):

    group = ClassGroup.query.get_or_404(class_group_id)

    is_admin = current_user.role == "Administrator"

    member = getattr(current_user, "member_profile", None)

    is_course_rep = False

    if member:
        is_course_rep = CourseRep.query.filter_by(
            class_group_id=group.id,
            member_id=member.id,
            position="Course Rep"
        ).first() is not None

    if not (is_admin or is_course_rep):
        flash(
            "You are not authorized to post notices for this class.",
            "danger"
        )
        return redirect(url_for("class_groups.view", id=group.id))

    if request.method == "POST":

        notice = ClassNotice(
            class_group_id=group.id,
            created_by_user_id=current_user.id,
            title=request.form.get("title"),
            message=request.form.get("message")
        )

        db.session.add(notice)
        db.session.commit()

        notify_class_members(
            class_group=group,
            title=notice.title,
            message=notice.message,
            link=url_for(
                "class_groups.view",
                id=group.id
            )
        )


        flash(
            "Class notice posted successfully.",
            "success"
        )


        return redirect(
            url_for(
                "class_groups.view",
                id=group.id
            )
        )

    notices = (
        ClassNotice.query
        .filter_by(
            class_group_id=group.id,
            status="Active"
        )
        .order_by(ClassNotice.created_at.desc())
        .all()
    )

    return render_template(
        "class_notices/add.html",
        group=group,
        notices=notices
    )

@class_notices_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):

    notice = ClassNotice.query.get_or_404(id)

    is_admin = current_user.role == "Administrator"

    if not is_admin and notice.created_by_user_id != current_user.id:
        flash("You are not authorized to edit this notice.", "danger")
        return redirect(url_for("class_groups.view", id=notice.class_group_id))

    if request.method == "POST":

        notice.title = request.form.get("title")
        notice.message = request.form.get("message")

        db.session.commit()

        flash("Notice updated successfully.", "success")

        return redirect(
            url_for(
                "class_groups.view",
                id=notice.class_group_id
            )
        )

    return render_template(
        "class_notices/edit.html",
        notice=notice
    )


@class_notices_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):

    notice = ClassNotice.query.get_or_404(id)

    is_admin = current_user.role == "Administrator"

    if not is_admin and notice.created_by_user_id != current_user.id:
        flash("You are not authorized to delete this notice.", "danger")
        return redirect(url_for("class_groups.view", id=notice.class_group_id))

    class_id = notice.class_group_id

    db.session.delete(notice)
    db.session.commit()

    flash("Notice deleted successfully.", "success")

    return redirect(
        url_for(
            "class_groups.view",
            id=class_id
        )
    )