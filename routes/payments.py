from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from extensions import db
from models.member import Member
from models.payment import Payment

payments_bp = Blueprint("payments", __name__)

# ==========================================
# Payments Dashboard
# ==========================================
@payments_bp.route("/payments")
def payments():

    search = request.args.get("search", "")

    query = Payment.query.join(Member)

    if search:
        query = query.filter(
            Member.first_name.contains(search) |
            Member.last_name.contains(search) |
            Member.student_id.contains(search) |
            Member.esa_id.contains(search)
        )

    payments = query.order_by(
        Payment.date_paid.desc()
    ).all()

    total_payments = Payment.query.count()

    total_revenue = db.session.query(
        db.func.sum(Payment.amount)
    ).scalar() or 0

    return render_template(
        "payments/index.html",
        payments=payments,
        total_payments=total_payments,
        total_revenue=total_revenue
    )
# ==========================================
# Add Payment (Dashboard)
# ==========================================
@payments_bp.route("/payments/add", methods=["GET", "POST"])
def add_payment_dashboard():

    members = Member.query.order_by(
        Member.first_name
    ).all()

    if request.method == "POST":
        payment = Payment(

            member_id=request.form["member_id"],

            payment_type=request.form["payment_type"],

            amount=float(request.form["amount"]),

            payment_method=request.form["payment_method"]

        )

        db.session.add(payment)
        db.session.flush()

        payment.reference = (
            f"ESA-REC-{payment.date_paid.year}-{payment.id:06d}"
        )

        db.session.commit()

        return redirect(url_for("payments.payments"))


    return render_template(
        "payments/add_dashboard.html",
        members=members
    )
# ==========================================
# Member Payments
# ==========================================
@payments_bp.route("/members/<int:member_id>/payments")
def member_payments(member_id):

    member = Member.query.get_or_404(member_id)

    payments = Payment.query.filter_by(
        member_id=member.id
    ).order_by(
        Payment.date_paid.desc()
    ).all()

    return render_template(
        "payments/member_payments.html",
        member=member,
        payments=payments
    )


# ==========================================
# Add Payment
# ==========================================
@payments_bp.route(
    "/members/<int:member_id>/payments/add",
    methods=["GET", "POST"]
)
def add_payment(member_id):

    member = Member.query.get_or_404(member_id)

    if request.method == "POST":
        payment = Payment(
            member_id=member.id,
            payment_type=request.form["payment_type"],
            amount=float(request.form["amount"]),
            payment_method=request.form["payment_method"]
        )

        db.session.add(payment)
        db.session.flush()

        payment.reference = (
            f"ESA-REC-{payment.date_paid.year}-{payment.id:06d}"
        )

        db.session.commit()

        return redirect(
            url_for(
                "payments.member_payments",
                member_id=member.id
            )
        )



    return render_template(
        "payments/add.html",
        member=member
    )

# ==========================================
# Edit Payment
# ==========================================
@payments_bp.route(
    "/payments/<int:payment_id>/edit",
    methods=["GET", "POST"]
)
def edit_payment(payment_id):

    payment = Payment.query.get_or_404(payment_id)

    if request.method == "POST":

        payment.payment_type = request.form["payment_type"]
        payment.amount = request.form["amount"]
        payment.payment_method = request.form["payment_method"]
        payment.reference = request.form["reference"]

        db.session.commit()

        return redirect(url_for("payments.payments"))

    return render_template(
        "payments/edit.html",
        payment=payment
    )
# ==========================================
# Delete Payment
# ==========================================
@payments_bp.route(
    "/payments/<int:payment_id>/delete",
    methods=["GET", "POST"]
)
def delete_payment(payment_id):

    payment = Payment.query.get_or_404(payment_id)

    if request.method == "POST":

        db.session.delete(payment)
        db.session.commit()

        return redirect(url_for("payments.payments"))

    return render_template(
        "payments/delete.html",
        payment=payment
    )

# ==========================================
    # Payment Receipt
    # ==========================================
@payments_bp.route("/payments/<int:payment_id>/receipt")
def payment_receipt(payment_id):
        payment = Payment.query.get_or_404(payment_id)

        return render_template(
            "payments/receipt.html",
            payment=payment
        )
@payments_bp.route("/payments/reports")
def reports():

    total_revenue = db.session.query(
        db.func.sum(Payment.amount)
    ).scalar() or 0

    total_payments = Payment.query.count()

    members_paid = db.session.query(
        Payment.member_id
    ).distinct().count()

    total_members = Member.query.count()

    outstanding_members = total_members - members_paid

    recent_payments = Payment.query.order_by(
        Payment.date_paid.desc()
    ).limit(10).all()

    payment_summary = db.session.query(
        Payment.payment_type,
        db.func.sum(Payment.amount)
    ).group_by(
        Payment.payment_type
    ).all()

    return render_template(
        "payments/reports.html",
        total_revenue=total_revenue,
        total_payments=total_payments,
        members_paid=members_paid,
        outstanding_members=outstanding_members,
        recent_payments=recent_payments,
        payment_summary=payment_summary
    )