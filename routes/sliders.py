from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

import os
from werkzeug.utils import secure_filename
from flask_login import login_required

from models.slider import Slider

sliders_bp = Blueprint(
    "sliders",
    __name__,
    url_prefix="/sliders"
)


@sliders_bp.route("/")
@login_required
def index():
    sliders = Slider.query.order_by(
        Slider.display_order.asc()
    ).all()

    return render_template(
        "sliders/index.html",
        sliders=sliders
    )


@sliders_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        title = request.form.get("title")
        subtitle = request.form.get("subtitle")
        button_text = request.form.get("button_text")
        button_link = request.form.get("button_link")
        display_order = request.form.get("display_order", 1)

        image_file = request.files.get("image")

        if not image_file or image_file.filename == "":
            flash("Please select an image.", "danger")
            return redirect(request.url)

        filename = secure_filename(image_file.filename)

        upload_folder = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            "sliders"
        )

        os.makedirs(upload_folder, exist_ok=True)

        image_path = os.path.join(upload_folder, filename)

        image_file.save(image_path)

        slider = Slider(
            title=title,
            subtitle=subtitle,
            image=f"uploads/sliders/{filename}",
            button_text=button_text,
            button_link=button_link,
            display_order=display_order,
            is_active=True
        )

        from extensions import db

        db.session.add(slider)
        db.session.commit()

        flash("Slide added successfully.", "success")

        return redirect(url_for("sliders.index"))

    return render_template("sliders/add.html")