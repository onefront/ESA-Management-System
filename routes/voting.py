from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from extensions import db

from models.member import Member
from models.vote import Vote
from models.portfolio import Portfolio
from models.candidate import Candidate
from models.election_settings import ElectionSettings

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
# STUDENT LOGIN
# ==========================================
@voting_bp.route("/login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":

        student_id = request.form["student_id"].strip()

        member = Member.query.filter_by(
            student_id=student_id
        ).first()

        if not member:

            flash(
                "Student ID not found.",
                "danger"
            )

            return redirect(
                url_for("voting.student_login")
            )

        if member.has_voted:

            flash(
                "You have already voted.",
                "warning"
            )

            return redirect(
                url_for("voting.student_login")
            )

        return redirect(
            url_for(
                "voting.ballot",
                member_id=member.id
            )
        )

    return render_template(
        "voting/login.html"
    )
# ==========================================
# BALLOT PAGE
# ==========================================

@voting_bp.route("/ballot/<int:member_id>", methods=["GET", "POST"])
def ballot(member_id):

    member = Member.query.get_or_404(member_id)
    if member.has_voted:
        flash(
            "You have already voted.",
            "warning"
        )

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

    if request.method == "POST":

        portfolios = Portfolio.query.order_by(
            Portfolio.display_order
        ).all()

        selections = []

        for portfolio in portfolios:

            candidate_id = request.form.get(
                f"portfolio_{portfolio.id}"
            )

            if candidate_id:
                candidate = Candidate.query.get(
                    int(candidate_id)
                )

                selections.append({
                    "portfolio": portfolio,
                    "candidate": candidate
                })

        return render_template(
            "voting/confirm_vote.html",
            member_id=member.id,
            selections=selections
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
        member=member,
        ballot=ballot
    )
@voting_bp.route("/success")
def success():

    return render_template(
        "voting/success.html"
    )
@voting_bp.route("/submit/<int:member_id>", methods=["POST"])
def submit_vote(member_id):

    member = Member.query.get_or_404(member_id)

    if member.has_voted:

        flash(
            "You have already voted.",
            "warning"
        )

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

            vote = Vote(
                election_id=settings.active_election_id,
                portfolio_id=portfolio.id,
                candidate_id=int(candidate_id),
                member_id=member.id
            )

            db.session.add(vote)

    member.has_voted = True

    db.session.commit()

    flash(
        "Your vote has been submitted successfully.",
        "success"
    )

    return redirect(
        url_for("voting.student_login")
    )