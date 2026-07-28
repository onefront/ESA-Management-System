import os
import qrcode

from flask import current_app, url_for


def generate_member_qrcode(esa_id):
    folder = os.path.join(
        current_app.static_folder,
        "qrcodes"
    )

    os.makedirs(folder, exist_ok=True)

    filename = f"{esa_id}.png"

    filepath = os.path.join(folder, filename)

    if not os.path.exists(filepath):
        from flask import url_for

        url = url_for(
            "member_portal.verify_member",
            esa_id=esa_id,
            _external=True
        )

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