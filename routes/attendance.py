from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from extensions import db
from flask_login import login_required
from utils.auth import admin_required
from models.attendance import Attendance
from models.member import Member
from models.event import Event

attendance_bp = Blueprint("attendance", __name__)


# ==========================================
# Attendance List
# ==========================================
@attendance_bp.route("/attendance")
@login_required
@admin_required
def attendance():

    attendance_records = Attendance.query.order_by(
        Attendance.attendance_date.desc()
    ).all()

    return render_template(
        "attendance/index.html",
        attendance_records=attendance_records
    )


# ==========================================
# Mark Attendance
# ==========================================
@attendance_bp.route("/attendance/add",
                     methods=["GET", "POST"])
@login_required
@admin_required
def add_attendance():

    members = Member.query.order_by(
        Member.first_name
    ).all()

    events = Event.query.order_by(
        Event.event_date.desc()
    ).all()

    if request.method == "POST":

        last = Attendance.query.order_by(
            Attendance.id.desc()
        ).first()

        next_id = 1 if last is None else last.id + 1

        attendance_code = f"ATT-{next_id:04d}"

        attendance = Attendance(

            attendance_code=attendance_code,

            member_id=request.form["member_id"],

            event_id=request.form["event_id"],

            status=request.form["status"]

        )

        db.session.add(attendance)
        db.session.commit()

        return redirect(
            url_for("attendance.attendance")
        )

    return render_template(
        "attendance/add.html",
        members=members,
        events=events
    )
# ==========================================
# Bulk Attendance
# ==========================================
@attendance_bp.route("/attendance/event", methods=["GET", "POST"])
@login_required
@admin_required
def attendance_by_event():

    events = Event.query.order_by(
        Event.event_date.desc()
    ).all()

    if request.method == "POST":

        # Save attendance
        if request.form.get("save_attendance") == "1":

            event_id = request.form.get("event_id")

            members = Member.query.order_by(
                Member.first_name
            ).all()

            for member in members:

                status = request.form.get(f"attendance_{member.id}")

                if not status:
                    continue

                # Prevent duplicate attendance
                existing = Attendance.query.filter_by(
                    member_id=member.id,
                    event_id=event_id
                ).first()

                if existing:
                    continue

                last = Attendance.query.order_by(
                    Attendance.id.desc()
                ).first()

                next_id = 1 if last is None else last.id + 1

                attendance = Attendance(
                    attendance_code=f"ATT-{next_id:04d}",
                    member_id=member.id,
                    event_id=event_id,
                    status=status
                )

                db.session.add(attendance)

            db.session.commit()

            return redirect(url_for("attendance.attendance"))

        # Load members for selected event
        event_id = request.form["event_id"]

        members = Member.query.order_by(
            Member.first_name
        ).all()

        return render_template(
            "attendance/bulk.html",
            members=members,
            events=events,
            selected_event=event_id
        )

    return render_template(
        "attendance/bulk.html",
        events=events,
        members=[]
    )