from flask import Blueprint, render_template
from flask_login import login_required

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

        portfolios = Portfolio.query.order_by(
            Portfolio.display_order
        ).all()

        for portfolio in portfolios:

            candidates = Candidate.query.filter_by(
                election_id=settings.active_election_id,
                portfolio_id=portfolio.id,
                status="Active"
            ).all()

            portfolio_results = []
            portfolio_total = 0

            for candidate in candidates:
                votes = Vote.query.filter_by(
                    candidate_id=candidate.id
                ).count()

                portfolio_total += votes

                portfolio_results.append({
                    "candidate": candidate,
                    "votes": votes
                })

            # Sort AFTER all candidates have been added
            portfolio_results.sort(
                key=lambda x: x["votes"],
                reverse=True
            )


            # Determine winner or tie
            highest_votes = 0

            if portfolio_results:
                highest_votes = portfolio_results[0]["votes"]

            winner_count = sum(
                1 for item in portfolio_results
                if item["votes"] == highest_votes
            )

            for item in portfolio_results:
                item["winner"] = (
                        active_election
                        and active_election.status == "Closed"
                        and item["votes"] == highest_votes
                        and winner_count == 1
                )

                item["tie"] = (
                        active_election
                        and active_election.status == "Closed"
                        and item["votes"] == highest_votes
                        and winner_count > 1
                )
            # -
            # ----------------------------------
            # Determine winner or tie
            # -----------------------------------

            highest_votes = 0

            if portfolio_results:
                highest_votes = portfolio_results[0]["votes"]

            winner_count = sum(
                1
                for item in portfolio_results
                if item["votes"] == highest_votes
            )

            for item in portfolio_results:
                item["winner"] = (
                        active_election
                        and active_election.status == "Closed"
                        and item["votes"] == highest_votes
                        and winner_count == 1
                )

                item["tie"] = (
                        active_election
                        and active_election.status == "Closed"
                        and item["votes"] == highest_votes
                        and winner_count > 1
                )
            for item in portfolio_results:

                if portfolio_total > 0:
                    item["percentage"] = round(
                        item["votes"] * 100 / portfolio_total,
                        1
                    )
                else:
                    item["percentage"] = 0

            results.append({
                "portfolio": portfolio,
                "results": portfolio_results
            })

    return render_template(
        "results/dashboard.html",
        settings=settings,
        active_election=active_election,
        total_votes=total_votes,
        results=results
    )