from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from werkzeug.security import generate_password_hash

from extensions import db

from models.member_application import MemberApplication


registration_bp = Blueprint(
    "registration",
    __name__,
    url_prefix="/registration"
)


# =====================================
# Registration Form
# =====================================

@registration_bp.route("/")
def register():
    return redirect(url_for("auth.verify_index"))

    if request.method == "POST":

        # Check Student ID
        existing_student = MemberApplication.query.filter_by(
            student_id=request.form["student_id"]
        ).first()

        if existing_student:

            flash(
                "Student ID has already been registered.",
                "danger"
            )

            return redirect(
                url_for("registration.register")
            )

        # Check Email
        existing_email = MemberApplication.query.filter_by(
            email=request.form["email"]
        ).first()

        if existing_email:

            flash(
                "Email has already been used.",
                "danger"
            )

            return redirect(
                url_for("registration.register")
            )

        application = MemberApplication(

            student_id=request.form["student_id"],

            first_name=request.form["first_name"],

            last_name=request.form["last_name"],

            gender=request.form["gender"],

            phone=request.form["phone"],

            email=request.form["email"],

            faculty_id=request.form["faculty_id"],

            programme=request.form["programme"],

            department=request.form["department"],

            level=request.form["level"],

            session=request.form["session"],

            academic_year=request.form["academic_year"],

            password_hash=generate_password_hash(
                request.form["password"]
            )

        )

        db.session.add(application)

        db.session.commit()

        flash(
            "Application submitted successfully. Awaiting approval.",
            "success"
        )

        return redirect(
            url_for("registration.success")
        )

    return render_template(
        "registration/register.html"
    )


# =====================================
# Success Page
# =====================================

