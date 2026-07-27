from flask import Blueprint, render_template
from flask_login import login_required
from services.election_service import get_portfolio_results
from utils.auth import roles_required

results_bp = Blueprint(
    "results",
    __name__,
    url_prefix="/results"
)


from flask import Blueprint, render_template
from flask_login import login_required

from utils.auth import roles_required
from models.portfolio import Portfolio
from models.candidate import Candidate
from models.election_settings import ElectionSettings
from models.election import Election
from models.vote import Vote

results_bp = Blueprint(
    "results",
    __name__,
    url_prefix="/results"
)


@results_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def dashboard():

    settings = ElectionSettings.query.first()

    active_election = None
    total_votes = 0
    results = []

    if settings and settings.active_election_id:

        active_election = Election.query.get(
            settings.active_election_id
        )

        total_votes = Vote.query.filter_by(
            election_id=settings.active_election_id
        ).count()
        results = get_portfolio_results(active_election)
    return render_template(
        "results/dashboard.html",
        settings=settings,
        active_election=active_election,
        total_votes=total_votes,
        results=results
    )