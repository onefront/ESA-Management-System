from flask import Blueprint, render_template
from sqlalchemy import func
from flask_login import login_required
from extensions import db
from utils.auth import roles_required
from models.member import Member
from models.programme import Programme
from models.payment import Payment
from models.slider import Slider
dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def dashboard():

    # Statistics
    total_members = Member.query.count()

    total_programmes = Programme.query.count()

    weekend_members = Member.query.filter_by(
        session="Weekend"
    ).count()

    evening_members = Member.query.filter_by(
        session="Evening"
    ).count()

    total_payments = Payment.query.count()

    total_revenue = db.session.query(
        func.sum(Payment.amount)
    ).scalar() or 0

    slides = Slider.query.filter_by(
        is_active=True
    ).order_by(
        Slider.display_order.asc()
    ).all()


    # Latest Members
    recent_members = Member.query.order_by(
        Member.id.desc()
    ).limit(5).all()
    # Payment Summary
    payment_count = Payment.query.count()

    total_revenue = db.session.query(
        func.sum(Payment.amount)
    ).scalar() or 0

    average_payment = 0

    if payment_count > 0:
        average_payment = total_revenue / payment_count

    recent_payments = Payment.query.order_by(
        Payment.date_paid.desc()
    ).limit(5).all()
    # Members by Level
    levels = (
        db.session.query(
            Member.level,
            func.count(Member.id)
        )
        .group_by(Member.level)
        .order_by(Member.level)
        .all()
    )

    chart_labels = [str(level[0]) for level in levels]
    chart_values = [level[1] for level in levels]
    # ==========================================
    # Recent Members
    # ==========================================
    recent_members = Member.query.order_by(
        Member.id.desc()
    ).limit(5).all()
    return render_template(
        "dashboard/index.html",
        chart_labels=chart_labels,
        chart_values=chart_values,
        total_members=total_members,
        total_programmes=total_programmes,
        weekend_members=weekend_members,
        evening_members=evening_members,
        total_payments=total_payments,
        total_revenue=total_revenue,
        recent_members=recent_members,
        payment_count=payment_count,
        average_payment=average_payment,
        recent_payments=recent_payments,
        slides=slides,

    )



