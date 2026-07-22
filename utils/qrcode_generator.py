import os
import qrcode

from flask import current_app


def generate_member_qrcode(esa_id):

    folder = os.path.join(
        current_app.static_folder,
        "qr_codes"
    )

    os.makedirs(folder, exist_ok=True)

    filename = f"{esa_id}.png"

    filepath = os.path.join(folder, filename)

    if not os.path.exists(filepath):

        url = f"http://127.0.0.1:5000/member/verify/{esa_id}"

        qr = qrcode.QRCode(
            version=1,
            box_size=8,
            border=2
        )

        qr.add_data(url)
        qr.make(fit=True)

        image = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        image.save(filepath)

    return filename