from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, current_user
from extensions import db

from models.lecturer import Lecturer
from models.department import Department

from utils.auth import (
    roles_required,
    lecturer_directory_required
)
from utils.audit import log_activity


lecturers_bp = Blueprint(
    "lecturers",
    __name__,
    url_prefix="/lecturers"
)



# ==========================================
# Lecturer Directory
# ==========================================
@lecturers_bp.route("/")
@login_required
@lecturer_directory_required
def lecturers():

    search = request.args.get("search", "")

    query = Lecturer.query

    if search:

        query = query.filter(
            Lecturer.lecturer_name.contains(search)
        )

    lecturers = query.order_by(
        Lecturer.lecturer_name
    ).all()

    layout = (
        "member_portal/layout2.html"
        if current_user.role == "Member"
        else "layout_old.html"
    )

    print("USING LAYOUT:", layout)

    return render_template(
        "lecturers/index.html",
        lecturers=lecturers,
        search=search,
        layout_template=layout
    )


# ==========================================
# Add Lecturer
# ==========================================
@lecturers_bp.route("/add", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def add_lecturer():

    if request.method == "POST":

        lecturer = Lecturer(

            lecturer_name=request.form["lecturer_name"],

            phone_number=request.form["phone_number"],

            department=request.form["department"]

        )

        db.session.add(lecturer)
        db.session.commit()

        log_activity(
            module="Lecturer Directory",
            action="Added Lecturer",
            description=lecturer.lecturer_name
        )

        flash(
            "Lecturer added successfully.",
            "success"
        )

        return redirect(
            url_for("lecturers.lecturers")
        )
    departments = Department.query.order_by(
        Department.department_name
    ).all()

    return render_template(
        "lecturers/add.html",
        departments=departments
    )
# ==========================================
# Edit Lecturer
# ==========================================
@lecturers_bp.route("/edit/<int:lecturer_id>", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def edit_lecturer(lecturer_id):

    lecturer = Lecturer.query.get_or_404(lecturer_id)

    if request.method == "POST":

        lecturer.lecturer_name = request.form["lecturer_name"]
        lecturer.phone_number = request.form["phone_number"]
        lecturer.department = request.form["department"]

        db.session.commit()

        log_activity(
            module="Lecturer Directory",
            action="Updated Lecturer",
            description=lecturer.lecturer_name
        )

        flash(
            "Lecturer updated successfully.",
            "success"
        )

        return redirect(
            url_for("lecturers.lecturers")
        )

    departments = Department.query.order_by(
        Department.department_name
    ).all()



    return render_template(
        "lecturers/edit.html",
        lecturer=lecturer,
        departments=departments
    )
# ==========================================
# Delete Lecturer
# ==========================================
@lecturers_bp.route("/delete/<int:lecturer_id>", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def delete_lecturer(lecturer_id):

    lecturer = Lecturer.query.get_or_404(lecturer_id)

    if request.method == "POST":

        log_activity(
            module="Lecturer Directory",
            action="Deleted Lecturer",
            description=lecturer.lecturer_name
        )

        db.session.delete(lecturer)
        db.session.commit()

        flash(
            "Lecturer deleted successfully.",
            "success"
        )

        return redirect(
            url_for("lecturers.lecturers")
        )

    return render_template(
        "lecturers/delete.html",
        lecturer=lecturer
    )