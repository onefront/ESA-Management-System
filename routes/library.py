import os

from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from extensions import db

from models.library import Library

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)



from models.programme import Programme
from flask_login import login_required

library_bp = Blueprint(
    "library",
    __name__,
    url_prefix="/library"
)
UPLOAD_FOLDER = "static/uploads/library"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

@library_bp.route("/")
@login_required
def dashboard():

    return render_template(
        "library/dashboard.html"
    )





@library_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_resource():

    programmes = Programme.query.order_by(
        Programme.programme_name
    ).all()

    if request.method == "POST":

        pdf = request.files.get("pdf_file")

        # Make sure a file was selected
        if not pdf or pdf.filename == "":
            flash(
                "Please select a PDF file.",
                "danger"
            )
            return redirect(url_for("library.upload_resource"))

        # Only allow PDF files
        if not pdf.filename.lower().endswith(".pdf"):
            flash(
                "Only PDF files are allowed.",
                "danger"
            )
            return redirect(url_for("library.upload_resource"))


        if not pdf or pdf.filename == "":
            flash(
                "Please select a PDF file.",
                "danger"
            )
            return redirect(
                url_for("library.upload_resource")
            )

        filename = secure_filename(pdf.filename)

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        pdf.save(filepath)
        # Maximum file size = 20 MB
        max_size = 20 * 1024 * 1024

        if os.path.getsize(filepath) > max_size:
            os.remove(filepath)

            flash(
                "File is larger than 20 MB.",
                "danger"
            )

            return redirect(
                url_for("library.upload_resource")
            )
        # Read form values
        programme_id = request.form.get("programme_id")
        level = request.form.get("level")
        course_code = request.form.get("course_code")
        course_title = request.form.get("course_title")
        academic_year = request.form.get("academic_year")
        semester = request.form.get("semester")
        exam_type = request.form.get("exam_type")

        # Check for duplicate
        existing = Library.query.filter_by(
            programme_id=programme_id,
            level=level,
            course_code=course_code,
            academic_year=academic_year,
            semester=semester,
            exam_type=exam_type
        ).first()

        if existing:

            if os.path.exists(filepath):
                os.remove(filepath)

            flash(
                "This academic resource already exists.",
                "warning"
            )

            return redirect(
                url_for("library.upload_resource")
            )

        resource = Library(

            title=f"{course_code} - {course_title}",

            programme_id=programme_id,

            level=level,

            course_code=course_code,

            course_title=course_title,

            academic_year=academic_year,

            semester=semester,

            exam_type=exam_type,

            file_name=filename,

            file_path=filepath,

            file_size=os.path.getsize(filepath),

            uploaded_by=current_user.id
        )

        db.session.add(resource)
        db.session.commit()

        flash(
            "Academic resource added successfully.",
            "success"
        )

        return redirect(
            url_for("library.upload_resource")
        )

    return render_template(
        "library/upload.html",
        programmes=programmes
    )


@library_bp.route("/view/<int:id>")
@login_required
def view_resource(id):

    resource = Library.query.get_or_404(id)

    resource.downloads += 1

    db.session.commit()

    return send_file(
        resource.file_path,
        mimetype="application/pdf"
    )


@library_bp.route("/student")
@login_required
def student_library():

    programmes = Programme.query.order_by(
        Programme.programme_name
    ).all()

    resources = Library.query
    search = request.args.get("search")
    programme = request.args.get("programme")
    level = request.args.get("level")
    semester = request.args.get("semester")
    exam = request.args.get("exam")

    if programme:
        resources = resources.filter(
            Library.programme_id == programme
        )

    if level:
        resources = resources.filter(
            Library.level == level
        )

    if semester:
        resources = resources.filter(
            Library.semester == semester
        )

    if exam:
        resources = resources.filter(
            Library.exam_type == exam
        )
    if search:
        resources = resources.filter(

            db.or_(

                Library.course_code.ilike(f"%{search}%"),

                Library.course_title.ilike(f"%{search}%")

            )

        )
    resources = resources.order_by(
        Library.course_code
    ).all()

    total_resources = Library.query.count()

    total_programmes = Programme.query.count()

    total_downloads = db.session.query(
        db.func.sum(Library.downloads)
    ).scalar() or 0

    latest_upload = Library.query.order_by(
        Library.created_at.desc()
    ).first()

    return render_template(
        "library/student.html",

        programmes=programmes,

        resources=resources,

        total_resources=total_resources,

        total_programmes=total_programmes,

        total_downloads=total_downloads,

        latest_upload=latest_upload
    )



@library_bp.route("/manage")
@login_required
def manage_resources():

    search = request.args.get("search", "")

    resources = Library.query

    if search:

        resources = resources.filter(

            db.or_(

                Library.course_code.ilike(f"%{search}%"),

                Library.course_title.ilike(f"%{search}%")

            )

        )

    resources = resources.order_by(
        Library.created_at.desc()
    ).all()

    return render_template(
        "library/manage.html",
        resources=resources,
        search=search
    )


@library_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_resource(id):

    resource = Library.query.get_or_404(id)

    programmes = Programme.query.order_by(
        Programme.programme_name
    ).all()

    if request.method == "POST":

        resource.programme_id = request.form.get("programme_id")
        resource.level = request.form.get("level")
        resource.course_code = request.form.get("course_code")
        resource.course_title = request.form.get("course_title")
        resource.academic_year = request.form.get("academic_year")
        resource.semester = request.form.get("semester")
        resource.exam_type = request.form.get("exam_type")

        db.session.commit()

        flash(
            "Academic resource updated successfully.",
            "success"
        )

        return redirect(
            url_for("library.manage_resources")
        )

    return render_template(
        "library/edit.html",
        resource=resource,
        programmes=programmes
    )


@library_bp.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_resource(id):

    resource = Library.query.get_or_404(id)

    if request.method == "POST":

        # Delete the PDF file
        if resource.file_path and os.path.exists(resource.file_path):
            os.remove(resource.file_path)

        db.session.delete(resource)
        db.session.commit()

        flash(
            "Academic resource deleted successfully.",
            "success"
        )

        return redirect(
            url_for("library.manage_resources")
        )

    return render_template(
        "library/delete.html",
        resource=resource
    )