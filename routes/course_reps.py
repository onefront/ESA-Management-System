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
from models.user import User
from models.course_rep import CourseRep
from models.member import Member

from utils.auth import roles_required
from utils.audit import log_activity


course_reps_bp = Blueprint(
    "course_reps",
    __name__,
    url_prefix="/course-reps"
)


# ==========================================
# Course Representatives
# ==========================================
@course_reps_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def course_reps():
    search = request.args.get("search", "").strip()

    query = CourseRep.query

    if search:
        query = query.join(Member).filter(

            db.or_(

                Member.first_name.ilike(f"%{search}%"),
                Member.last_name.ilike(f"%{search}%"),
                Member.student_id.ilike(f"%{search}%"),
                Member.programme.ilike(f"%{search}%")

            )

        )

    reps = query.order_by(
        CourseRep.appointed_date.desc()
    ).all()

    # Summary Cards
    total_reps = CourseRep.query.count()

    course_rep_count = CourseRep.query.filter_by(
        position="Course Rep"
    ).count()

    assistant_rep_count = CourseRep.query.filter_by(
        position="Assistant Course Rep"
    ).count()


    return render_template(

    "course_reps/index.html",

    reps=reps,

    total_reps=total_reps,

    course_rep_count=course_rep_count,

    assistant_rep_count=assistant_rep_count,

    search=search

)

@course_reps_bp.route("/assign/<int:class_group_id>", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def assign_class_reps(class_group_id):

    class_group = ClassGroup.query.get_or_404(class_group_id)

    if request.method == "POST":
        return add_course_rep_for_class(class_group)

    appointed_ids = [
        rep.member_id
        for rep in CourseRep.query.filter_by(
            class_group_id=class_group.id
        ).all()
    ]

    members = Member.query.filter(
        Member.class_group_id == class_group.id,
        ~Member.id.in_(appointed_ids)
    ).order_by(
        Member.first_name
    ).all()

    return render_template(
        "course_reps/add.html",
        members=members,
        class_group=class_group
    )

# ==========================================
# View Course Representative
# ==========================================
@course_reps_bp.route("/view/<int:rep_id>")
@login_required
@roles_required("Administrator", "General Secretary")
def view_course_rep(rep_id):

    rep = CourseRep.query.get_or_404(rep_id)

    return render_template(
        "course_reps/view.html",
        rep=rep
    )
# ==========================================
# Edit Course Representative
# ==========================================
@course_reps_bp.route("/edit/<int:rep_id>", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def edit_course_rep(rep_id):

    rep = CourseRep.query.get_or_404(rep_id)

    if request.method == "POST":

        position = request.form.get("position")
        status = request.form.get("status")

        if not position or not status:
            flash(
                "Please complete all required fields.",
                "danger"
            )
            return redirect(
                url_for(
                    "course_reps.edit_course_rep",
                    rep_id=rep.id
                )
            )

        rep.position = position
        rep.status = status

        db.session.commit()

        log_activity(
            module="Course Representatives",
            action="Updated Course Representative",
            description=f"{rep.member.first_name} {rep.member.last_name}"
        )

        flash(
            "Course Representative updated successfully.",
            "success"
        )

        return redirect(
            url_for("course_reps.course_reps")
        )

    return render_template(
        "course_reps/edit.html",
        rep=rep
    )
# ==========================================
# Add Course Representative
# ==========================================
@course_reps_bp.route("/add", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def add_course_rep():

    if request.method == "POST":

        member_id = request.form.get("member_id")
        position = request.form.get("position")
        member = Member.query.get_or_404(member_id)
        print("=" * 60)
        print("Selected Member:", member.first_name, member.last_name)
        print("Member ID:", member.id)
        print("Member Class Group ID:", member.class_group_id)
        print("=" * 60)
        # -----------------------------------------
        # Check if this class already has
        # this position
        # -----------------------------------------
        existing_reps = CourseRep.query.all()

        for rep in existing_reps:

            existing_member = rep.member

            if (
                    existing_member.programme == member.programme
                    and existing_member.level == member.level
                    and existing_member.session == member.session
                    and rep.position == position
            ):
                flash(
                    f"{member.programme} "
                    f"Level {member.level} "
                    f"({member.session}) "
                    f"already has a {position}.",
                    "danger"
                )

                return redirect(
                    url_for("course_reps.add_course_rep")
                )

        # Ensure the selected member belongs to a class group
        if not member.class_group_id:
            flash(
                "The selected member has not been assigned to a class group.",
                "danger"
            )
            return redirect(
                url_for("course_reps.add_course_rep")
            )

        rep = CourseRep(
            member_id=member.id,
            class_group_id=member.class_group_id,
            position=position,
            status="Active"
        )

        db.session.add(rep)

        # Update the ClassGroup leadership
        class_group = member.class_group

        if position == "Course Rep":
            class_group.course_rep_id = member.id

        elif position == "Assistant Course Rep":
            class_group.assistant_course_rep_id = member.id

        db.session.commit()
        db.session.refresh(class_group)

        print("=" * 60)
        print("AFTER COMMIT")
        print("Course Rep After:", class_group.course_rep_id)
        print("Assistant Rep After:", class_group.assistant_course_rep_id)
        print("=" * 60)

        log_activity(
            module="Course Representatives",
            action=f"Appointed {position}",
            description=f"{member.first_name} {member.last_name}"
        )
        flash(
            "Course Representative appointed successfully.",
            "success"
        )

        return redirect(
            url_for("course_reps.course_reps")
        )

    # Get IDs of members already appointed
    appointed_ids = [
        rep.member_id
        for rep in CourseRep.query.all()
    ]

    # Only members who are not already appointed
    members = Member.query.filter(
        ~Member.id.in_(appointed_ids)
    ).order_by(
        Member.first_name
    ).all()

    return render_template(
        "course_reps/add.html",
        members=members
    )

# Remove Course Representative
# ==========================================
@course_reps_bp.route("/delete/<int:rep_id>", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def delete_course_rep(rep_id):
    rep = CourseRep.query.get_or_404(rep_id)

    member = rep.member

    class_group = member.class_group

    if request.method == "POST":

        if member.user_id:

            user = User.query.get(member.user_id)

            if user:
                user.role = "Member"

        log_activity(
            module="Course Representatives",
            action="Removed Course Representative",
            description=f"{member.first_name} {member.last_name}"
        )

        if rep.position == "Course Rep":
            class_group.course_rep_id = None

        elif rep.position == "Assistant Course Rep":
            class_group.assistant_course_rep_id = None

        db.session.delete(rep)

        db.session.commit()

        flash(
            "Course Representative removed successfully.",
            "success"
        )

        return redirect(
            url_for("course_reps.course_reps")
        )

    return render_template(
        "course_reps/delete.html",
        rep=rep
    )
