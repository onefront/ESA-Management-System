from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.member import Member
from models.class_group import ClassGroup
from models.course_rep import CourseRep
from models.fee_setting import FeeSetting
from utils.auth import admin_required
from models.class_notice import ClassNotice
from flask import request, flash, redirect, url_for
class_groups_bp = Blueprint(
    "class_groups",
    __name__,
    url_prefix="/class-groups"
)




REQUIRED_PAYMENT_TYPES = [
    "Registration Fee",
    "Annual Dues",
    "Welfare Levy"
]

REGISTRATION_REQUIRED = 200
ANNUAL_DUES_REQUIRED = 50
TOTAL_REQUIRED = REGISTRATION_REQUIRED + ANNUAL_DUES_REQUIRED



@class_groups_bp.route("/")
@login_required
@admin_required
def index():
    class_groups = ClassGroup.query.order_by(
        ClassGroup.name
    ).all()

    return render_template(
        "class_groups/index.html",
        class_groups=class_groups
    )
from flask import request, redirect, url_for, flash
from models.programme import Programme
from extensions import db
from models.payment import Payment





@class_groups_bp.route("/my-class")
@login_required
def my_class():

    if not current_user.member_profile:
        flash("Member profile not found.", "warning")
        return redirect(url_for("dashboard.dashboard"))

    member = current_user.member_profile

    if not member.class_group_id:
        flash(
            "You have not yet been assigned to a Class Group.",
            "warning"
        )
        return redirect(url_for("dashboard.dashboard"))

    return redirect(
        url_for(
            "class_groups.view",
            id=member.class_group_id
        )
    )


@class_groups_bp.route("/view/<int:id>")
@login_required
def view(id):

    group = ClassGroup.query.get_or_404(id)

    total_members = Member.query.filter_by(
        class_group_id=group.id
    ).count()

    male_members = Member.query.filter_by(
        class_group_id=group.id,
        gender="Male"
    ).count()

    female_members = Member.query.filter_by(
        class_group_id=group.id,
        gender="Female"
    ).count()

    course_rep_count = CourseRep.query.filter_by(
        class_group_id=group.id
    ).count()

    course_rep = CourseRep.query.filter_by(
        class_group_id=group.id,
        position="Course Rep"
    ).first()

    assistant_rep = CourseRep.query.filter_by(
        class_group_id=group.id,
        position="Assistant Course Rep"
    ).first()

    member = current_user.member_profile

    is_admin = (
            current_user.role == "Administrator"
    )

    is_course_rep = False

    if member:

        # Main Course Representative
        if course_rep and course_rep.member_id == member.id:
            is_course_rep = True

        # Assistant Course Representative
        elif assistant_rep and assistant_rep.member_id == member.id:
            is_course_rep = True

    # Select the correct template
    template = (
        "class_groups/view.html"
        if is_admin
        else "member_portal/class_view.html"
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
        template,
        group=group,
        total_members=total_members,
        male_members=male_members,
        female_members=female_members,
        course_rep_count=course_rep_count,
        course_rep=course_rep,
        assistant_rep=assistant_rep,
        notices=notices,

        can_add_members=is_admin,
        can_assign_reps=is_admin,
        can_send_notice=(is_admin or is_course_rep)
    )



@class_groups_bp.route("/<int:id>/members")
@login_required
def members(id):

    group = ClassGroup.query.get_or_404(id)
    fee = FeeSetting.query.filter_by(active=True).first()

    if fee:
        registration_required = fee.registration_fee
        annual_dues_required = fee.annual_dues
        welfare_required = fee.welfare_levy
        other_required = fee.other_fee

        total_required = (
                registration_required +
                annual_dues_required +
                welfare_required +
                other_required
        )
    else:
        registration_required = 200
        annual_dues_required = 50
        welfare_required = 0
        other_required = 0
        total_required = 250
    status = request.args.get("status", "all")
    members = (
        Member.query
        .filter_by(class_group_id=id)
        .order_by(Member.last_name, Member.first_name)
        .all()
    )
    for member in members:

        registration_paid = sum(
            p.amount for p in member.payments
            if p.payment_type == "Registration Fee"
            and p.status == "Approved"
        )

        dues_paid = sum(
            p.amount for p in member.payments
            if p.payment_type == "Annual Dues"
            and p.status == "Approved"
        )

        total_paid = registration_paid + dues_paid

        balance = max(total_required - total_paid, 0)

        if (
                registration_paid >= registration_required
                and dues_paid >= annual_dues_required
        ):
            payment_status = "Paid"
        elif total_paid > 0:
            payment_status = "Partial"
        else:
            payment_status = "Outstanding"

        member.registration_paid = registration_paid
        member.dues_paid = dues_paid
        member.total_paid = total_paid
        member.balance = balance
        member.payment_status = payment_status
    if status == "paid":
        members = [m for m in members if m.payment_status == "Paid"]

    elif status == "partial":
        members = [m for m in members if m.payment_status == "Partial"]

    elif status == "outstanding":
        members = [m for m in members if m.payment_status == "Outstanding"]


    member_count = len(members)

    male_count = sum(1 for m in members if m.gender == "Male")
    female_count = sum(1 for m in members if m.gender == "Female")

    paid_count = sum(
        1 for m in members
        if m.payment_status == "Paid"
    )

    partial_count = sum(
        1 for m in members
        if m.payment_status == "Partial"
    )

    unpaid_count = sum(
        1 for m in members
        if m.payment_status == "Outstanding"
    )

    return render_template(
        "class_groups/members.html",
        group=group,
        members=members,
        member_count=member_count,
        male_count=male_count,
        female_count=female_count,
        paid_count=paid_count,
        partial_count=partial_count,
        unpaid_count=unpaid_count,
    status = status,
    )


@class_groups_bp.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def add():

    programmes = Programme.query.order_by(
        Programme.programme_name
    ).all()
    admission_years = [
        f"{year}/{year + 1}"
        for year in range(2023, 2051)
    ]
    if request.method == "POST":
        programme = Programme.query.get(request.form["programme_id"])

        programme_name = programme.programme_name

        admission = request.form["admission_year"].split("/")[0]

        words = programme_name.split()

        abbreviation = ""

        for word in words:
            if word.upper() not in ["B.SC.", "BSC", "B.ED.", "BED", "OF", "IN"]:
                abbreviation += word[0].upper()

        session_code = "W" if request.form["session"] == "Weekend" else "E"

        generated_name = (
            f"{abbreviation}-"
            f"{session_code}"
            f"{request.form['level']}-"
            f"{admission}"
        )
        existing = ClassGroup.query.filter_by(
            name=generated_name
        ).first()

        if existing:
            flash(
                "This Academic Class already exists.",
                "warning"
            )
            return redirect(url_for("class_groups.add"))
        group = ClassGroup(
            name=generated_name,
            programme_id=request.form["programme_id"],
            session=request.form["session"],
            level=request.form["level"],
            admission_year=request.form["admission_year"],
            graduation_year=request.form["graduation_year"],
            status=request.form["status"]
        )

        db.session.add(group)
        db.session.flush()

        programme = Programme.query.get(group.programme_id)

        if programme:

            members = Member.query.filter_by(
                programme=programme.programme_name,
                level=group.level,
                session=group.session
            ).all()

            for member in members:
                member.class_group_id = group.id

        db.session.commit()

        flash(
            f"Class Group added successfully. {len(members) if programme else 0} member(s) assigned automatically.",
            "success"
        )

        return redirect(url_for("class_groups.index"))

    return render_template(
        "class_groups/add.html",
        programmes=programmes,
        admission_years=admission_years
    )
@class_groups_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit(id):

    group = ClassGroup.query.get_or_404(id)

    programmes = Programme.query.order_by(
        Programme.programme_name
    ).all()
    # admission_years = [
    #     f"{year}/{year + 1}"
    #     for year in range(2023, 2051)
    # ]
    if request.method == "POST":

        group.name = request.form["name"]
        group.programme_id = request.form["programme_id"]
        group.session = request.form["session"]
        group.level = request.form["level"]
        group.admission_year = request.form["admission_year"]
        group.graduation_year = request.form["graduation_year"]
        group.status = request.form["status"]

        db.session.commit()

        flash("Class Group updated successfully.", "success")

        return redirect(url_for("class_groups.index"))

    return render_template(
        "class_groups/edit.html",
        group=group,
        programmes=programmes
    )
@class_groups_bp.route("/delete/<int:id>")
@login_required
@admin_required
def delete(id):
    group = ClassGroup.query.get_or_404(id)

    db.session.delete(group)
    db.session.commit()

    flash("Class Group deleted successfully.", "success")

    return redirect(url_for("class_groups.index"))