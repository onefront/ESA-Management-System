from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from datetime import date
from models.timetable import Timetable
from flask import current_app
from werkzeug.utils import secure_filename
import uuid




from utils.qrcode_generator import generate_member_qrcode
from sqlalchemy import func
from flask import abort

from services.election_service import get_portfolio_results
from flask import send_file
import os
from flask_login import login_required, current_user
from models.election_settings import ElectionSettings
from models.portfolio import Portfolio
from models.candidate import Candidate
from models.vote import Vote
from extensions import db
from models.faculty import Faculty
from models.programme import Programme
from models.department import Department
from models.member import Member
from models.notice import Notice
from models.event import Event
from models.payment import Payment
from models.class_announcement import ClassAnnouncement
from models.election import Election
from models.system_settings import SystemSettings
member_portal_bp = Blueprint(
    "member_portal",
    __name__,
    url_prefix="/member"
)


def get_current_member():
    """
    Return the logged-in member record.
    """

    if not current_user.is_authenticated:
        return None

    return Member.query.filter_by(
        user_id=current_user.id
    ).first()
@member_portal_bp.route("/dashboard")
@login_required
def dashboard():

    member = get_current_member()

    if member is None:
        flash("Member profile not found.", "warning")
        return redirect(url_for("auth.logout"))

    latest_notices = (
        Notice.query
        .order_by(Notice.id.desc())
        .limit(5)
        .all()
    )

    class_announcements = (
        ClassAnnouncement.query
        .order_by(ClassAnnouncement.id.desc())
        .limit(5)
        .all()
    )

    settings = SystemSettings.query.first()

    today_exam = (
        Timetable.query
        .filter_by(
            programme=member.programme,
            level=member.level,
            session=member.session,
            academic_year=settings.current_academic_year,
            semester=settings.current_semester
        )
        .filter(
            Timetable.exam_date == date.today()
        )
        .order_by(
            Timetable.start_time.asc()
        )
        .first()
    )

    next_exam = (
        Timetable.query
        .filter_by(
            programme=member.programme,
            level=member.level,
            session=member.session,
            academic_year=settings.current_academic_year,
            semester=settings.current_semester
        )
        .filter(
            Timetable.exam_date >= date.today()
        )
        .order_by(
            Timetable.exam_date.asc(),
            Timetable.start_time.asc()
        )
        .first()
    )

    return render_template(
        "member_portal/dashboard_v2.html",
        member=member,
        latest_notices=latest_notices,
        class_announcements=class_announcements,
        today_exam=today_exam,
        next_exam=next_exam
    )



@member_portal_bp.route("/profile")
@login_required
def profile():

    member = get_current_member()

    if member is None:
        flash("Member profile not found.", "warning")
        return redirect(url_for("member_portal.dashboard"))

    return render_template(
        "member_portal/profile.html",
        member=member
    )



@member_portal_bp.route("/digital-id")
@login_required
def digital_id():

    member = get_current_member()

    if member is None:
        flash("Member profile not found.", "warning")
        return redirect(url_for("member_portal.dashboard"))

    qr_code = generate_member_qrcode(member.esa_id)

    return render_template(
        "member_portal/digital_id.html",
        member=member,
        qr_code=qr_code,
        debug_test="THIS_IS_THE_NEW_TEMPLATE"
    )

@member_portal_bp.route("/payments")
@login_required
def payments():

    member = get_current_member()

    if member is None:
        flash("Member profile not found.", "warning")
        return redirect(url_for("member_portal.dashboard"))

    payments = (
        Payment.query
        .filter_by(member_id=member.id)
        .order_by(Payment.date_paid.desc())
        .all()
    )

    total_paid = (
        db.session.query(func.coalesce(func.sum(Payment.amount), 0))
        .filter(
            Payment.member_id == member.id,
            Payment.status == "Approved"
        )
        .scalar()
    )

    approved_payments = sum(
        1 for p in payments if p.status == "Approved"
    )

    pending_payments = sum(
        1 for p in payments if p.status == "Pending"
    )

    rejected_payments = sum(
        1 for p in payments if p.status == "Rejected"
    )

    return render_template(
        "member_portal/payments.html",
        member=member,
        payments=payments,
        total_paid=total_paid,
        approved_payments=approved_payments,
        pending_payments=pending_payments,
        rejected_payments=rejected_payments
    )



@member_portal_bp.route("/payments/<int:payment_id>/receipt")
@login_required
def payment_receipt(payment_id):

    member = get_current_member()

    if member is None:
        flash("Member profile not found.", "warning")
        return redirect(url_for("member_portal.dashboard"))

    payment = Payment.query.filter_by(
        id=payment_id,
        member_id=member.id
    ).first()

    if payment is None:
        abort(404)

    return render_template(
        "member_portal/payment_receipt.html",
        member=member,
        payment=payment
    )


# ==========================================
# Member Announcements
# ==========================================
@member_portal_bp.route("/announcements")
@login_required
def announcements():

    notices = (
        Notice.query
        .filter_by(status="Published")
        .order_by(
            Notice.is_pinned.desc(),
            Notice.created_at.desc()
        )
        .all()
    )


    return render_template(
        "member_portal/announcements.html",
        notices=notices
    )


# ==========================================
# View Announcement
# ==========================================
@member_portal_bp.route("/announcements/<int:notice_id>")
@login_required
def notice_details(notice_id):

    notice = Notice.query.filter_by(
        id=notice_id,
        status="Published"
    ).first_or_404()

    return render_template(
        "member_portal/announcement_view.html",
        notice=notice
    )



@member_portal_bp.route("/events")
@login_required
def events():

    member = get_current_member()

    if member is None:
        flash("Member profile not found.", "warning")
        return redirect(url_for("member_portal.dashboard"))

    events = Event.query.order_by(Event.id.desc()).all()

    return render_template(
        "member_portal/events.html",
        member=member,
        events=events
    )



# ==========================================
# Member Event Details
# ==========================================
@member_portal_bp.route("/events/<int:event_id>")
@login_required
def event_details(event_id):

    member = get_current_member()

    if member is None:
        flash("Member profile not found.", "warning")
        return redirect(url_for("member_portal.dashboard"))

    event = Event.query.get_or_404(event_id)

    return render_template(
        "member_portal/event_view.html",
        member=member,
        event=event
    )


@member_portal_bp.route("/notifications")
@login_required
def notifications():

    member = get_current_member()

    if member is None:
        flash("Member profile not found.", "warning")
        return redirect(url_for("member_portal.dashboard"))

    notices = Notice.query.order_by(Notice.id.desc()).all()

    return render_template(
        "member_portal/notifications.html",
        member=member,
        notices=notices
    )

@member_portal_bp.route("/elections")
@login_required
def elections():

    member = get_current_member()

    if member is None:
        flash("Member profile not found.", "warning")
        return redirect(url_for("member_portal.dashboard"))

    settings = ElectionSettings.query.first()

    if not settings or not settings.active_election_id:

        return render_template(
            "member_portal/elections.html",
            member=member,
            election=None
        )

    election = Election.query.get(settings.active_election_id)
    portfolio_data = get_portfolio_results(election)
    return render_template(
        "member_portal/elections.html",
        member=member,
        election=election,
        settings=settings,
        portfolio_data=portfolio_data
    )

@member_portal_bp.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    member = get_current_member()

    if member is None:
        flash("Member profile not found.", "warning")
        return redirect(url_for("member_portal.dashboard"))

    if request.method == "POST":
        from werkzeug.utils import secure_filename
        from flask import current_app
        import os
        import uuid

        passport = request.files.get("passport")

        if passport and passport.filename:
            filename = f"{uuid.uuid4().hex}_{secure_filename(passport.filename)}"

            passport.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            member.passport = filename
        member.phone = request.form.get("phone")
        member.email = request.form.get("email")
        member.gender = request.form.get("gender")
        member.student_id = request.form.get("student_id")

        member.faculty_id = request.form.get("faculty_id") or None

        # Save the programme NAME instead of its ID
        programme_id = request.form.get("programme")

        if programme_id:
            programme = Programme.query.get(programme_id)
            if programme:
                member.programme = programme.programme_name

        department_id = request.form.get("department")

        if department_id:
            department = Department.query.get(department_id)
            if department:
                member.department = department.department_name
        member.level = request.form.get("level")
        member.session = request.form.get("session")
        member.academic_year = request.form.get("academic_year")

        member.guardian_name = request.form.get("guardian_name")
        member.guardian_phone = request.form.get("guardian_phone")

        db.session.commit()

        flash("Profile updated successfully.", "success")

        return redirect(url_for("member_portal.profile"))

    faculties = Faculty.query.order_by(Faculty.faculty_name).all()

    programmes = Programme.query.order_by(Programme.programme_name).all()

    faculties = Faculty.query.order_by(Faculty.faculty_name).all()
    programmes = Programme.query.order_by(Programme.programme_name).all()

    return render_template(
        "member_portal/edit_profile.html",
        member=member,
        faculties=faculties,
        programmes=programmes
    )




@member_portal_bp.route("/download-id")
@login_required
def download_id():

    member = get_current_member()

    if member is None:
        flash("Member profile not found.", "warning")
        return redirect(url_for("member_portal.dashboard"))

    flash(
        "ID download will be connected after we restore the PDF generator.",
        "info"
    )

    return redirect(url_for("member_portal.digital_id"))




@member_portal_bp.route("/verify/<esa_id>")
def verify_member(esa_id):

    member = Member.query.filter_by(esa_id=esa_id).first_or_404()

    return render_template(
        "member_portal/verify_member.html",
        member=member
    )

