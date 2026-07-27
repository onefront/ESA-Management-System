from models.portfolio import Portfolio
from models.candidate import Candidate
from models.vote import Vote


def get_portfolio_results(election):
    """
    Returns election results grouped by portfolio.
    Used by:
        - Admin Results Dashboard
        - Member Portal
    """

    results = []

    portfolios = Portfolio.query.order_by(
        Portfolio.display_order
    ).all()

    for portfolio in portfolios:

        candidates = Candidate.query.filter_by(
            election_id=election.id,
            portfolio_id=portfolio.id,
            status="Active"
        ).all()

        portfolio_results = []
        portfolio_total = 0

        # Count votes
        for candidate in candidates:

            votes = Vote.query.filter_by(
                candidate_id=candidate.id
            ).count()

            portfolio_total += votes

            portfolio_results.append({
                "candidate": candidate,
                "votes": votes
            })

        # Highest votes first
        portfolio_results.sort(
            key=lambda x: x["votes"],
            reverse=True
        )

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
                election.status == "Closed"
                and item["votes"] == highest_votes
                and winner_count == 1
            )

            item["tie"] = (
                election.status == "Closed"
                and item["votes"] == highest_votes
                and winner_count > 1
            )

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

    return results