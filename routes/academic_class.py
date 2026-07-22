from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request, flash
from extensions import db
from models.class_announcement import ClassAnnouncement
from models.member import Member
from models.class_group import ClassGroup
from models.course_rep import CourseRep

academic_class_bp = Blueprint(
    "academic_class",
    __name__,
    url_prefix="/academic-class"
)



@academic_class_bp.route("/")
@login_required
def dashboard():

    member = Member.query.filter_by(
        user_id=current_user.id
    ).first()

    if not member:
        flash("Member record not found.", "danger")
        return redirect(url_for("member_portal.dashboard"))

    if not member.class_group_id:
        flash("You are not assigned to any academic class.", "warning")
        return redirect(url_for("member_portal.dashboard"))

    class_group = ClassGroup.query.get(
        member.class_group_id
    )

    classmates = Member.query.filter_by(
        class_group_id=class_group.id
    ).order_by(
        Member.first_name,
        Member.last_name
    ).all()

    announcements = ClassAnnouncement.query.filter_by(
        class_group_id=class_group.id,
        is_active=True
    ).order_by(
        ClassAnnouncement.is_pinned.desc(),
        ClassAnnouncement.created_at.desc()
    ).all()

    can_post = False

    if current_user.role == "Administrator":
        can_post = True

    elif class_group.course_rep_id == member.id:
        can_post = True

    elif (
        class_group.assistant_course_rep_id
        and
        class_group.assistant_course_rep_id == member.id
    ):
        can_post = True
    print("=" * 50)
    print("Class Group:", class_group.name)
    print("Course Rep ID:", class_group.course_rep_id)
    print("Course Rep:", class_group.course_rep)
    print("Assistant Rep ID:", class_group.assistant_course_rep_id)
    print("Assistant Rep:", class_group.assistant_course_rep)
    print("=" * 50)
    return render_template(
        "academic_class/dashboard.html",
        member=member,
        class_group=class_group,
        classmates=classmates,
        course_rep=class_group.course_rep,
        assistant_rep=class_group.assistant_course_rep,
        announcements=announcements,
        can_post=can_post
    )