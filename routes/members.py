import os
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    current_app,
    flash,
    jsonify,make_response
)
from flask_login import login_required, current_user
from utils.audit import log_activity
from dateutil.relativedelta import relativedelta
from models.course_rep import CourseRep
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from io import BytesIO
from models.member_index import MemberIndex
from models.user import User
from models.vote import Vote
from models.candidate import Candidate
from models.payment import Payment
from models.attendance import Attendance
from models.class_announcement import ClassAnnouncement
from sqlalchemy import func, or_
from werkzeug.utils import secure_filename
from utils.auth import roles_required
from flask_login import login_required
from extensions import db
from models.member import Member
from models.department import Department
from models.programme import Programme
from models.class_group import ClassGroup
from datetime import datetime
from models.faculty import Faculty
members_bp = Blueprint("members", __name__)


# ==========================================
# Members List
# ==========================================
from sqlalchemy import func

@members_bp.route("/members")
@login_required
@roles_required("Administrator", "General Secretary")
def members():

    search = request.args.get("search", "")
    programme = request.args.get("programme", "")
    level = request.args.get("level", "")
    session = request.args.get("session", "")

    page = request.args.get("page", 1, type=int)

    query = Member.query

    # -------------------------------
    # Search
    # -------------------------------
    if search:
        query = query.filter(
            or_(
                Member.first_name.ilike(f"%{search}%"),
                Member.last_name.ilike(f"%{search}%"),
                Member.student_id.ilike(f"%{search}%"),
                Member.esa_id.ilike(f"%{search}%"),
                Member.phone.ilike(f"%{search}%")
            )
        )

    # -------------------------------
    # Filters
    # -------------------------------
    if programme:
        query = query.filter(Member.programme == programme)

    if level:
        query = query.filter(Member.level == level)

    if session:
        query = query.filter(Member.session == session)

    # -------------------------------
    # Statistics
    # -------------------------------
    total_members = Member.query.count()
    active_members = Member.query.filter_by(
        status="Active"
    ).count()

    total_programmes = Programme.query.count()

    weekend_members = Member.query.filter_by(
        session="Weekend"
    ).count()

    evening_members = Member.query.filter_by(
        session="Evening"
    ).count()

    # -------------------------------
    # Pagination
    # -------------------------------
    members = query.order_by(
        Member.first_name.asc(),
        Member.last_name.asc()
    ).paginate(
        page=page,
        per_page=25
    )

    programmes = Programme.query.order_by(
        Programme.programme_name
    ).all()

    return render_template(
        "members/index.html",

        members=members,

        programmes=programmes,

        total_members=total_members,

        total_programmes=total_programmes,

        weekend_members=weekend_members,

        evening_members=evening_members,
        active_members=active_members,

        search=search,

        programme=programme,

        level=level,

        session=session

    )
# ==========================================
# Add Member
# ==========================================
@members_bp.route("/members/add", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def add_member():
    selected_class_group = request.args.get(
        "class_group_id",
        type=int
    )

    selected_group = None

    if selected_class_group:
        selected_group = ClassGroup.query.get(selected_class_group)
    if request.method == "POST":
        student_id = request.form["student_id"]

        existing_member = Member.query.filter_by(student_id=student_id).first()

        if existing_member:
            flash("A member with this Student ID already exists.", "danger")
            return redirect(url_for("members.add_member"))

        # Upload passport photo
        passport = request.files.get("passport")



        filename = "default.png"

        if passport and passport.filename:
            import uuid

            filename = f"{uuid.uuid4().hex}_{secure_filename(passport.filename)}"

            passport.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        last_member = Member.query.order_by(Member.id.desc()).first()

        if last_member:
            next_id = last_member.id + 1
        else:
            next_id = 1

        esa_id = f"ESA-2026-{next_id:04d}"


        # Login credentials
        username = student_id

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if not password or not confirm_password:
            flash("Password and Confirm Password are required.", "danger")
            return redirect(url_for("members.add_member"))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("members.add_member"))

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            flash(
                "A user account with this Student ID already exists.",
                "danger"
            )
            return redirect(url_for("members.add_member"))

        programme = Programme.query.get(
            request.form.get("programme")
        )

        department = Department.query.get(
            request.form.get("department")
        )

        member = Member(

            esa_id=esa_id,

            student_id=request.form["student_id"],

            first_name=request.form["first_name"],

            last_name=request.form["last_name"],

            gender=request.form.get("gender"),



            phone=request.form.get("phone"),

            email=request.form.get("email"),
            registration_status="Approved",

            status="Active",

            approved_by=current_user.id,

            approved_at=datetime.utcnow(),
            class_group_id=request.form.get("class_group_id") or None,
            faculty_id=request.form.get("faculty_id") or None,

            programme=programme.programme_name if programme else "",

            department=department.department_name if department else "",

            level=request.form.get("level"),

            session=request.form.get("session"),

            academic_year=request.form.get("academic_year"),



        )

        # Check if a user already exists

        email = request.form.get("email", "").strip()

        if email == "":
            email = None

        if email:
            existing_email = User.query.filter_by(
                email=email
            ).first()

            if existing_email:
                flash(
                    "A user account with this email already exists.",
                    "danger"
                )
                return redirect(url_for("members.add_member"))
            # Create the login account
            user = User(
                full_name=f"{request.form['first_name']} {request.form['last_name']}",
                username=username,
                email=email,
                role="Member",
                must_change_password=True
            )

            user.set_password(password)

            db.session.add(user)

            # Save user first so it gets an ID
            db.session.flush()

            # Link Member to User
            member.user_id = user.id
            # Link Member to User
        member.user_id = user.id

        db.session.add(member)

        db.session.commit()


        log_activity(
            module="Members",
            action="Added Member",
            description=member.esa_id
        )
        return redirect(url_for("members.members"))

    programmes = Programme.query.order_by(
        Programme.programme_name
    ).all()

    faculties = Faculty.query.order_by(
        Faculty.faculty_name
    ).all()
    class_groups = ClassGroup.query.order_by(ClassGroup.name).all()
    academic_years = [
        f"{year}/{year + 1}"
        for year in range(2023, 2051)
    ]
    return render_template(
        "members/add.html",
        programmes=programmes,
        faculties=faculties,
        class_groups=class_groups,
        academic_years=academic_years,
        selected_class_group=selected_class_group,
        selected_group=selected_group
    )

@members_bp.route("/members/recent")
@login_required
@roles_required("Administrator", "General Secretary")
def recent_members():

    recent_members = Member.query.order_by(
        Member.date_registered.desc()
    ).limit(20).all()

    return render_template(
        "members/recent_members.html",
        recent_members=recent_members
    )
# ==========================================F
# Add Member
# ==========================================
@members_bp.route("/members/programmes")
@login_required
@roles_required("Administrator", "General Secretary")
def members_by_programme():

    programmes = Programme.query.order_by(
        Programme.programme_name
    ).all()

    data = []

    for programme in programmes:

        levels = []

        for level in ["100", "200", "300", "400"]:

            count = Member.query.filter_by(
                programme=programme.programme_name,
                level=level
            ).count()

            levels.append({
                "level": level,
                "count": count
            })

        total = Member.query.filter_by(
            programme=programme.programme_name
        ).count()

        data.append({
            "programme": programme.programme_name,
            "total": total,
            "levels": levels
        })

    return render_template(
        "members/programme_view.html",
        data=data
    )
# ==========================================
# Members by Programme and Level
# ==========================================
@members_bp.route("/members/programme/<programme>/<level>")
@login_required
@roles_required("Administrator", "General Secretary")
def programme_level_members(programme, level):

    members = Member.query.filter_by(
        programme=programme,
        level=level
    ).all()

    return render_template(
        "members/programme_level.html",
        members=members,
        programme=programme,
        level=level
    )
# ==========================================
# Member Profile
# ==========================================
    # ==========================================
    # Member Profile
    # ==========================================
@members_bp.route("/members/<int:member_id>")
@login_required
@roles_required("Administrator", "General Secretary")
def member_profile(member_id):

    member = Member.query.get_or_404(member_id)
    user = member.user
    # Payment Statistics
    total_paid = db.session.query(
        db.func.sum(Payment.amount)
    ).filter(
        Payment.member_id == member.id
    ).scalar() or 0

    payment_count = Payment.query.filter_by(
        member_id=member.id
    ).count()

    recent_payments = Payment.query.filter_by(
        member_id=member.id
    ).order_by(
        Payment.date_paid.desc()
    ).limit(5).all()

    # Attendance Statistics
    attendance_count = Attendance.query.filter_by(
        member_id=member.id
    ).count()

    return render_template(
        "members/profile.html",
        member=member,
        total_paid=total_paid,
        payment_count=payment_count,
        attendance_count=attendance_count,
        recent_payments=recent_payments
    )
# ==========================================
# Edit Member
# ==========================================
@members_bp.route("/members/edit/<int:member_id>", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def edit_member(member_id):


    member = Member.query.get_or_404(member_id)

    if request.method == "POST":

        # Convert Date of Birth
        dob = request.form.get("date_of_birth")

        if dob:
            dob = datetime.strptime(dob, "%Y-%m-%d").date()
        else:
            dob = None

        member.student_id = request.form["student_id"]
        member.first_name = request.form["first_name"]
        member.last_name = request.form["last_name"]

        member.gender = request.form.get("gender")
        member.date_of_birth = dob

        member.phone = request.form.get("phone")
        member.email = request.form.get("email")


        member.faculty_id = request.form.get("faculty_id") or None
        programme = Programme.query.get(
            request.form.get("programme")
        )

        department = Department.query.get(
            request.form.get("department")
        )

        member.programme = programme.programme_name if programme else ""

        member.department = department.department_name if department else ""
        member.academic_year = request.form.get("academic_year")

        member.level = request.form.get("level")
        member.session = request.form.get("session")



        member.status = request.form.get("status")
        passport = request.files.get("passport")

        if passport and passport.filename:
            filename = secure_filename(passport.filename)

            passport.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            member.passport = filename
        db.session.commit()

        return redirect(
            url_for(
                "members.member_profile",
                member_id=member.id
            )
        )

    programmes = Programme.query.order_by(
        Programme.programme_name
    ).all()

    faculties = Faculty.query.order_by(
        Faculty.faculty_name
    ).all()
    selected_programme = Programme.query.filter_by(
        programme_name=member.programme
    ).first()
    return render_template(
        "members/edit.html",
        member=member,
        programmes=programmes,
        faculties=faculties,
        selected_programme=selected_programme
    )

@members_bp.route("/members/delete/<int:member_id>", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def delete_member(member_id):

    member = Member.query.get_or_404(member_id)

    if request.method == "POST":
        # Prevent an administrator from deleting their own account

        try:

            # Get the linked user account
            user = member.user

            # Prevent an administrator from deleting their own account
            from flask_login import current_user

            if user and user.id == current_user.id:
                flash(
                    "You cannot delete your own account while you are logged in.",
                    "danger"
                )
                return redirect(url_for("members.members"))

            # Delete candidate records
            Candidate.query.filter_by(
                member_id=member.id
            ).delete()

            # Delete announcements
            ClassAnnouncement.query.filter_by(
                created_by=member.id
            ).delete()

            # Remove member from any class group leadership role
            ClassGroup.query.filter_by(
                course_rep_id=member.id
            ).update(
                {"course_rep_id": None},
                synchronize_session=False
            )

            ClassGroup.query.filter_by(
                assistant_course_rep_id=member.id
            ).update(
                {"assistant_course_rep_id": None},
                synchronize_session=False
            )



            # Delete approved voting index
            MemberIndex.query.filter_by(
                student_id=member.student_id
            ).delete()
            # Delete course representative record
            CourseRep.query.filter_by(
                member_id=member.id
            ).delete()
            # Delete login account
            if user:
                db.session.delete(user)

            # Delete member
            db.session.delete(member)

            db.session.commit()

            flash(
                "Member deleted successfully.",
                "success"
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"Unable to delete member: {str(e)}",
                "danger"
            )


        return redirect(
            url_for("members.members")
        )

    return render_template(
        "members/delete.html",
        member=member
    )
# Membership Card
# ==========================================
@members_bp.route("/members/card/<int:member_id>")
@login_required
@roles_required("Administrator", "General Secretary")
def member_card(member_id):

    member = Member.query.get_or_404(member_id)

    return render_template(
        "members/card.html",
        member=member
    )
# ==========================================
# Printable Membership Card
# ==========================================
@members_bp.route("/members/card/<int:member_id>/print")
@login_required
@roles_required("Administrator", "General Secretary")
def member_card_print(member_id):

    member = Member.query.get_or_404(member_id)

    return render_template(
        "members/card_print.html",
        member=member
    )

@members_bp.route("/members/card/<int:member_id>/pdf")
@login_required
@roles_required("Administrator", "General Secretary")
def download_member_card_pdf(member_id):
    member = Member.query.get_or_404(member_id)

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setTitle("ESA Membership Card")

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(60, 800, "EXECUTIVE STUDENT ASSOCIATION")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(60, 775, "UNIVERSITY OF SKILLS TRAINING AND ENTREPRENEURIAL DEVELOPMENT")

    pdf.drawString(60, 730, f"Member: {member.first_name} {member.last_name}")
    pdf.drawString(60, 710, f"ESA ID: {member.esa_id}")
    pdf.drawString(60, 690, f"Student ID: {member.student_id}")
    pdf.drawString(60, 670, f"Programme: {member.programme}")
    pdf.drawString(60, 650, f"Level: {member.level}")
    pdf.drawString(60, 630, f"Session: {member.session}")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    response = make_response(buffer.read())

    response.headers["Content-Type"] = "application/pdf"

    response.headers["Content-Disposition"] = (
        f'attachment; filename="{member.esa_id}-ID-Card.pdf"'
    )

    return response

# ==========================================
# Reset Member Password
# ==========================================
@members_bp.route("/members/<int:member_id>/reset-password", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def reset_member_password(member_id):

    member = Member.query.get_or_404(member_id)

    if not member.user:
        flash("This member does not have a login account.", "warning")
        return redirect(url_for("members.members"))

    if request.method == "POST":

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not password or not confirm_password:
            flash("Please enter and confirm the password.", "danger")
            return redirect(
                url_for("members.reset_member_password", member_id=member.id)
            )

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(
                url_for("members.reset_member_password", member_id=member.id)
            )

        member.user.set_password(password)
        member.user.must_change_password = True

        db.session.commit()

        log_activity(
            module="Members",
            action="Reset Password",
            description=member.esa_id
        )

        flash("Password reset successfully.", "success")

        return redirect(url_for("members.members"))

    return render_template(
        "members/reset_password.html",
        member=member
    )
# Get Programmes by Faculty (AJAX)
# ==========================================


@members_bp.route("/get_programmes/<int:faculty_id>")
@login_required
@roles_required("Administrator", "General Secretary")
def get_programmes(faculty_id):

    programmes = Programme.query.filter_by(
        faculty_id=faculty_id
    ).order_by(
        Programme.programme_name
    ).all()

    return jsonify([
        {
            "id": p.id,
            "name": p.programme_name
        }
        for p in programmes
    ])
@members_bp.route("/get_departments/<int:programme_id>")
@login_required
@roles_required("Administrator", "General Secretary")
def get_departments(programme_id):

    departments = Department.query.filter_by(
        programme_id=programme_id,
        status="Active"
    ).order_by(
        Department.department_name
    ).all()

    return jsonify([
        {
            "id": d.id,
            "name": d.department_name
        }
        for d in departments
    ])
# ==========================================
# Get Academic Class (AJAX)
# ==========================================
@members_bp.route("/get_class_group")
@login_required
def get_class_group():

    programme_id = request.args.get("programme", type=int)
    level = request.args.get("level")
    session = request.args.get("session")

    if not programme_id or not level or not session:
        return jsonify({})

    group = ClassGroup.query.filter_by(
        programme_id=programme_id,
        level=level,
        session=session,
        status="Active"
    ).first()

    if group:
        return jsonify({
            "id": group.id,
            "name": group.name
        })

    return jsonify({})