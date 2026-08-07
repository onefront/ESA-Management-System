from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from extensions import db
from sqlalchemy import or_
from werkzeug.security import generate_password_hash
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from utils.qrcode_generator import generate_member_qrcode
from flask import current_app
from werkzeug.utils import secure_filename
import os
import uuid
from utils.audit import log_activity
from models.department import Department
from models.faculty import Faculty
from models.member_index import MemberIndex
from models.programme import Programme
from models.class_group import ClassGroup
from sqlalchemy import or_
from models.member import Member
from models.user import User
from datetime import datetime, timedelta
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"].strip()

        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and user.check_password(password):

            if not user.is_active:

                flash(
                    "Your account has been disabled.",
                    "danger"
                )

                return redirect(url_for("auth.login"))

            login_user(user)

            log_activity(
                module="Authentication",
                action="LOGIN",
                description=f"{user.full_name} logged into the system."
            )

            if user.must_change_password:
                return redirect(url_for("auth.change_password"))

            if user.role == "Member":
                return redirect(url_for("member_portal.dashboard"))

            return redirect(url_for("dashboard.dashboard"))

        flash(
            "Invalid Student ID or Password.",
            "danger"
        )

        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")
@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":

        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not current_user.check_password(current_password):

            flash(
                "Current password is incorrect.",
                "danger"
            )

            return redirect(url_for("auth.change_password"))

        if new_password != confirm_password:

            flash(
                "New passwords do not match.",
                "danger"
            )

            return redirect(url_for("auth.change_password"))

        if len(new_password) < 8:

            flash(
                "Password must be at least 8 characters.",
                "danger"
            )

            return redirect(url_for("auth.change_password"))

        current_user.set_password(new_password)

        current_user.must_change_password = False

        db.session.commit()

        log_activity(
            module="Authentication",
            action="PASSWORD CHANGE",
            description=f"{current_user.full_name} changed password."
        )



        flash(
            "Password changed successfully.",
            "success"
        )

        if current_user.role == "Member":

            return redirect(
                url_for("member_portal.dashboard")
            )

        return redirect(
            url_for("dashboard.dashboard")
        )

    return render_template(
        "auth/change_password.html"
    )
@auth_bp.route("/logout")
@login_required
def logout():

    log_activity(
        module="Authentication",
        action="LOGOUT",
        description=f"{current_user.full_name} logged out."
    )

    logout_user()

    return redirect(url_for("auth.login"))



@auth_bp.route("/verify-index", methods=["GET", "POST"])
def verify_index():

    if request.method == "POST":
        print("===== VERIFY INDEX =====")
        print(request.form)

        student_id = request.form["student_id"].strip().upper()

        print("Student ID:", student_id)

        member_index = MemberIndex.query.filter_by(
            student_id=student_id
        ).first()

        print("Member Index:", member_index)
        student_id = request.form["student_id"].strip().upper()

        member_index = MemberIndex.query.filter_by(
            student_id=student_id
        ).first()

        if not member_index:

            flash(
                "Your Student Index Number is not registered with ESA.",
                "danger"
            )

            return redirect(
                url_for("auth.verify_index")
            )

        if member_index.used:

            flash(
                "An account has already been created using this Student Index Number.",
                "warning"
            )

            return redirect(
                url_for("auth.verify_index")
            )

        return redirect(
            url_for(
                "auth.register",
                student_id=student_id
            )
        )

    return render_template(
        "auth/verify_index.html"
    )


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    student_id = request.args.get(
        "student_id",
        ""
    ).strip().upper()

    if not student_id:

        flash(
            "Please verify your Student Index Number first.",
            "warning"
        )

        return redirect(
            url_for("auth.verify_index")
        )

    if request.method == "POST":

        student_id = request.form["student_id"].strip().upper()
        username = request.form["username"].strip()


        email = request.form.get(
            "email",
            ""
        ).strip().lower()
        if len(username) < 4:
            flash(
                "Username must be at least 4 characters long.",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.register",
                    student_id=student_id
                )
            )

        if " " in username:
            flash(
                "Username cannot contain spaces.",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.register",
                    student_id=student_id
                )
            )
        if email == "":
            email = None

        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.register",
                    student_id=student_id
                )
            )

        if email:

            existing_user = User.query.filter(
                or_(
                    User.username == username,
                    User.email == email
                )
            ).first()

        else:

            existing_user = User.query.filter_by(
                username=username
            ).first()
        if existing_user:

            flash(
                "Student ID or Email already exists.",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.register",
                    student_id=student_id
                )
            )
        member_index = MemberIndex.query.filter_by(
            student_id=student_id
        ).first()

        if not member_index:
            flash(
                "Invalid Student Index Number.",
                "danger"
            )

            return redirect(
                url_for("auth.verify_index")
            )

        if member_index.used:
            flash(
                "This Student Index Number has already been used.",
                "danger"
            )

            return redirect(
                url_for("auth.verify_index")
            )
        user = User(

            full_name=f"{request.form['first_name']} {request.form['last_name']}",

            username=username,

            email=email,

            role="Member",

            is_active=True,

            must_change_password=False

        )

        user.set_password(password)

        db.session.add(user)

        db.session.flush()
        passport = request.files.get("passport")

        filename = None

        if passport and passport.filename:
            filename = f"{uuid.uuid4().hex}_{secure_filename(passport.filename)}"

            passport.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )
        faculty = Faculty.query.get(
            request.form["faculty_id"]
        )

        programme = Programme.query.get(
            request.form["programme"]
        )

        department = Department.query.get(
            request.form["department"]
        )

        department_name = (
            department.department_name
            if department else None
        )

        programme_name = (
            programme.programme_name
            if programme else None
        )

        class_group = None

        if programme:
            class_group = ClassGroup.query.filter_by(
                programme_id=programme.id,
                level=request.form["level"],
                session=request.form["session"],
                status="Active"
            ).first()

        last_member = Member.query.order_by(
            Member.id.desc()
        ).first()

        next_id = 1 if not last_member else last_member.id + 1

        esa_id = f"ESA-{datetime.now().year}-{next_id:04d}"

        member = Member(

            user_id=user.id,

            student_id=student_id,

            esa_id=esa_id,

            first_name=request.form["first_name"],

            last_name=request.form["last_name"],

            gender=request.form["gender"],

            phone=request.form["phone"],

            email=email,

            passport=filename,

            faculty_id=faculty.id if faculty else None,

            programme=programme_name,

            department=department_name,

            level=request.form["level"],

            session=request.form["session"],

            academic_year=request.form["academic_year"],
            guardian_name=request.form.get("guardian_name"),
            guardian_phone=request.form.get("guardian_phone"),

            class_group_id=class_group.id if class_group else None,

            status="Active",

            registration_status="Approved",

            approved_at=datetime.utcnow(),

            expiry_date=datetime.utcnow() + timedelta(days=365)

        )

        db.session.add(member)

        member_index.used = True
        member_index.used_by = user.id
        member_index.used_at = datetime.utcnow()

        db.session.commit()

        generate_member_qrcode(member.esa_id)

        login_user(user)

        flash(
            "Welcome to ESA CONNECT! Your account has been created successfully.",
            "success"
        )

        return redirect(
            url_for("member_portal.dashboard")
        )



    faculties = Faculty.query.order_by(
        Faculty.faculty_name
    ).all()

    class_groups = ClassGroup.query.order_by(
        ClassGroup.name
    ).all()

    academic_years = [
        f"{year}/{year + 1}"
        for year in range(2023, 2051)
    ]

    return render_template(
        "members/add.html",
        registration_mode=True,
        student_id=student_id,
        faculties=faculties,
        class_groups=class_groups,
        academic_years=academic_years,
        selected_group=None,
        selected_class_group=None
    )