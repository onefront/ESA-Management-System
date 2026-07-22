import os
from uuid import uuid4

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)

from flask_login import login_required

from werkzeug.utils import secure_filename

from extensions import db
from models.slider import Slider
from utils.auth import admin_required


slides_bp = Blueprint(
    "slides",
    __name__,
    url_prefix="/slides"
)


UPLOAD_FOLDER = "uploads/slides"


# =====================================================
# LIST SLIDES
# =====================================================

@slides_bp.route("/")
@login_required
@admin_required
def index():

    slides = Slider.query.order_by(
        Slider.display_order.asc()
    ).all()

    return render_template(
        "slides/index.html",
        slides=slides
    )


# =====================================================
# ADD SLIDE
# =====================================================

@slides_bp.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def add():

    if request.method == "POST":

        image = request.files.get("image")

        if not image or image.filename == "":
            flash("Please select an image.", "danger")
            return redirect(request.url)

        filename = (
            f"{uuid4().hex}_"
            f"{secure_filename(image.filename)}"
        )

        folder = os.path.join(
            current_app.static_folder,
            UPLOAD_FOLDER
        )

        os.makedirs(folder, exist_ok=True)

        image.save(
            os.path.join(folder, filename)
        )

        slide = Slider(

            title=request.form["title"],

            subtitle=request.form.get("subtitle"),

            button_text=request.form.get("button_text"),

            button_link=request.form.get("button_link"),

            display_order=int(
                request.form.get("display_order", 1)
            ),

            is_active=(
                "is_active" in request.form
            ),

            image=f"{UPLOAD_FOLDER}/{filename}"

        )

        db.session.add(slide)
        db.session.commit()

        flash(
            "Slide added successfully.",
            "success"
        )

        return redirect(
            url_for("slides.index")
        )

    return render_template("slides/add.html")




# =====================================================
# EDIT SLIDE
# =====================================================

@slides_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit(id):

    slide = Slider.query.get_or_404(id)

    if request.method == "POST":

        slide.title = request.form["title"]
        slide.subtitle = request.form.get("subtitle")
        slide.button_text = request.form.get("button_text")
        slide.button_link = request.form.get("button_link")
        slide.display_order = int(request.form.get("display_order", 1))
        slide.is_active = "is_active" in request.form

        image = request.files.get("image")

        if image and image.filename != "":

            # Delete old image
            old_image = os.path.join(
                current_app.static_folder,
                slide.image
            )

            if os.path.exists(old_image):
                os.remove(old_image)

            filename = f"{uuid4().hex}_{secure_filename(image.filename)}"

            folder = os.path.join(
                current_app.static_folder,
                UPLOAD_FOLDER
            )

            os.makedirs(folder, exist_ok=True)

            image.save(
                os.path.join(folder, filename)
            )

            slide.image = f"{UPLOAD_FOLDER}/{filename}"

        db.session.commit()

        flash("Slide updated successfully.", "success")

        return redirect(url_for("slides.index"))

    return render_template(
        "slides/edit.html",
        slide=slide
    )

# =====================================================
# DELETE
# =====================================================

@slides_bp.route("/delete/<int:id>")
@login_required
@admin_required
def delete(id):

    slide = Slider.query.get_or_404(id)

    try:

        image_path = os.path.join(
            current_app.static_folder,
            slide.image
        )

        if os.path.exists(image_path):
            os.remove(image_path)

    except Exception:
        pass

    db.session.delete(slide)
    db.session.commit()

    flash(
        "Slide deleted successfully.",
        "success"
    )

    return redirect(
        url_for("slides.index")
    )