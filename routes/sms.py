from flask import Blueprint
from flask import render_template

from flask_login import login_required
from flask import jsonify, request
from models.member import Member
from utils.auth import roles_required
from models.programme import Programme
from models.department import Department
from models.faculty import Faculty
sms_bp = Blueprint(
    "sms",
    __name__
)


@sms_bp.route("/sms")
@login_required
@roles_required(
    "Administrator",
    "CEO",
    "General Secretary"
)
def dashboard():

    return render_template(
        "sms/dashboard.html"
    )


@sms_bp.route("/sms/compose")
@login_required
@roles_required(
    "Administrator",
    "CEO",
    "General Secretary"
)
def compose():

    programme_list = [
        {
            "id": p.id,
            "programme_name": p.programme_name
        }
        for p in Programme.query
        .filter_by(status="Active")
        .order_by(Programme.programme_name)
        .all()
    ]

    department_list = [
        {
            "id": d.id,
            "department_name": d.department_name
        }
        for d in Department.query
        .filter_by(status="Active")
        .order_by(Department.department_name)
        .all()
    ]

    faculty_list = [
        {
            "id": f.id,
            "faculty_name": f.faculty_name
        }
        for f in Faculty.query
        .filter_by(status="Active")
        .order_by(Faculty.faculty_name)
        .all()
    ]

    return render_template(
        "sms/compose.html",
        programmes=programme_list,
        departments=department_list,
        faculties=faculty_list
    )


@sms_bp.route("/sms/search-members")
@login_required
@roles_required(
    "Administrator",
    "CEO",
    "General Secretary"
)
def search_members():

    search = request.args.get("q", "").strip()

    query = Member.query.filter_by(status="Active")

    if search:
        query = query.filter(
            (Member.first_name.ilike(f"%{search}%")) |
            (Member.last_name.ilike(f"%{search}%")) |
            (Member.student_id.ilike(f"%{search}%"))
        )

    members = (
        query
        .order_by(Member.first_name)
        .limit(100)
        .all()
    )

    return jsonify([
        {
            "id": m.id,
            "name": m.full_name,
            "student_id": m.student_id,
            "programme": m.programme,
            "department": m.department,
            "level": m.level
        }
        for m in members
    ])