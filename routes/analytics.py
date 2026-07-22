from flask import Blueprint, render_template
from flask_login import login_required

from utils.auth import roles_required
from models.member import Member
from models.vote import Vote
from models.election_settings import ElectionSettings

analytics_bp = Blueprint(
    "analytics",
    __name__,
    url_prefix="/analytics"
)


@analytics_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def dashboard():

    total_members = Member.query.count()

    total_votes = Vote.query.count()

    voted_members = Member.query.filter_by(
        has_voted=True
    ).count()

    remaining_members = total_members - voted_members

    turnout = 0

    if total_members > 0:
        turnout = round(
            (voted_members / total_members) * 100,
            1
        )

    settings = ElectionSettings.query.first()

    return render_template(
        "analytics/dashboard.html",
        total_members=total_members,
        total_votes=total_votes,
        voted_members=voted_members,
        remaining_members=remaining_members,
        turnout=turnout,
        settings=settings
    )