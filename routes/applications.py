from flask import Blueprint, render_template
from flask_login import login_required

from utils.auth import roles_required

from models.member_application import MemberApplication


applications_bp = Blueprint(
    "applications",
    __name__,
    url_prefix="/applications"
)


@applications_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def dashboard():

    applications = MemberApplication.query.order_by(
        MemberApplication.date_applied.desc()
    ).all()

    return render_template(
        "applications/dashboard.html",
        applications=applications
    )
from models.faculty import Faculty


@applications_bp.route("/apply")
def apply():

    faculties = Faculty.query.order_by(
        Faculty.faculty_name
    ).all()

    return render_template(
        "applications/apply.html",
        faculties=faculties
    )