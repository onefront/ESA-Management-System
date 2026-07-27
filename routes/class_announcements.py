import os
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
from uuid import uuid4
from werkzeug.utils import secure_filename
from flask import current_app
from extensions import db
from datetime import datetime
from models.member import Member
from models.class_group import ClassGroup
from models.class_announcement import ClassAnnouncement

class_announcements_bp = Blueprint(
    "class_announcements",
    __name__,
    url_prefix="/class-announcements"
)



@class_announcements_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():

    member = Member.query.filter_by(user_id=current_user.id).first()

    if not member:
        flash("Member record not found.", "danger")
        return redirect(url_for("member_portal.dashboard"))

    class_group = member.class_group

    if not class_group:
        flash("You are not assigned to an academic class.", "warning")
        return redirect(url_for("member_portal.dashboard"))

    is_course_rep = (
        class_group.course_rep_id == member.id
    )

    is_assistant = (
        class_group.assistant_course_rep_id == member.id
    )

    print("=" * 50)
    print("Member ID:", member.id)
    print("Class Group:", class_group.name)
    print("Course Rep ID:", class_group.course_rep_id)
    print("Assistant Rep ID:", class_group.assistant_course_rep_id)
    print("Is Course Rep:", is_course_rep)
    print("Is Assistant:", is_assistant)
    print("=" * 50)

    if not (is_course_rep or is_assistant):
        flash(
            "Only the Course Representative or Assistant Course Representative can post class announcements.",
            "danger"
        )
        return redirect(url_for("member_portal.dashboard"))

    if request.method == "POST":
        from datetime import datetime

        # Upload attachment
        attachment = request.files.get("attachment")

        filename = None
        attachment_name = None
        attachment_type = None

        if attachment and attachment.filename:

            allowed_extensions = {
                "pdf",
                "doc",
                "docx",
                "xls",
                "xlsx",
                "ppt",
                "pptx"
            }

            extension = attachment.filename.rsplit(".", 1)[1].lower()

            if extension not in allowed_extensions:
                flash(
                    "Only PDF, Word, Excel and PowerPoint files are allowed.",
                    "danger"
                )

                return redirect(request.url)

            upload_folder = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                "class_announcements"
            )

            os.makedirs(upload_folder, exist_ok=True)

            from uuid import uuid4

            extension = attachment.filename.rsplit(".", 1)[1].lower()

            filename = f"{uuid4().hex}.{extension}"

            attachment.save(
                os.path.join(upload_folder, filename)
            )

            attachment_name = attachment.filename
            attachment_type = attachment.content_type

        announcement = ClassAnnouncement(
            class_group_id=class_group.id,
            created_by=member.id,
            title=request.form["title"],
            message=request.form["message"],
            event_date=(
                datetime.strptime(request.form["event_date"], "%Y-%m-%d").date()
                if request.form.get("event_date")
                else None
            ),
            event_time=(
                datetime.strptime(request.form["event_time"], "%H:%M").time()
                if request.form.get("event_time")
                else None
            ),
            venue=request.form.get("venue") or None,

            attachment=f"class_announcements/{filename}" if filename else None,
            attachment_name=attachment_name,
            attachment_type=attachment_type
        )

        db.session.add(announcement)
        db.session.commit()

        flash(
            "Announcement published successfully.",
            "success"
        )

        return redirect(
            url_for("academic_class.dashboard")
        )

    return render_template(
        "class_announcements/new.html",
        class_group=class_group
    )


@class_announcements_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):

    member = Member.query.filter_by(user_id=current_user.id).first()

    if not member:
        flash("Member record not found.", "danger")
        return redirect(url_for("member_portal.dashboard"))

    announcement = ClassAnnouncement.query.get_or_404(id)

    if announcement.created_by != member.id:
        flash("You are not authorized to edit this announcement.", "danger")
        return redirect(url_for("class_announcements.index"))

    if request.method == "POST":
        from datetime import datetime

        announcement.title = request.form["title"]
        announcement.message = request.form["message"]

        announcement.event_date = (
            datetime.strptime(request.form["event_date"], "%Y-%m-%d").date()
            if request.form.get("event_date")
            else None
        )

        time_value = request.form.get("event_time")

        if time_value:
            try:
                announcement.event_time = datetime.strptime(
                    time_value,
                    "%H:%M:%S"
                ).time()
            except ValueError:
                announcement.event_time = datetime.strptime(
                    time_value,
                    "%H:%M"
                ).time()
        else:
            announcement.event_time = None
        announcement.venue = request.form.get("venue") or None

        db.session.commit()

        flash(
            "Announcement updated successfully.",
            "success"
        )

        return redirect(url_for("class_announcements.index"))

    return render_template(
        "class_announcements/edit.html",
        announcement=announcement,
        class_group=member.class_group,
        member=member
    )






@class_announcements_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):

    member = Member.query.filter_by(user_id=current_user.id).first()

    if not member:
        flash("Member record not found.", "danger")
        return redirect(url_for("member_portal.dashboard"))

    announcement = ClassAnnouncement.query.get_or_404(id)

    if announcement.created_by != member.id:
        flash(
            "You are not authorized to delete this announcement.",
            "danger"
        )
        return redirect(url_for("class_announcements.index"))

    db.session.delete(announcement)
    db.session.commit()

    flash(
        "Announcement deleted successfully.",
        "success"
    )

    return redirect(url_for("class_announcements.index"))

@class_announcements_bp.route("/")
@login_required
def index():

    member = Member.query.filter_by(
        user_id=current_user.id
    ).first()

    if not member or not member.class_group:
        flash(
            "You are not assigned to an academic class.",
            "warning"
        )
        return redirect(url_for("member_portal.dashboard"))

    announcements = (
        ClassAnnouncement.query
        .filter_by(
            class_group_id=member.class_group.id,
            is_active=True
        )
        .order_by(
            ClassAnnouncement.is_pinned.desc(),
            ClassAnnouncement.created_at.desc()
        )
        .all()
    )

    return render_template(
        "class_announcements/index.html",
        announcements=announcements,
        class_group=member.class_group,
        member=member
    )