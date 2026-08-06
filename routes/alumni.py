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
from sqlalchemy import or_
from models.member import Member
from utils.auth import roles_required
from extensions import db
from datetime import date
alumni_bp = Blueprint(
    "alumni",
    __name__,
    url_prefix="/alumni"
)


@alumni_bp.route("/")
@login_required
def index():
    search = request.args.get("search", "").strip()

    query = Member.query.filter_by(
        member_type="Alumni"
    )

    if search:
        query = query.filter(
            or_(

                Member.first_name.ilike(f"%{search}%"),
                Member.last_name.ilike(f"%{search}%"),
                Member.student_id.ilike(f"%{search}%"),
                Member.esa_id.ilike(f"%{search}%"),
                Member.phone.ilike(f"%{search}%"),
                Member.programme.ilike(f"%{search}%")
            )
        )

    alumni = query.order_by(
        Member.first_name
    ).all()

    total_alumni = len(alumni)

    this_year = Member.query.filter_by(
        member_type="Alumni"
    ).filter(
        Member.graduation_year != None
    ).count()

    male_count = Member.query.filter_by(
        member_type="Alumni",
        gender="Male"
    ).count()

    female_count = Member.query.filter_by(
        member_type="Alumni",
        gender="Female"
    ).count()

    programme_count = db.session.query(
        Member.programme
    ).filter_by(
        member_type="Alumni"
    ).distinct().count()

    return render_template(
        "alumni/index.html",
        alumni=alumni,
        total_alumni=total_alumni,
        this_year=this_year,
        male_count=male_count,
        female_count=female_count,
        programme_count=programme_count
    )

# ==========================================
# Alumni Profile
# ==========================================
@alumni_bp.route("/<int:id>")
@login_required
@roles_required(
    "Administrator",
    "CEO",
    "General Secretary"
)
def profile(id):

    member = Member.query.get_or_404(id)

    if member.member_type != "Alumni":

        flash(
            "This member is not an Alumni.",
            "warning"
        )

        return redirect(
            url_for("alumni.index")
        )

    return render_template(
        "members/alumni_profile.html",
        member=member
    )


# ==========================================
# Restore Alumni to Active Member
# ==========================================
@alumni_bp.route("/restore/<int:id>")
@login_required
@roles_required(
    "Administrator",
    "CEO",
    "General Secretary"
)
def restore(id):

    member = Member.query.get_or_404(id)

    if member.member_type != "Alumni":

        flash(
            "This member is not an Alumni.",
            "warning"
        )

        return redirect(
            url_for("alumni.index")
        )

    member.member_type = "Student"
    member.status = "Active"
    member.graduation_year = None
    member.graduation_date = None

    db.session.commit()

    flash(
        f"{member.full_name} has been restored successfully.",
        "success"
    )

    return redirect(
        url_for("alumni.index")
    )