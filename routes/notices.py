import os
from uuid import uuid4

from flask import current_app
from werkzeug.utils import secure_filename
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required

from extensions import db

from models.notice import Notice

from utils.auth import roles_required

from utils.audit import log_activity


notices_bp = Blueprint(
    "notices",
    __name__,
    url_prefix="/notices"
)


# ==========================================
# Notice Dashboard
# ==========================================
@notices_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def notices():

    notices = Notice.query.order_by(
        Notice.created_at.desc()
    ).all()

    return render_template(
        "notices/index.html",
        notices=notices
    )


# ==========================================
# Add Notice
# ==========================================
@notices_bp.route("/add", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def add_notice():

    if request.method == "POST":

        # -----------------------------
        # Upload Notice Image
        # -----------------------------
        image = request.files.get("image")

        image_filename = None

        if image and image.filename:

            allowed_images = {
                "jpg",
                "jpeg",
                "png",
                "gif",
                "webp"
            }

            ext = image.filename.rsplit(".", 1)[1].lower()

            if ext not in allowed_images:
                flash("Only image files are allowed.", "danger")
                return redirect(request.url)

            upload_folder = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                "notices"
            )

            os.makedirs(upload_folder, exist_ok=True)

            image_filename = f"{uuid4().hex}.{ext}"

            image.save(
                os.path.join(upload_folder, image_filename)
            )

        # -----------------------------
        # Upload Attachment
        # -----------------------------
        attachment = request.files.get("attachment")

        attachment_filename = None
        attachment_name = None
        attachment_type = None

        if attachment and attachment.filename:

            allowed_docs = {
                "pdf",
                "doc",
                "docx",
                "xls",
                "xlsx",
                "ppt",
                "pptx"
            }

            ext = attachment.filename.rsplit(".", 1)[1].lower()

            if ext not in allowed_docs:
                flash(
                    "Only PDF, Word, Excel and PowerPoint files are allowed.",
                    "danger"
                )

                return redirect(request.url)

            upload_folder = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                "notices"
            )

            os.makedirs(upload_folder, exist_ok=True)

            attachment_filename = f"{uuid4().hex}.{ext}"

            attachment.save(
                os.path.join(upload_folder, attachment_filename)
            )

            attachment_name = attachment.filename
            attachment_type = attachment.content_type

        notice = Notice(

            title=request.form["title"],

            message=request.form["message"],

            category=request.form["category"],

            image=f"notices/{image_filename}" if image_filename else None,

            attachment=f"notices/{attachment_filename}" if attachment_filename else None,

            attachment_name=attachment_name,

            attachment_type=attachment_type,

            status=request.form["status"],

            is_pinned=True if request.form.get("is_pinned") else False

        )

        db.session.add(notice)
        db.session.commit()

        print("=== BEFORE AUDIT ===")

        log_activity(
            module="Notice Board",
            action="Created Notice",
            description=notice.title
        )

        print("=== AFTER AUDIT ===")

        flash(
            "Notice created successfully.",
            "success"
        )

        return redirect(
            url_for("notices.notices")
        )

    return render_template(
        "notices/add.html"
    )

# ==========================================
# View Notice
# ==========================================
@notices_bp.route("/view/<int:notice_id>")
@login_required
@roles_required("Administrator", "General Secretary")
def view_notice(notice_id):

    notice = Notice.query.get_or_404(notice_id)

    return render_template(
        "notices/view.html",
        notice=notice
    )

# ==========================================
# Edit Notice
# ==========================================
@notices_bp.route("/edit/<int:notice_id>", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def edit_notice(notice_id):

    notice = Notice.query.get_or_404(notice_id)

    if request.method == "POST":

        notice.title = request.form["title"]
        notice.message = request.form["message"]
        notice.category = request.form["category"]
        notice.status = request.form["status"]
        notice.is_pinned = True if request.form.get("is_pinned") else False

        db.session.commit()

        log_activity(
            module="Notice Board",
            action="Updated Notice",
            description=notice.title
        )

        flash(
            "Notice updated successfully.",
            "success"
        )

        return redirect(url_for("notices.notices"))

    return render_template(
        "notices/edit.html",
        notice=notice
    )

# ==========================================
# Delete Notice
# ==========================================
@notices_bp.route("/delete/<int:notice_id>", methods=["POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def delete_notice(notice_id):

    notice = Notice.query.get_or_404(notice_id)

    # Delete notice image
    if notice.image:
        image_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            notice.image
        )

        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete attachment
    if notice.attachment:
        attachment_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            notice.attachment
        )

        if os.path.exists(attachment_path):
            os.remove(attachment_path)

    title = notice.title

    db.session.delete(notice)
    db.session.commit()

    log_activity(
        module="Notice Board",
        action="Deleted Notice",
        description=title
    )

    flash(
        "Notice deleted successfully.",
        "success"
    )

    return redirect(url_for("notices.notices"))