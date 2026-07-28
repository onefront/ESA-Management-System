
from extensions import db
from models.executive import Executive
import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    current_app
)
from flask_login import login_required
from werkzeug.utils import secure_filename
executives_bp = Blueprint("executives", __name__)


# ==========================================
# View Executives
# ==========================================
@executives_bp.route("/executives")
def executives():

    executives = Executive.query.order_by(
        Executive.position
    ).all()

    return render_template(
        "executives/index.html",
        executives=executives
    )


# ==========================================
# Add Executive

# ==========================================
# Executive Profile
# ==========================================
@executives_bp.route("/executives/<int:executive_id>")
def executive_profile(executive_id):

    executive = Executive.query.get_or_404(executive_id)

    return render_template(
        "executives/profile.html",
        executive=executive
    )
# ==========================================
# Edit Executive
# ==========================================
@executives_bp.route("/executives/edit/<int:executive_id>",
                     methods=["GET", "POST"])
def edit_executive(executive_id):

    executive = Executive.query.get_or_404(executive_id)

    if request.method == "POST":

        executive.full_name = request.form["full_name"]
        executive.position = request.form["position"]
        executive.phone = request.form["phone"]
        executive.email = request.form["email"]
        executive.year = request.form["year"]

        db.session.commit()

        return redirect(
            url_for(
                "executives.executive_profile",
                executive_id=executive.id
            )
        )

    return render_template(
        "executives/edit.html",
        executive=executive
    )
# ==========================================
# Delete Executive
# ==========================================
@executives_bp.route("/executives/delete/<int:executive_id>",
                     methods=["GET", "POST"])
def delete_executive(executive_id):

    executive = Executive.query.get_or_404(executive_id)

    if request.method == "POST":

        db.session.delete(executive)
        db.session.commit()

        return redirect(
            url_for("executives.executives")
        )

    return render_template(
        "executives/delete.html",
        executive=executive
    )
from flask import jsonify
from models.member import Member
@executives_bp.route("/search-member")
@login_required
def search_member():

    search = request.args.get("q", "").strip()

    if not search:
        return jsonify([])

    members = (
        Member.query.filter(
            (Member.first_name.ilike(f"%{search}%")) |
            (Member.last_name.ilike(f"%{search}%")) |
            (Member.student_id.ilike(f"%{search}%"))
        )
        .limit(10)
        .all()
    )

    results = []

    for member in members:
        results.append({
            "id": member.id,
            "name": f"{member.first_name} {member.last_name}",
            "student_id": member.student_id,
            "phone": member.phone,
            "email": member.email,
            "programme": member.programme,
            "photo": member.passport or ""
        })

    return jsonify(results)
@executives_bp.route("/executives/add", methods=["GET", "POST"])
def add_executive():

    if request.method == "POST":

        # Upload Photo
        photo = request.files.get("photo")

        filename = ""

        if photo and photo.filename:

            filename = secure_filename(photo.filename)

            photo.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        # Generate Executive ID
        last = Executive.query.order_by(
            Executive.id.desc()
        ).first()

        next_id = 1 if last is None else last.id + 1

        executive_id = f"ESA-EX-{next_id:03d}"

        member = Member.query.get_or_404(request.form["member_id"])

        executive = Executive(
            member_id=member.id,
            executive_id=executive_id,
            full_name=f"{member.first_name} {member.last_name}",
            position=request.form["position"],
            phone=member.phone,
            email=member.email,
            year=request.form["year"],
            photo=member.passport if member.passport else filename
        )

        db.session.add(executive)
        db.session.commit()

        return redirect(url_for("executives.executives"))

    return render_template("executives/add.html")