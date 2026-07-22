from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from extensions import db
from models.payment_settings import PaymentSettings
from utils.auth import roles_required

payment_settings_bp = Blueprint(
    "payment_settings",
    __name__,
    url_prefix="/payment-settings"
)


@payment_settings_bp.route("/", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "Financial Secretary", "Treasurer")
def settings():

    settings = PaymentSettings.query.first()

    if not settings:
        settings = PaymentSettings(
            momo_network="MTN Mobile Money",
            momo_number="",
            account_name="EXECUTIVE STUDENT ASSOCIATION",
            payment_instruction="",
            online_payment_enabled=True
        )

        db.session.add(settings)
        db.session.commit()

    if request.method == "POST":

        settings.momo_network = request.form["momo_network"]
        settings.momo_number = request.form["momo_number"]
        settings.account_name = request.form["account_name"]
        settings.payment_instruction = request.form["payment_instruction"]
        settings.online_payment_enabled = (
            request.form.get("online_payment_enabled") == "on"
        )

        db.session.commit()

        flash(
            "Payment settings updated successfully.",
            "success"
        )

        return redirect(
            url_for("payment_settings.settings")
        )

    return render_template(
        "payments/settings.html",
        settings=settings
    )