from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from datetime import datetime
from flask_login import current_user
from flask_login import login_required

from models.payment import Payment
from extensions import db
from utils.auth import admin_required

payment_approval_bp = Blueprint(
    "payment_approval",
    __name__,
    url_prefix="/payment-approval"
)


@payment_approval_bp.route("/")
@login_required
@admin_required
def index():
    payments = (
        Payment.query
        .order_by(Payment.id.desc())
        .all()
    )

    pending_count = Payment.query.filter_by(
        status="Pending"
    ).count()

    approved_count = Payment.query.filter_by(
        status="Approved"
    ).count()

    rejected_count = Payment.query.filter_by(
        status="Rejected"
    ).count()

    total_amount = db.session.query(
        db.func.sum(Payment.amount)
    ).filter(
        Payment.status == "Approved"
    ).scalar() or 0

    return render_template(
        "payments/approval_dashboard.html",
        payments=payments,
        pending_count=pending_count,
        approved_count=approved_count,
        rejected_count=rejected_count,
        total_amount=total_amount
    )


@payment_approval_bp.route(
    "/review/<int:payment_id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def review(payment_id):

    payment = Payment.query.get_or_404(payment_id)

    if request.method == "POST":

        action = request.form["action"]
        remarks = request.form["remarks"]

        payment.remarks = remarks
        payment.approved_by = current_user.id
        payment.approved_at = datetime.utcnow()

        if action == "approve":
            payment.status = "Approved"
            flash(
                "Payment approved successfully.",
                "success"
            )
        else:
            payment.status = "Rejected"
            flash(
                "Payment rejected successfully.",
                "warning"
            )

        db.session.commit()

        return redirect(
            url_for("payment_approval.index")
        )

    return render_template(
        "payments/review_payment.html",
        payment=payment
    )



@payment_approval_bp.route("/approve/<int:payment_id>")
@login_required
@admin_required
def approve(payment_id):

    payment = Payment.query.get_or_404(payment_id)

    payment.status = "Approved"
    payment.approved_by = current_user.id
    payment.approved_at = datetime.utcnow()

    db.session.commit()

    flash(
        "Payment approved successfully.",
        "success"
    )

    return redirect(
        url_for("payment_approval.index")
    )
@payment_approval_bp.route("/reject/<int:payment_id>")
@login_required
@admin_required
def reject(payment_id):

    payment = Payment.query.get_or_404(payment_id)

    payment.status = "Rejected"
    payment.approved_by = current_user.id
    payment.approved_at = datetime.utcnow()

    db.session.commit()

    flash(
        "Payment rejected successfully.",
        "warning"
    )

    return redirect(
        url_for("payment_approval.index")
    )