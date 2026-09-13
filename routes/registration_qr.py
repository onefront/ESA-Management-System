from io import BytesIO

import qrcode
from flask import Blueprint, render_template, send_file
from flask_login import login_required, current_user


registration_qr_bp = Blueprint(
    "registration_qr",
    __name__,
    url_prefix="/admin"
)


REGISTRATION_URL = "https://onefront.pythonanywhere.com/verify-index"


def admin_or_general_secretary_required():
    return current_user.is_authenticated and current_user.role in [
        "Administrator",
        "General Secretary"
    ]


@registration_qr_bp.route("/registration-qr")
@login_required
def registration_qr():
    if not admin_or_general_secretary_required():
        return "Access denied", 403

    return render_template(
        "admin/registration_qr.html",
        registration_url=REGISTRATION_URL
    )


@registration_qr_bp.route("/registration-qr/image")
@login_required
def registration_qr_image():
    if not admin_or_general_secretary_required():
        return "Access denied", 403

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4
    )

    qr.add_data(REGISTRATION_URL)
    qr.make(fit=True)

    image = qr.make_image()

    output = BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    return send_file(
        output,
        mimetype="image/png",
        download_name="ESA_CONNECT_Registration_QR.png"
    )