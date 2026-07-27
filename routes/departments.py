from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from flask_login import login_required
from models.programme import Programme

from extensions import db
from models.department import Department
from utils.auth import admin_required

departments_bp = Blueprint(
    "departments",
    __name__,
    url_prefix="/departments"
)


@departments_bp.route("/")
@login_required
@admin_required
def departments():

    search = request.args.get("search", "")

    query = Department.query

    if search:

        query = query.filter(
            Department.department_name.ilike(f"%{search}%")
        )

    departments = query.order_by(
        Department.department_name
    ).all()

    return render_template(
        "departments/departments.html",
        departments=departments,
        search=search
    )
@departments_bp.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_department():

    programmes = Programme.query.order_by(
        Programme.programme_name
    ).all()

    if request.method == "POST":

        department = Department(
            department_name=request.form["department_name"],
            programme_id=request.form["programme_id"],
            status=request.form["status"]
        )

        db.session.add(department)
        db.session.commit()

        flash("Department added successfully.", "success")

        return redirect(url_for("departments.departments"))

    return render_template(
        "departments/add.html",
        programmes=programmes
    )
@departments_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_department(id):

    department = Department.query.get_or_404(id)

    programmes = Programme.query.order_by(
        Programme.programme_name
    ).all()

    if request.method == "POST":

        department.department_name = request.form["department_name"]
        department.programme_id = request.form["programme_id"]
        department.status = request.form["status"]

        db.session.commit()

        flash("Department updated successfully.", "success")

        return redirect(url_for("departments.departments"))

    return render_template(
        "departments/edit.html",
        department=department,
        programmes=programmes
    )
@departments_bp.route("/delete/<int:id>")
@login_required
@admin_required
def delete_department(id):

    department = Department.query.get_or_404(id)

    db.session.delete(department)
    db.session.commit()

    flash("Department deleted successfully.", "success")

    return redirect(url_for("departments.departments"))

from flask import jsonify


@departments_bp.route("/get_departments/<int:programme_id>")
@login_required
def get_departments(programme_id):

    departments = Department.query.filter_by(
        programme_id=programme_id
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