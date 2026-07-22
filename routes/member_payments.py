import os
from werkzeug.utils import secure_filename

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import login_required, current_user
from extensions import db
from models.payment import Payment
from models.payment_settings import PaymentSettings

member_payments_bp = Blueprint(
    "member_payments",
    __name__,
    url_prefix="/member-payments"
)


@member_payments_bp.route("/make-payment", methods=["GET", "POST"])
@login_required
def make_payment():

    settings = PaymentSettings.query.first()

    print("=" * 50)
    print("Current User ID:", current_user.id)
    print("Username:", current_user.username)
    print("Role:", current_user.role)
    print("Member Profile:", current_user.member_profile)
    print("=" * 50)

    if request.method == "POST":

        print("===== POST REQUEST RECEIVED =====")

        proof = request.files.get("proof_image")

        print("Uploaded File:", proof)

        filename = None

        if proof and proof.filename:
            print("Saving uploaded file...")

            filename = secure_filename(proof.filename)

            upload_folder = os.path.join(
                "static",
                "uploads",
                "payment_proofs"
            )

            os.makedirs(upload_folder, exist_ok=True)

            proof.save(
                os.path.join(upload_folder, filename)
            )

            print("File saved:", filename)

        proof = request.files.get("proof_image")

        filename = None

        if proof and proof.filename:

            filename = secure_filename(proof.filename)

            upload_folder = os.path.join(
                "static",
                "uploads",
                "payment_proofs"
            )

            os.makedirs(upload_folder, exist_ok=True)

            proof.save(
                os.path.join(upload_folder, filename)
            )

        member = current_user.member_profile

        if member is None:
            flash(
                "Your account is not linked to a member profile. Please contact the administrator.",
                "danger"
            )
            return redirect(url_for("member_payments.make_payment"))
        print("Creating Payment object...")
        payment = Payment(
            member_id=member.id,
            payment_type=request.form["payment_type"],
            amount=float(request.form["amount"]),
            payment_method=settings.momo_network,
            reference=request.form["reference"],
            proof_image=filename,
            status="Pending"
        )

        print("Adding payment to database...")
        db.session.add(payment)
        print("Committing payment...")
        db.session.commit()
        print("Payment committed successfully.")
        print("Payment ID:", payment.id)
        print("Payment saved successfully. Payment ID:", payment.id)
        flash(
            "Payment submitted successfully. Waiting for approval.",
            "success"
        )

        return redirect(
            url_for("member_payments.make_payment")
        )

    return render_template(
        "member/payments/make_payment.html",
        settings=settings
    )

@member_payments_bp.route("/payment-history")
@login_required
def payment_history():

    member = current_user.member_profile

    if member is None:
        flash(
            "Your account is not linked to a member profile.",
            "danger"
        )
        return redirect(
            url_for("member_portal.dashboard")
        )

    payments = (
        Payment.query
        .filter_by(member_id=member.id)
        .order_by(Payment.id.desc())
        .all()
    )

    return render_template(
        "member/payments/payment_history.html",
        payments=payments
    )