


from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from extensions import db
from models.faculty import Faculty
from flask_login import login_required
from utils.auth import admin_required
from models.programme import Programme
from utils.auth import admin_required

programmes_bp = Blueprint(
    "programmes",
    __name__,
    url_prefix="/programmes"
)


@programmes_bp.route("/")
@login_required
@admin_required
def programmes():

    search = request.args.get("search", "")

    query = Programme.query

    if search:

        query = query.filter(
            Programme.programme_name.ilike(f"%{search}%")
        )

    programmes = query.order_by(
        Programme.programme_name
    ).all()

    return render_template(
        "programmes/programmes.html",
        programmes=programmes,
        search=search
    )
@programmes_bp.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_programme():

    faculties = Faculty.query.order_by(
        Faculty.faculty_name
    ).all()

    if request.method == "POST":
        programme_name = request.form["programme_name"]

        programme_code = request.form["programme_code"].upper().strip()

        faculty_id = request.form["faculty_id"]

        status = request.form["status"]

        programme = Programme(
            programme_name=programme_name,
            programme_code=programme_code,
            faculty_id=faculty_id,
            status=status
        )

        db.session.add(programme)
        db.session.commit()

        flash("Programme added successfully.", "success")

        return redirect(url_for("programmes.programmes"))

    return render_template(
        "programmes/add.html",
        faculties=faculties)
@programmes_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_programme(id):

    programme = Programme.query.get_or_404(id)

    faculties = Faculty.query.order_by(
        Faculty.faculty_name
    ).all()

    if request.method == "POST":
        programme.programme_name = request.form["programme_name"]

        programme.programme_code = (
            request.form["programme_code"]
            .upper()
            .strip()
        )

        programme.faculty_id = request.form["faculty_id"]

        programme.status = request.form["status"]

        db.session.commit()

        flash("Programme updated successfully.", "success")

        return redirect(url_for("programmes.programmes"))

    return render_template(
        "programmes/edit.html",
        programme=programme,
        faculties=faculties
    )
@programmes_bp.route("/delete/<int:id>")
@login_required
@admin_required
def delete_programme(id):

    programme = Programme.query.get_or_404(id)

    if programme.departments:

        flash(
            "Cannot delete this programme because it has departments assigned to it.",
            "danger"
        )

        return redirect(url_for("programmes.programmes"))

    db.session.delete(programme)
    db.session.commit()

    flash("Programme deleted successfully.", "success")

    return redirect(url_for("programmes.programmes"))



