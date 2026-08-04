from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for
)
from models.programme import Programme
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
import tempfile
from openpyxl import Workbook
from flask import send_file
import tempfile
from sqlalchemy import or_
from models.programme import Programme
import os
from werkzeug.utils import secure_filename
from services.timetable_importer import TimetableImporter
from models.timetable import Timetable
from extensions import db
from flask_login import login_required, current_user
from models.member import Member
from services.docx_timetable_importer import DocxTimetableImporter
import services.docx_timetable_importer as dti
from services.docx_timetable_importer import DocxTimetableImporter
from services.pdf_timetable_importer import PDFTimetableImporter
from services.university_timetable import UniversityTimetableImporter


timetable_bp = Blueprint(
    "timetable",
    __name__,
    url_prefix="/timetable"
)

UPLOAD_FOLDER = "uploads/timetables"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)










@timetable_bp.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files.get("file")

        if not file or file.filename == "":
            flash("Please choose a timetable file.", "danger")
            return redirect(url_for("timetable.upload"))

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(filepath)

        extension = os.path.splitext(filename)[1].lower()

        records = []

        if extension == ".pdf":

            importer = PDFTimetableImporter(filepath)
            records = importer.import_pdf()

        elif extension == ".xlsx":

            importer = UniversityTimetableImporter(filepath)
            records = importer.import_excel()

        elif extension == ".docx":

            importer = DocxTimetableImporter(filepath)
            records = importer.import_docx()

        else:

            flash(
                "Only PDF (.pdf), Excel (.xlsx) and Word (.docx) files are supported.",
                "warning"
            )
            return redirect(url_for("timetable.upload"))

        # Clear old timetable
        db.session.query(Timetable).delete()
        db.session.commit()

        for record in records:
            timetable = Timetable(

                day=record.get("day"),
                exam_date=record.get("exam_date"),
                start_time=record.get("start_time"),
                end_time=record.get("end_time"),

                programme=record.get("programme"),
                level=record.get("level"),

                course_code=record.get("course_code"),
                course_title=record.get("course_title"),

                venue=record.get("venue"),
                examiner=record.get("examiner"),
                session=record.get("session", "Weekend"),

                timetable_type=request.form.get(
                    "timetable_type",
                    "Examination"
                ),

                status="Active",

                academic_year=request.form.get(
                    "academic_year",
                    "2025/2026"
                ),

                semester=request.form.get(
                    "semester",
                    "Semester 2"
                )
            )
            if (
                    not record.get("programme")
                    or not record.get("exam_date")
                    or not record.get("start_time")
            ):
                continue
            db.session.add(timetable)

        db.session.commit()
        try:
            os.remove(filepath)
        except OSError:
            pass
        flash(
            f"{len(records)} timetable records imported successfully.",
            "success"
        )

        return redirect(
            url_for("timetable.records")
        )

    return render_template(
        "timetable/upload.html"
    )



@timetable_bp.route("/test-docx")
def test_docx():

    import os

    filepath = os.path.join(
        os.getcwd(),
        "uploads",
        "timetables",
        "sample.docx"
    )

    print("DOCX PATH:", filepath)
    print("EXISTS:", os.path.exists(filepath))

    importer = DocxTimetableImporter(filepath)

    output = importer.preview_tables()

    return f"<pre>{output}</pre>"




from sqlalchemy import or_

@timetable_bp.route("/records")
def records():
    search = request.args.get("search", "").strip()

    page = request.args.get("page", 1, type=int)

    per_page = 25
    programme = request.args.get("programme", "")
    level = request.args.get("level", "")
    day = request.args.get("day", "")

    query = Timetable.query

    if search:

        query = query.filter(

            or_(

                Timetable.programme.ilike(f"%{search}%"),
                Timetable.level.ilike(f"%{search}%"),
                Timetable.course_code.ilike(f"%{search}%"),
                Timetable.course_title.ilike(f"%{search}%"),
                Timetable.venue.ilike(f"%{search}%"),
                Timetable.examiner.ilike(f"%{search}%"),
                Timetable.day.ilike(f"%{search}%")

            )

        )

    if programme:
        query = query.filter(Timetable.programme == programme)

    if level:
        query = query.filter(Timetable.level == level)

    if day:
        query = query.filter(Timetable.day == day)

    pagination = query.order_by(
        Timetable.exam_date.asc(),
        Timetable.start_time.asc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    timetables = pagination.items
    programmes = db.session.query(
        Timetable.programme
    ).distinct().order_by(
        Timetable.programme
    ).all()

    levels = db.session.query(
        Timetable.level
    ).distinct().order_by(
        Timetable.level
    ).all()

    days = db.session.query(
        Timetable.day
    ).distinct().order_by(
        Timetable.day
    ).all()

    return render_template(

        "timetable/records.html",

        timetables=timetables,

        search=search,
        pagination=pagination,
        programme=programme,

        level=level,

        day=day,

        programmes=programmes,

        levels=levels,

        days=days

    )





@timetable_bp.route("/management")
@login_required
def management():

    return render_template(
        "timetable/management.html"
    )






@timetable_bp.route("/view/<int:timetable_id>")
def view_record(timetable_id):

    timetable = Timetable.query.get_or_404(timetable_id)

    return render_template(
        "timetable/view.html",
        timetable=timetable
    )



@timetable_bp.route("/edit/<int:timetable_id>", methods=["GET", "POST"])
def edit_record(timetable_id):

    timetable = Timetable.query.get_or_404(timetable_id)

    if request.method == "POST":

        timetable.day = request.form["day"]
        timetable.programme = request.form["programme"]
        timetable.level = request.form["level"]
        timetable.course_code = request.form["course_code"]
        timetable.course_title = request.form["course_title"]
        timetable.venue = request.form["venue"]
        timetable.examiner = request.form["examiner"]

        db.session.commit()

        flash(
            "Timetable updated successfully.",
            "success"
        )

        return redirect(
            url_for("timetable.records")
        )

    return render_template(
        "timetable/edit.html",
        timetable=timetable
    )




@timetable_bp.route("/delete/<int:timetable_id>", methods=["GET", "POST"])
def delete_record(timetable_id):

    timetable = Timetable.query.get_or_404(timetable_id)

    if request.method == "POST":

        db.session.delete(timetable)
        db.session.commit()

        flash(
            "Timetable record deleted successfully.",
            "success"
        )

        return redirect(
            url_for("timetable.records")
        )

    return render_template(
        "timetable/delete.html",
        timetable=timetable
    )


@timetable_bp.route("/my", methods=["GET", "POST"])
@login_required
def my_timetable():

    member = Member.query.filter_by(
        user_id=current_user.id
    ).first()

    if not member:
        flash("Member profile not found.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    programme = Programme.query.filter_by(
        programme_name=member.programme
    ).first()

    programme_code = (
        programme.programme_code
        if programme
        else member.programme
    )

    # Academic Year & Semester options
    academic_years = (
        db.session.query(Timetable.academic_year)
        .distinct()
        .order_by(Timetable.academic_year.desc())
        .all()
    )

    # Always show both semesters
    semesters = [
        ("First Semester",),
        ("Second Semester",)
    ]

    selected_year = request.args.get("academic_year")
    selected_semester = request.args.get("semester")

    timetables = []

    if selected_year and selected_semester:

        timetables = (
            Timetable.query
            .filter_by(
                programme=programme_code,
                level=member.level,
                session=member.session,
                academic_year=selected_year,
                semester=selected_semester
            )
            .order_by(
                Timetable.exam_date.asc(),
                Timetable.start_time.asc()
            )
            .all()
        )

    return render_template(
        "timetable/my_timetable.html",
        member=member,
        timetables=timetables,
        academic_years=academic_years,
        semesters=semesters,
        selected_year=selected_year,
        selected_semester=selected_semester
    )



@timetable_bp.route("/print")
@login_required
def print_timetable():

    timetables = (
        Timetable.query
        .order_by(
            Timetable.exam_date.asc(),
            Timetable.start_time.asc()
        )
        .all()
    )

    return render_template(
        "timetable/print.html",
        timetables=timetables
    )

@timetable_bp.route("/export/excel")
@login_required
def export_excel():

    wb = Workbook()
    ws = wb.active
    ws.title = "Timetable"

    ws.append([
        "Date",
        "Day",
        "Start Time",
        "End Time",
        "Programme",
        "Level",
        "Course Code",
        "Course Title",
        "Venue",
        "Examiner"
    ])

    records = Timetable.query.order_by(
        Timetable.exam_date.asc(),
        Timetable.start_time.asc()
    ).all()

    for row in records:

        ws.append([
            row.exam_date,
            row.day,
            row.start_time,
            row.end_time,
            row.programme,
            row.level,
            row.course_code,
            row.course_title,
            row.venue,
            row.examiner
        ])

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".xlsx"
    )

    wb.save(temp.name)

    return send_file(
        temp.name,
        as_attachment=True,
        download_name="ESA_Timetable.xlsx"
    )

@timetable_bp.route("/export/pdf")
@login_required
def export_pdf():

    records = (
        Timetable.query
        .order_by(
            Timetable.exam_date.asc(),
            Timetable.start_time.asc()
        )
        .all()
    )

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    doc = SimpleDocTemplate(
        temp.name,
        pagesize=(11*inch, 8.5*inch)
    )

    data = [[
        "Date",
        "Day",
        "Time",
        "Programme",
        "Level",
        "Course Code",
        "Course Title",
        "Venue"
    ]]

    for row in records:

        time = ""

        if row.start_time and row.end_time:
            time = f"{row.start_time.strftime('%I:%M %p')} - {row.end_time.strftime('%I:%M %p')}"

        data.append([

            str(row.exam_date),

            row.day,

            time,

            row.programme,

            row.level,

            row.course_code,

            row.course_title,

            row.venue

        ])

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("FONTSIZE",(0,0),(-1,-1),8),

        ("BOTTOMPADDING",(0,0),(-1,0),8),

    ]))

    doc.build([table])

    return send_file(

        temp.name,

        as_attachment=True,

        download_name="ESA_Timetable.pdf"

    )


@timetable_bp.route("/clear", methods=["GET", "POST"])
@login_required
def clear_timetable():

    if request.method == "POST":

        Timetable.query.delete()

        db.session.commit()

        flash(
            "All timetable records have been deleted.",
            "success"
        )

        return redirect(
            url_for("timetable.management")
        )

    return render_template(
        "timetable/clear.html"
    )