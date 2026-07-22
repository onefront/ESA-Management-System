import os
from models.event import Event
from flask import abort
from flask import current_app
import qrcode
import uuid
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

# from utils.pdf_generator import generate_member_id_pdf
from models.class_announcement import ClassAnnouncement
from utils.qrcode_generator import generate_member_qrcode
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from extensions import db
from models.payment import Payment
from models.member import Member
from models.class_group import ClassGroup
from models.faculty import Faculty
from models.programme import Programme
from models.department import Department
from flask import Blueprint, render_template
from models.candidate import Candidate
from models.election import Election
from models.portfolio import Portfolio
from models.vote import Vote

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.notice import Notice
from models.slider import Slider
member_portal_bp = Blueprint(
    "member_portal",
    __name__,
    url_prefix="/member"
)






def generate_member_qr(member):

    url = f"http://127.0.0.1:5000/member/verify/{member.esa_id}"

    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=2
    )

    qr.add_data(url)
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    save_folder = os.path.join(
        current_app.static_folder,
        "qr_codes"
    )

    os.makedirs(save_folder, exist_ok=True)

    image.save(
        os.path.join(
            save_folder,
            f"{member.esa_id}.png"
        )
    )
@member_portal_bp.route("/elections")
@login_required
def elections():

    if current_user.role != "Member":
        return "Access Denied", 403

    member = Member.query.filter_by(
        user_id=current_user.id
    ).first()

    election = Election.query.filter_by(
        status="Active"
    ).first()

    if not election:

        return render_template(
            "member_portal/no_election.html"
        )

    portfolios = Portfolio.query.filter_by(
        status="Active"
    ).order_by(
        Portfolio.display_order
    ).all()

    voted = []

    for portfolio in portfolios:

        vote = Vote.query.filter_by(
            election_id=election.id,
            portfolio_id=portfolio.id,
            member_id=member.id
        ).first()

        if vote:
            voted.append(portfolio.id)

    return render_template(

        "member_portal/elections.html",

        election=election,

        portfolios=portfolios,

        voted=voted

    )

@member_portal_bp.route("/vote/<int:portfolio_id>")
@login_required
def vote_portfolio(portfolio_id):

    if current_user.role != "Member":
        return "Access Denied", 403

    member = Member.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    election = Election.query.filter_by(
        status="Active"
    ).first_or_404()

    portfolio = Portfolio.query.get_or_404(portfolio_id)

    candidates = Candidate.query.filter_by(
        election_id=election.id,
        portfolio_id=portfolio.id,
        status="Active"
    ).all()

    return render_template(
        "member_portal/vote_portfolio.html",
        election=election,
        portfolio=portfolio,
        candidates=candidates,
        member=member
    )
@member_portal_bp.route("/cast-vote/<int:candidate_id>", methods=["POST"])
@login_required
def cast_vote(candidate_id):

    member = Member.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    candidate = Candidate.query.get_or_404(candidate_id)

    election = candidate.election

    portfolio = candidate.portfolio

    # Prevent duplicate voting
    existing_vote = Vote.query.filter_by(
        election_id=election.id,
        portfolio_id=portfolio.id,
        member_id=member.id
    ).first()

    if existing_vote:

        flash(
            "You have already voted for this portfolio.",
            "warning"
        )

        return redirect(
            url_for(
                "member_portal.vote_portfolio",
                portfolio_id=portfolio.id
            )
        )

    vote = Vote(

        election_id=election.id,

        portfolio_id=portfolio.id,

        candidate_id=candidate.id,

        member_id=member.id

    )

    db.session.add(vote)

    db.session.commit()

    flash(
        "Your vote has been recorded successfully.",
        "success"
    )

    return redirect(
        url_for("member_portal.elections")
    )

@member_portal_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "Member":
        return "Access Denied", 403

    member = Member.query.filter_by(
        user_id=current_user.id
    ).first()

    upcoming_events = (
        Event.query
        .filter_by(status="Upcoming")
        .order_by(Event.event_date.asc())
        .limit(5)
        .all()
    )
    latest_notices = (
        Notice.query
        .filter_by(status="Published")
        .order_by(
            Notice.is_pinned.desc(),
            Notice.created_at.desc()
        )
        .limit(3)
        .all()
    )

    class_announcements = []

    if member and member.class_group:
        class_announcements = (
            ClassAnnouncement.query
            .filter_by(
                class_group_id=member.class_group.id,
                is_active=True
            )
            .order_by(
                ClassAnnouncement.is_pinned.desc(),
                ClassAnnouncement.created_at.desc()
            )
            .limit(3)
            .all()
        )
    slides = (
        Slider.query
        .filter_by(is_active=True)
        .order_by(Slider.display_order.asc())
        .all()
    )

    return render_template(
        "member_portal/dashboard_v2.html",
        member=member,
        upcoming_events=upcoming_events,
        latest_notices=latest_notices,
        class_announcements=class_announcements,
        slides=slides
    )


@member_portal_bp.route("/digital-id")
@login_required
def digital_id():

    if current_user.role != "Member":
        return "Access Denied", 403

    member = Member.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    qr_code = generate_member_qrcode(member.esa_id)

    return render_template(
        "member_portal/digital_id_v2.html",
        member=member,
        qr_code=qr_code
    )
@member_portal_bp.route("/download-id")
@login_required
def download_id():

    flash(
        "PDF download is temporarily unavailable.",
        "warning"
    )

    return redirect(
        url_for("member_portal.digital_id")
    )
@member_portal_bp.route("/verify/<esa_id>")
def verify_member(esa_id):

    member = Member.query.filter_by(
        esa_id=esa_id
    ).first()

    if not member:
        return render_template(
            "member_portal/member_not_found.html"
        ), 404

    return render_template(
        "member_portal/verify_member.html",
        member=member
    )
@member_portal_bp.route("/profile")
@login_required
def profile():

    if current_user.role != "Member":
        return "Access Denied", 403

    member = Member.query.filter_by(
        user_id=current_user.id
    ).first()

    if not member:
        return redirect(
            url_for("member_portal.complete_profile")
        )

    return render_template(
        "member_portal/profile.html",
        member=member
    )


@member_portal_bp.route("/complete-profile", methods=["GET", "POST"])
@login_required
def complete_profile():

    if current_user.role != "Member":
        return "Access Denied", 403

    # Check if the user already has a profile
    member = Member.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        # ----------------------------
        # Upload Passport
        # ----------------------------
        passport = request.files.get("passport")

        filename = "default.png"

        if passport and passport.filename:

            filename = (
                f"{uuid.uuid4().hex}_"
                f"{secure_filename(passport.filename)}"
            )

            passport.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        # ----------------------------
        # Generate ESA ID
        # ----------------------------
        last_member = Member.query.order_by(Member.id.desc()).first()

        next_id = 1 if last_member is None else last_member.id + 1

        esa_id = f"ESA-2026-{next_id:04d}"

        # ----------------------------
        # Get Programme
        # ----------------------------
        programme = None

        programme_id = request.form.get("programme")

        if programme_id:
            programme = Programme.query.get(int(programme_id))

        # ----------------------------
        # Get Department
        # ----------------------------
        department = None

        department_id = request.form.get("department")

        if department_id:
            department = Department.query.get(int(department_id))

        # ----------------------------
        # Split User Full Name
        # ----------------------------
        names = current_user.full_name.strip().split()

        first_name = names[0]

        last_name = " ".join(names[1:]) if len(names) > 1 else ""

        # ----------------------------
        # Save Member
        # ----------------------------
        member = Member(

            user_id=current_user.id,

            student_id=request.form.get("student_id"),

            esa_id=esa_id,

            first_name=first_name,

            last_name=last_name,

            gender=request.form.get("gender"),

            phone=request.form.get("phone"),

            email=current_user.email,

            passport=filename,

            faculty_id=request.form.get("faculty_id") or None,

            programme=programme.programme_name if programme else "",

            department=department.department_name if department else "",

            level=request.form.get("level"),

            session=request.form.get("session"),

            academic_year=request.form.get("academic_year"),

            status="Active"

        )
        db.session.add(member)

        # ---------------------------------
        # Automatically Assign Academic Class
        # ---------------------------------

        if programme:

            class_group = ClassGroup.query.filter_by(
                programme_id=programme.id,
                level=member.level,
                session=member.session,
                status="Active"
            ).first()

            if class_group:
                member.class_group_id = class_group.id

        db.session.commit()

        # ------------------------
        # Generate Member QR Code
        # ------------------------

        generate_member_qr(member)

        if member.class_group_id:

            flash(
                f"Welcome to ESA! Your profile has been completed successfully and you have been assigned to {class_group.name}.",
                "success"
            )

        else:

            flash(
                "Welcome to ESA! Your profile has been completed successfully. No matching Academic Class was found. Please contact the Administrator.",
                "warning"
            )
        return redirect(
            url_for("member_portal.edit_profile")
        )

    faculties = Faculty.query.order_by(
        Faculty.faculty_name
    ).all()

    programmes = Programme.query.order_by(
        Programme.programme_name
    ).all()

    return render_template(
        "member_portal/complete_profile.html",
        faculties=faculties,
        programmes=programmes
    )



@member_portal_bp.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    if current_user.role != "Member":
        return "Access Denied", 403

    member = Member.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        member.student_id = request.form.get("student_id")

        member.gender = request.form.get("gender")

        member.phone = request.form.get("phone")

        member.faculty_id = request.form.get("faculty_id") or None

        programme = None
        department = None

        programme_id = request.form.get("programme")
        department_id = request.form.get("department")

        if programme_id:
            programme = Programme.query.get(int(programme_id))

        if department_id:
            department = Department.query.get(int(department_id))

        member.programme = (
            programme.programme_name
            if programme else ""
        )

        member.department = (
            department.department_name
            if department else ""
        )

        member.level = request.form.get("level")

        member.session = request.form.get("session")

        member.academic_year = request.form.get("academic_year")

        passport = request.files.get("passport")

        if passport and passport.filename:

            filename = (
                f"{uuid.uuid4().hex}_"
                f"{secure_filename(passport.filename)}"
            )

            passport.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            member.passport = filename

        db.session.commit()

        generate_member_qr(member)

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(
            url_for("member_portal.edit_profile")
        )

    faculties = Faculty.query.order_by(
        Faculty.faculty_name
    ).all()

    programmes = Programme.query.order_by(
        Programme.programme_name
    ).all()

    return render_template(
        "member_portal/edit_profile.html",
        member=member,
        faculties=faculties,
        programmes=programmes
    )


@member_portal_bp.route("/payments")
@login_required
def payments():

    if current_user.role != "Member":
        return "Access Denied", 403

    member = Member.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    total_paid = db.session.query(
        db.func.sum(Payment.amount)
    ).filter(
        Payment.member_id == member.id
    ).scalar() or 0

    payment_count = Payment.query.filter_by(
        member_id=member.id
    ).count()

    recent_payments = Payment.query.filter_by(
        member_id=member.id
    ).order_by(
        Payment.date_paid.desc()
    ).all()

    return render_template(
        "member_portal/payments.html",
        member=member,
        total_paid=total_paid,
        payment_count=payment_count,
        recent_payments=recent_payments
    )


from models.event import Event


@member_portal_bp.route("/events")
@login_required
def events():

    if current_user.role != "Member":
        return "Access Denied", 403

    events = (
        Event.query
        .order_by(Event.event_date.asc())
        .all()
    )

    return render_template(
        "member_portal/events.html",
        events=events
    )

@member_portal_bp.route("/notifications")
@login_required
def notifications():

    if current_user.role != "Member":
        return "Access Denied", 403

    announcements = Notice.query.all()

    print("TOTAL NOTICES:", len(announcements))

    for notice in announcements:
        print(notice.title, notice.status)

    return render_template(
        "member_portal/notifications.html",
        announcements=announcements
    )
@member_portal_bp.route("/id-card")
@login_required
def id_card():
    return digital_id()
@member_portal_bp.route("/payment/<int:payment_id>")
@login_required
def payment_receipt(payment_id):

    payment = Payment.query.get_or_404(payment_id)

    member = Member.query.filter_by(
        user_id=current_user.id
    ).first()

    if payment.member_id != member.id:
        abort(403)

    return render_template(
        "member_portal/payment_receipt.html",
        payment=payment,
        member=member
    )


