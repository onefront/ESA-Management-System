from flask import Blueprint, render_template
from flask import send_file
from openpyxl import Workbook
from io import BytesIO
from models.member import Member
from models.payment import Payment
from models.attendance import Attendance
from models.event import Event

from extensions import db

reports_bp = Blueprint("reports", __name__)


# ==========================================
# Reports Dashboard
# ==========================================
@reports_bp.route("/reports")
def reports():

    total_members = Member.query.count()

    total_payments = Payment.query.count()

    total_revenue = db.session.query(
        db.func.sum(Payment.amount)
    ).scalar() or 0

    total_events = Event.query.count()

    total_attendance = Attendance.query.count()

    return render_template(
        "reports/index.html",
        total_members=total_members,
        total_payments=total_payments,
        total_revenue=total_revenue,
        total_events=total_events,
        total_attendance=total_attendance
    )
# ==========================================
# Members Report
# ==========================================
@reports_bp.route("/reports/members")
def members_report():

    members = Member.query.order_by(
        Member.first_name
    ).all()

    return render_template(
        "reports/members_report.html",
        members=members
    )
# ==========================================
# Export Members Report to Excel
# ==========================================
@reports_bp.route("/reports/members/excel")
def export_members_excel():

    wb = Workbook()
    ws = wb.active

    ws.title = "ESA Members"

    # Headings
    ws.append([
        "ESA ID",
        "Student ID",
        "First Name",
        "Last Name",
        "Programme",
        "Level",
        "Session"
    ])

    members = Member.query.order_by(
        Member.first_name
    ).all()

    for member in members:

        ws.append([
            member.esa_id,
            member.student_id,
            member.first_name,
            member.last_name,
            member.programme,
            member.level,
            member.session
        ])

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="ESA_Members_Report.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
# ==========================================
# Payments Report
# ==========================================
@reports_bp.route("/reports/payments")
def payments_report():

    payments = Payment.query.order_by(
        Payment.date_paid.desc()
    ).all()

    total_payments = Payment.query.count()

    total_revenue = db.session.query(
        db.func.sum(Payment.amount)
    ).scalar() or 0

    return render_template(
        "reports/payments_report.html",
        payments=payments,
        total_payments=total_payments,
        total_revenue=total_revenue
    )
# ==========================================
# Attendance Report
# ==========================================
@reports_bp.route("/reports/attendance")
def attendance_report():

    attendance = Attendance.query.order_by(
        Attendance.attendance_date.desc()
    ).all()

    total_records = Attendance.query.count()

    total_present = Attendance.query.filter_by(
        status="Present"
    ).count()

    total_absent = Attendance.query.filter_by(
        status="Absent"
    ).count()

    return render_template(
        "reports/attendance_report.html",
        attendance=attendance,
        total_records=total_records,
        total_present=total_present,
        total_absent=total_absent
    )
# ==========================================
# Events Report
# ==========================================
@reports_bp.route("/reports/events")
def events_report():

    events = Event.query.order_by(
        Event.event_date.desc()
    ).all()

    total_events = Event.query.count()

    return render_template(
        "reports/events_report.html",
        events=events,
        total_events=total_events
    )