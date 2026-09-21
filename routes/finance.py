from flask import Blueprint, render_template
from flask_login import login_required
from extensions import db
from models.member import Member
from models.payment import Payment
from models.fee_setting import FeeSetting
from sqlalchemy import func, extract

finance_bp = Blueprint(
    "finance",
    __name__,
    url_prefix="/finance"
)


@finance_bp.route("/")
@login_required
def dashboard():

    # Active Fee Setting
    fee = FeeSetting.query.filter_by(active=True).first()

    registration_required = fee.registration_fee if fee else 200
    annual_dues_required = fee.annual_dues if fee else 50
    welfare_required = fee.welfare_levy if fee else 0
    other_required = fee.other_fee if fee else 0

    total_required = (
        registration_required +
        annual_dues_required +
        welfare_required +
        other_required
    )

    # Total Members
    total_members = Member.query.count()

    # Registration Fees Collected
    registration_total = (
        db.session.query(func.sum(Payment.amount))
        .filter(
            Payment.payment_type == "Registration Fee",
            Payment.status == "Approved"
        )
        .scalar() or 0
    )

    # Annual Dues Collected
    annual_dues_total = (
        db.session.query(func.sum(Payment.amount))
        .filter(
            Payment.payment_type == "Annual Dues",
            Payment.status == "Approved"
        )
        .scalar() or 0
    )

    # Welfare Contributions Collected
    welfare_total = (
            db.session.query(func.sum(Payment.amount))
            .filter(
                Payment.payment_type == "Welfare Contribution",
                Payment.status == "Approved"
            )
            .scalar() or 0
    )

    # Total Revenue
    total_revenue = (
            registration_total
            + annual_dues_total
            + welfare_total
    )

    # Payment Statistics
    registration_paid_members = 0
    dues_paid_members = 0
    welfare_paid_members = 0

    outstanding_members = 0

    members = Member.query.all()

    for member in members:

        registration_paid = sum(
            p.amount for p in member.payments
            if p.payment_type == "Registration Fee"
            and p.status == "Approved"
        )

        dues_paid = sum(
            p.amount for p in member.payments
            if p.payment_type == "Annual Dues"
            and p.status == "Approved"
        )

        welfare_paid = sum(
            p.amount for p in member.payments
            if p.payment_type == "Welfare Contribution"
            and p.status == "Approved"
        )


        # Count members who have paid Registration Fee
        if registration_paid > 0:
            registration_paid_members += 1

        # Count members who have fully paid Annual Dues
        if dues_paid >= annual_dues_required:
            dues_paid_members += 1

        # Count members who have paid Welfare Contribution
        if welfare_paid > 0:
            welfare_paid_members += 1

        total_paid = (
                registration_paid
                + dues_paid
                + welfare_paid
        )

        if total_paid == 0:
            outstanding_members += 1

    # Overall Collection Rate
    total_expected_revenue = total_required * total_members

    collection_rate = 0

    if total_expected_revenue > 0:
        collection_rate = round(
            (total_revenue / total_expected_revenue) * 100,
            1
        )

    # Recent Approved Payments
    recent_payments = (
        Payment.query
        .filter_by(status="Approved")
        .order_by(Payment.id.desc())
        .limit(10)
        .all()
    )

    # Top Outstanding Members
    outstanding_list = []

    for member in members:

        registration_paid = sum(
            p.amount for p in member.payments
            if p.payment_type == "Registration Fee"
            and p.status == "Approved"
        )

        dues_paid = sum(
            p.amount for p in member.payments
            if p.payment_type == "Annual Dues"
            and p.status == "Approved"
        )

        welfare_paid = sum(
            p.amount for p in member.payments
            if p.payment_type == "Welfare Contribution"
            and p.status == "Approved"
        )

        total_paid = (
                registration_paid
                + dues_paid
                + welfare_paid
        )

        balance = max(total_required - total_paid, 0)

        if balance > 0:
            outstanding_list.append({
                "member": member,
                "programme": member.programme,
                "level": member.level,
                "balance": balance
            })

    outstanding_list = sorted(
        outstanding_list,
        key=lambda x: x["balance"],
        reverse=True
    )[:10]

    # Monthly Revenue
    monthly_data = (
        db.session.query(
            extract("month", Payment.date_paid).label("month"),
            func.sum(Payment.amount)
        )
        .filter(Payment.status == "Approved")
        .group_by(extract("month", Payment.date_paid))
        .order_by(extract("month", Payment.date_paid))
        .all()
    )

    month_names = [
        "",
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    chart_labels = []
    chart_values = []

    for month, total in monthly_data:
        chart_labels.append(month_names[int(month)])
        chart_values.append(float(total))



    return render_template(
        "finance/dashboard_v2.html",
        total_members=total_members,
        registration_total=registration_total,
        annual_dues_total=annual_dues_total,
        total_revenue=total_revenue,
        total_required=total_required,

        registration_paid_members=registration_paid_members,
        dues_paid_members=dues_paid_members,
        welfare_paid_members=welfare_paid_members,
        outstanding_members=outstanding_members,
        collection_rate=collection_rate,
        recent_payments=recent_payments,
        outstanding_list=outstanding_list,
        chart_labels=chart_labels,
        chart_values=chart_values,
    )