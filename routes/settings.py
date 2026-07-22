import os
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)
from flask_login import login_required
from utils.auth import roles_required
from werkzeug.utils import secure_filename

from models.election_settings import ElectionSettings
from models.system_settings import SystemSettings
from extensions import db

settings_bp = Blueprint(
    "settings",
    __name__,
    url_prefix="/settings"
)


@settings_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def dashboard():

    return render_template(
        "settings/dashboard.html"
    )
# ==========================================
# General System Settings
# ==========================================
@settings_bp.route("/system")
@login_required
@roles_required("Administrator")
def system():

    settings = SystemSettings.query.first()

    if not settings:

        settings = SystemSettings()

        db.session.add(settings)
        db.session.commit()

    return render_template(
        "settings/system.html",
        settings=settings
    )
# ==========================================
# Edit System Settings
# ==========================================
@settings_bp.route("/system/edit", methods=["GET", "POST"])
@login_required
@roles_required("Administrator")
def edit_system():

    settings = SystemSettings.query.first()

    if not settings:
        settings = SystemSettings()
        db.session.add(settings)
        db.session.commit()

    if request.method == "POST":

        settings.system_name = request.form["system_name"]
        settings.short_name = request.form["short_name"]
        settings.slogan = request.form["slogan"]
        settings.university_name = request.form["university_name"]
        settings.campus = request.form["campus"]
        settings.membership_validity = int(
            request.form["membership_validity"]
        )
        logo = request.files.get("logo")

        if logo and logo.filename:
            filename = secure_filename(logo.filename)

            logo.save(
                os.path.join(
                    "static",
                    "uploads",
                    "system",
                    filename
                )
            )

            settings.logo = filename

        signature = request.files.get("ceo_signature")

        if signature and signature.filename:
            filename = secure_filename(signature.filename)

            signature.save(
                os.path.join(
                    "static",
                    "uploads",
                    "system",
                    filename
                )
            )

            settings.ceo_signature = filename
        db.session.commit()

        return redirect(url_for("settings.system"))

    return render_template(
        "settings/edit_system.html",
        settings=settings
    )