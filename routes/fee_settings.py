from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from extensions import db
from models.fee_setting import FeeSetting

fee_settings_bp = Blueprint(
    "fee_settings",
    __name__,
    url_prefix="/fee-settings"
)


@fee_settings_bp.route("/")
@login_required
def index():

    settings = FeeSetting.query.order_by(
        FeeSetting.academic_year.desc()
    ).all()

    return render_template(
        "fee_settings/index.html",
        settings=settings
    )


@fee_settings_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        if request.form.get("active"):

            FeeSetting.query.update({"active": False})

        fee = FeeSetting(
            academic_year=request.form["academic_year"],
            registration_fee=request.form["registration_fee"],
            annual_dues=request.form["annual_dues"],
            welfare_levy=request.form["welfare_levy"],
            other_fee=request.form["other_fee"],
            active=bool(request.form.get("active"))
        )

        db.session.add(fee)
        db.session.commit()

        flash("Fee setting added successfully.", "success")

        return redirect(url_for("fee_settings.index"))

    return render_template("fee_settings/add.html")


@fee_settings_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):

    fee = FeeSetting.query.get_or_404(id)

    if request.method == "POST":

        if request.form.get("active"):
            FeeSetting.query.update({"active": False})

        fee.academic_year = request.form["academic_year"]
        fee.registration_fee = request.form["registration_fee"]
        fee.annual_dues = request.form["annual_dues"]
        fee.welfare_levy = request.form["welfare_levy"]
        fee.other_fee = request.form["other_fee"]
        fee.active = bool(request.form.get("active"))

        db.session.commit()

        flash("Fee setting updated successfully.", "success")

        return redirect(url_for("fee_settings.index"))

    return render_template(
        "fee_settings/edit.html",
        fee=fee
    )
@fee_settings_bp.route("/delete/<int:id>")
@login_required
def delete(id):

    fee = FeeSetting.query.get_or_404(id)

    if fee.active:
        flash(
            "You cannot delete the active fee setting.",
            "danger"
        )
        return redirect(url_for("fee_settings.index"))

    db.session.delete(fee)
    db.session.commit()

    flash(
        "Fee setting deleted successfully.",
        "success"
    )

    return redirect(url_for("fee_settings.index"))

@fee_settings_bp.route("/activate/<int:id>")
@login_required
def activate(id):

    FeeSetting.query.update({"active": False})

    fee = FeeSetting.query.get_or_404(id)
    fee.active = True

    db.session.commit()

    flash(
        "Fee setting activated successfully.",
        "success"
    )

    return redirect(url_for("fee_settings.index"))