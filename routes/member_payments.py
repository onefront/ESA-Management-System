import hashlib
import hmac
import uuid

import requests

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)

from flask_login import login_required, current_user

from extensions import db
from models.payment import Payment
from models.fee_setting import FeeSetting
from services.sms_service import SMSService


member_payments_bp = Blueprint(
    "member_payments",
    __name__,
    url_prefix="/member-payments"
)


PAYSTACK_INITIALIZE_URL = "https://api.paystack.co/transaction/initialize"
PAYSTACK_VERIFY_URL = "https://api.paystack.co/transaction/verify"


def get_paystack_headers():
    return {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}",
        "Content-Type": "application/json",
    }


def get_payment_amount(payment_type, requested_amount=None):
    """
    Get the amount that the member is allowed to pay.

    Fixed fees come from the active FeeSetting record.
    Donation is allowed to use a member-entered amount.
    """

    fee_setting = (
        FeeSetting.query
        .filter_by(active=True)
        .order_by(FeeSetting.id.desc())
        .first()
    )

    if payment_type == "Donation":
        try:
            amount = float(requested_amount)
        except (TypeError, ValueError):
            return None

        if amount <= 0:
            return None

        return amount

    if not fee_setting:
        return None

    fee_map = {
        "Registration Fee": fee_setting.registration_fee,
        "Annual Dues": fee_setting.annual_dues,
        "ESA Cloth": fee_setting.esa_cloth,
        "Excursion Fee": fee_setting.excursion_fee,
        "Event Fee": fee_setting.event_fee,
        "Welfare Contribution": fee_setting.welfare_levy,
        "Other": fee_setting.other_fee,
    }

    return fee_map.get(payment_type)


def create_paystack_payment(payment, member, amount):
    """
    Initialize a Paystack transaction.
    """

    secret_key = current_app.config.get("PAYSTACK_SECRET_KEY")

    if not secret_key:
        raise RuntimeError("Paystack secret key is not configured.")

    email = current_user.email or member.email

    if not email:
        raise ValueError(
            "Your account does not have an email address. "
            "Please contact the administrator."
        )

    reference = (
        f"ESA-{member.id}-"
        f"{uuid.uuid4().hex[:20].upper()}"
    )

    payment.reference = reference
    payment.payment_method = "Paystack"
    payment.status = "Pending"

    # Assign payment.id without committing the transaction
    db.session.flush()

    payload = {
        "email": email,
        "amount": str(int(round(amount * 100))),
        "currency": "GHS",
        "reference": reference,
        "callback_url": current_app.config["PAYSTACK_CALLBACK_URL"],
        "channels": [
            "card",
            "mobile_money",
            "bank",
            "ussd",
            "bank_transfer",
        ],
        "metadata": {
            "member_id": member.id,
            "payment_id": payment.id,
            "payment_type": payment.payment_type,
        },
    }

    response = requests.post(
        PAYSTACK_INITIALIZE_URL,
        json=payload,
        headers=get_paystack_headers(),
        timeout=30,
    )

    response_data = response.json()

    if not response.ok or not response_data.get("status"):
        raise RuntimeError(
            response_data.get(
                "message",
                "Unable to initialize Paystack payment."
            )
        )

    db.session.commit()

    return response_data["data"]["authorization_url"]

def verify_paystack_transaction(reference):
    """
    Verify a transaction directly with Paystack.
    """

    response = requests.get(
        f"{PAYSTACK_VERIFY_URL}/{reference}",
        headers=get_paystack_headers(),
        timeout=30,
    )

    response_data = response.json()

    if not response.ok or not response_data.get("status"):
        return None

    return response_data.get("data")

def complete_payment_from_paystack(reference):
    """
    Verify a Paystack transaction and mark the matching ESA
    payment as approved.

    After successful approval, send one SMS confirmation
    to the member.
    """

    payment = Payment.query.filter_by(reference=reference).first()

    if not payment:
        return False, "Payment record was not found."

    transaction = verify_paystack_transaction(reference)

    if not transaction:
        return False, "Unable to verify the Paystack transaction."

    if transaction.get("status") != "success":
        return False, "The Paystack transaction was not successful."

    if transaction.get("reference") != reference:
        return False, "Payment reference verification failed."

    expected_amount = int(round(float(payment.amount) * 100))
    paid_amount = int(transaction.get("amount", 0))

    if paid_amount != expected_amount:
        return False, "The payment amount does not match."

    if transaction.get("currency") != "GHS":
        return False, "The payment currency is not valid."

    # Lock this payment row so the callback and webhook
    # cannot send duplicate SMS messages.
    payment = (
        Payment.query
        .filter_by(id=payment.id)
        .with_for_update()
        .first()
    )

    if not payment:
        return False, "Payment record was not found."

    # If already approved and SMS was already sent,
    # nothing more needs to be done.
    if payment.status == "Approved" and payment.sms_sent:
        return True, "Payment has already been processed."

    # Approve the payment.
    payment.status = "Approved"
    payment.date_paid = db.func.now()
    payment.payment_method = "Paystack"

    member = payment.member

    # Send SMS only once.
    if not payment.sms_sent and member and member.phone:

        message = (
            f"ESA CONNECT: Dear {member.first_name}, "
            f"your payment of GH₵{float(payment.amount):.2f} "
            f"for {payment.payment_type} has been received successfully. "
            f"Ref: {payment.reference}. Thank you."
        )

        sms_success, sms_response = SMSService.send_sms(
            member.phone,
            message
        )

        if sms_success:
            payment.sms_sent = True
            current_app.logger.info(
                "Payment SMS sent successfully for %s",
                payment.reference
            )
        else:
            current_app.logger.error(
                "Payment SMS failed for %s: %s",
                payment.reference,
                sms_response
            )

    db.session.commit()

    return True, "Payment verified successfully."




@member_payments_bp.route("/make-payment", methods=["GET", "POST"])
@login_required
def make_payment():

    member = current_user.member_profile

    if not member:
        flash("Member profile not found.", "danger")
        return redirect(url_for("member_portal.dashboard"))

    if request.method == "POST":

        payment_type = request.form.get("payment_type", "").strip()
        requested_amount = request.form.get("amount")

        allowed_types = [
            "Registration Fee",
            "Annual Dues",
            "ESA Cloth",
            "Excursion Fee",
            "Event Fee",
            "Welfare Contribution",
            "Donation",
            "Other",
        ]

        if payment_type not in allowed_types:
            flash("Please select a valid payment type.", "danger")
            return redirect(url_for("member_payments.make_payment"))

        amount = get_payment_amount(
            payment_type,
            requested_amount
        )

        if amount is None or amount <= 0:
            if payment_type == "Donation":
                flash(
                    "Please enter a valid donation amount.",
                    "danger"
                )
            else:
                flash(
                    "The selected fee has not been configured.",
                    "danger"
                )

            return redirect(
                url_for("member_payments.make_payment")
            )

        try:

            payment = Payment(
                member_id=member.id,
                payment_type=payment_type,
                amount=amount,
                payment_method="Paystack",
                status="Pending",
            )

            db.session.add(payment)

            authorization_url = create_paystack_payment(
                payment,
                member,
                amount
            )

            return redirect(authorization_url)

        except Exception as e:

            db.session.rollback()

            current_app.logger.exception(
                "Paystack payment initialization failed"
            )

            flash(
                f"Unable to initialize payment: {str(e)}",
                "danger"
            )

            return redirect(
                url_for("member_payments.make_payment")
            )

    fee_setting = (
        FeeSetting.query
        .filter_by(active=True)
        .order_by(FeeSetting.id.desc())
        .first()
    )

    return render_template(
        "member/payments/make_payment.html",
        fee_setting=fee_setting
    )



@member_payments_bp.route("/paystack/callback")
@login_required
def paystack_callback():

    reference = request.args.get("reference")

    if not reference:
        flash(
            "No Paystack payment reference was received.",
            "danger"
        )
        return redirect(
            url_for("member_payments.make_payment")
        )

    payment = Payment.query.filter_by(
        reference=reference
    ).first()

    if not payment:
        flash(
            "Payment record not found.",
            "danger"
        )
        return redirect(
            url_for("member_payments.make_payment")
        )

    # Make sure the logged-in member owns this payment.
    member = current_user.member_profile

    if not member or payment.member_id != member.id:
        flash(
            "You are not authorized to view this payment.",
            "danger"
        )
        return redirect(
            url_for("member_portal.dashboard")
        )

    success, message = complete_payment_from_paystack(
        reference
    )

    if success:
        flash(
            "Payment completed successfully.",
            "success"
        )
    else:
        flash(
            message,
            "danger"
        )

    return redirect(
        url_for("member_payments.payment_history")
    )


@member_payments_bp.route("/paystack/webhook", methods=["POST"])
def paystack_webhook():

    secret_key = current_app.config.get(
        "PAYSTACK_SECRET_KEY"
    )

    if not secret_key:
        return "", 500

    payload = request.get_data()

    signature = request.headers.get(
        "x-paystack-signature",
        ""
    )

    expected_signature = hmac.new(
        secret_key.encode("utf-8"),
        payload,
        hashlib.sha512
    ).hexdigest()

    if not hmac.compare_digest(
        expected_signature,
        signature
    ):
        return "", 401

    event = request.get_json(silent=True) or {}

    if event.get("event") == "charge.success":

        data = event.get("data", {})

        reference = data.get("reference")

        if reference:
            try:
                complete_payment_from_paystack(
                    reference
                )
            except Exception:
                current_app.logger.exception(
                    "Paystack webhook processing failed."
                )
                db.session.rollback()

    return "", 200


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