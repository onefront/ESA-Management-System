from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from flask_login import login_required
from utils.auth import roles_required
from utils.audit import log_activity
from extensions import db
from models.member_index import MemberIndex
from models.member import Member
from models.vote import Vote
from models.portfolio import Portfolio
from models.candidate import Candidate
from models.election_settings import ElectionSettings
from datetime import datetime
from sqlalchemy import func
voting_bp = Blueprint(
    "voting",
    __name__,
    url_prefix="/voting"
)


# ==========================================
# ADMIN VOTING DASHBOARD
# ==========================================

@voting_bp.route("/")
def dashboard():

    return render_template(
        "voting/dashboard.html"
    )


# ==========================================
# ADMIN - RESET VOTER
# ==========================================

@voting_bp.route("/admin/reset-voter", methods=["GET", "POST"])
@login_required
@roles_required("Administrator")
def reset_voter():

    settings = ElectionSettings.query.first()

    if not settings or not settings.active_election_id:
        flash("No active election is configured.", "warning")
        return redirect(url_for("voting.dashboard"))

    if request.method == "POST":

        student_id = request.form.get(
            "student_id",
            ""
        ).strip().upper()

        if not student_id:
            flash(
                "Please enter an Index Number.",
                "warning"
            )
            return redirect(
                url_for("voting.reset_voter")
            )

        index = MemberIndex.query.filter_by(
            student_id=student_id
        ).first()

        if not index:
            flash(
                "Index Number not found.",
                "danger"
            )
            return redirect(
                url_for("voting.reset_voter")
            )

        # Delete only this voter's votes
        # from the active election
        deleted_votes = Vote.query.filter_by(
            election_id=settings.active_election_id,
            member_index_id=index.id
        ).delete(
            synchronize_session=False
        )

        # Make the Index Number available again
        index.used = False
        index.used_at = None

        db.session.commit()

        # Record the reset in the Audit Log
        log_activity(
            module="Elections",
            action="Reset Voter",
            description=(
                f"Index Number {student_id} was reset for "
                f"the active election. "
                f"{deleted_votes} vote(s) removed."
            )
        )

        flash(
            f"Index Number {student_id} has been reset "
            f"successfully. The voter can vote again.",
            "success"
        )

        return redirect(
            url_for("voting.reset_voter")
        )

    return render_template(
        "voting/reset_voter.html"
    )




# ==========================================
# STUDENT LOGIN
@voting_bp.route("/login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":

        student_id = request.form["student_id"].strip().upper()

        index = MemberIndex.query.filter_by(
            student_id=student_id
        ).first()

        if not index:

            flash(
                "Invalid Index Number.",
                "danger"
            )

            return redirect(
                url_for("voting.student_login")
            )

        if index.used:

            flash(
                "This Index Number has already voted.",
                "warning"
            )

            return redirect(
                url_for("voting.student_login")
            )

        session["member_index_id"] = index.id

        return redirect(
            url_for("voting.ballot")
        )

    return render_template(
        "voting/login.html"
    )

# BALLOT PAGE
@voting_bp.route("/ballot", methods=["GET", "POST"])
def ballot():

    if "member_index_id" not in session:

        flash(
            "Please enter your Index Number first.",
            "warning"
        )

        return redirect(
            url_for("voting.student_login")
        )

    index = MemberIndex.query.get_or_404(
        session["member_index_id"]
    )

    if index.used:

        flash(
            "This Index Number has already voted.",
            "warning"
        )

        session.clear()

        return redirect(
            url_for("voting.student_login")
        )

    settings = ElectionSettings.query.first()

    if not settings:

        flash(
            "Election has not been configured.",
            "danger"
        )

        return redirect(
            url_for("voting.student_login")
        )

    if settings.voting_status != "Open":

        flash(
            "Voting is currently closed.",
            "warning"
        )

        return redirect(
            url_for("voting.student_login")
        )

    portfolios = Portfolio.query.order_by(
        Portfolio.display_order
    ).all()

    ballot = []

    for portfolio in portfolios:

        candidates = Candidate.query.filter_by(
            election_id=settings.active_election_id,
            portfolio_id=portfolio.id,
            status="Active"
        ).all()

        ballot.append({
            "portfolio": portfolio,
            "candidates": candidates
        })

    return render_template(
        "voting/ballot.html",
        ballot=ballot,
        index=index
    )


@voting_bp.route("/success")
def success():

    return render_template(
        "voting/success.html"
    )



@voting_bp.route("/results")
def results():

    settings = ElectionSettings.query.first()

    if not settings or not settings.active_election_id:
        flash("No active election.", "warning")
        return redirect(url_for("voting.dashboard"))

    portfolios = Portfolio.query.order_by(
        Portfolio.display_order
    ).all()

    total_registered = MemberIndex.query.count()

    total_votes_cast = Vote.query.with_entities(
        Vote.member_index_id
    ).distinct().count()

    turnout = 0

    if total_registered > 0:
        turnout = round(
            (total_votes_cast / total_registered) * 100,
            2
        )

    results = []

    for portfolio in portfolios:

        candidates = Candidate.query.filter_by(
            election_id=settings.active_election_id,
            portfolio_id=portfolio.id,
            status="Active"
        ).all()

        total_votes = Vote.query.filter_by(
            election_id=settings.active_election_id,
            portfolio_id=portfolio.id
        ).count()

        candidate_results = []

        for candidate in candidates:

            votes = Vote.query.filter_by(
                election_id=settings.active_election_id,
                portfolio_id=portfolio.id,
                candidate_id=candidate.id
            ).count()

            percentage = 0

            if total_votes > 0:
                percentage = round(
                    (votes / total_votes) * 100,
                    2
                )

            candidate_results.append({
                "candidate": candidate,
                "votes": votes,
                "percentage": percentage
            })

        candidate_results.sort(
            key=lambda x: x["votes"],
            reverse=True
        )

        results.append({
            "portfolio": portfolio,
            "total_votes": total_votes,
            "winner": candidate_results[0] if candidate_results else None,
            "candidates": candidate_results
        })

    return render_template(
        "voting/results.html",
        results=results,
        total_registered=total_registered,
        total_votes_cast=total_votes_cast,
        turnout=turnout,
        settings=settings
    )



# ==========================================
# CONFIRM VOTE
# ==========================================

@voting_bp.route("/confirm", methods=["POST"])
def confirm_vote():

    if "member_index_id" not in session:
        flash(
            "Session expired. Please enter your Index Number again.",
            "warning"
        )

        return redirect(
            url_for("voting.student_login")
        )

    settings = ElectionSettings.query.first()

    portfolios = Portfolio.query.order_by(
        Portfolio.display_order
    ).all()

    selections = []

    for portfolio in portfolios:

        candidate_id = request.form.get(
            f"portfolio_{portfolio.id}"
        )

        if candidate_id:

            candidate = Candidate.query.filter_by(
                id=int(candidate_id),
                election_id=settings.active_election_id
            ).first()

            if candidate:

                selections.append({
                    "portfolio": portfolio,
                    "candidate": candidate
                })

    # IMPORTANT:
    # This must be OUTSIDE the for loop
    return render_template(
        "voting/confirm_vote.html",
        selections=selections
    )

@voting_bp.route("/submit", methods=["POST"])
def submit_vote():

    if "member_index_id" not in session:

        flash(
            "Session expired. Please enter your Index Number again.",
            "warning"
        )

        return redirect(
            url_for("voting.student_login")
        )

    index = MemberIndex.query.get_or_404(
        session["member_index_id"]
    )

    if index.used:

        flash(
            "This Index Number has already voted.",
            "warning"
        )

        session.clear()

        return redirect(
            url_for("voting.student_login")
        )

    settings = ElectionSettings.query.first()

    portfolios = Portfolio.query.order_by(
        Portfolio.display_order
    ).all()

    for portfolio in portfolios:

        candidate_id = request.form.get(
            f"portfolio_{portfolio.id}"
        )

        if candidate_id:

            existing_vote = Vote.query.filter_by(
                election_id=settings.active_election_id,
                portfolio_id=portfolio.id,
                member_index_id=index.id
            ).first()

            if existing_vote:
                continue

            vote = Vote(
                election_id=settings.active_election_id,
                portfolio_id=portfolio.id,
                candidate_id=int(candidate_id),
                member_index_id=index.id
            )

            db.session.add(vote)


    index.used = True
    index.used_at = datetime.utcnow()

    db.session.commit()

    session.clear()

    flash(
        "Your vote has been submitted successfully.",
        "success"
    )


    return redirect(
        url_for("voting.success")
)