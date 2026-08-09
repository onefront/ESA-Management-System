from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from flask_login import login_required, current_user
import secrets

from models.election_device_vote import ElectionDeviceVote
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

        student_ids = request.form.getlist("student_id")

        # Remove empty entries
        student_ids = [
            student_id.strip().upper()
            for student_id in student_ids
            if student_id.strip()
        ]

        if not student_ids:
            flash(
                "Please enter at least one Index Number.",
                "warning"
            )
            return redirect(url_for("voting.reset_voter"))

        # Maximum of 10 Index Numbers
        if len(student_ids) > 10:
            flash(
                "You can reset a maximum of 10 Index Numbers at once.",
                "danger"
            )
            return redirect(url_for("voting.reset_voter"))

        reset_count = 0
        not_found = []

        for student_id in student_ids:

            index = MemberIndex.query.filter_by(
                student_id=student_id
            ).first()

            if not index:
                not_found.append(student_id)
                continue

            # Delete only this voter's votes
            # from the active election
            deleted_votes = Vote.query.filter_by(
                election_id=settings.active_election_id,
                member_index_id=index.id
            ).delete(
                synchronize_session=False
            )

            # Make the Index Number available again
            # Remove this voter's device restriction
            ElectionDeviceVote.query.filter_by(
                election_id=settings.active_election_id,
                member_index_id=index.id
            ).delete(
                synchronize_session=False
            )

            # Make the Index Number available again
            index.used = False
            index.used_at = None

            reset_count += 1

            # Record each reset separately
            log_activity(
                module="Elections",
                action="Reset Voter",
                description=(
                    f"Index Number {student_id} was reset "
                    f"for the active election. "
                    f"{deleted_votes} vote(s) removed."
                )
            )

        db.session.commit()

        if reset_count:
            flash(
                f"{reset_count} voter(s) reset successfully. "
                f"They can vote again.",
                "success"
            )

        if not_found:
            flash(
                "Index Numbers not found: "
                + ", ".join(not_found),
                "warning"
            )

        return redirect(
            url_for("voting.reset_voter")
        )

    return render_template(
        "voting/reset_voter.html"
    )



def get_device_token():
    token = request.cookies.get("esa_device_token")

    if not token:
        token = secrets.token_urlsafe(48)

    return token



@voting_bp.route("/login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":

        student_id = request.form["student_id"].strip().upper()

        index = MemberIndex.query.filter_by(
            student_id=student_id
        ).first()

        if not index:
            log_activity(
                module="Voting",
                action="Invalid Index",
                description=f"Invalid Index Number attempt: {student_id}"
            )
            flash(
                "Invalid Index Number.",
                "danger"
            )

            return redirect(
                url_for("voting.student_login")
            )

        if index.used:
            log_activity(
                module="Voting",
                action="Already Voted",
                description=f"Index Number {student_id} attempted to vote again"
            )
            flash(
                "This Index Number has already voted.",
                "warning"
            )

            return redirect(
                url_for("voting.student_login")
            )

        settings = ElectionSettings.query.first()

        if not settings or not settings.active_election_id:
            flash(
                "No active election is configured.",
                "danger"
            )

            return redirect(
                url_for("voting.student_login")
            )

        # Administrator can use the same device for testing
        is_admin = (
            current_user.is_authenticated
            and getattr(current_user, "role", None) == "Administrator"
        )

        if not is_admin:

            device_token = get_device_token()

            device_vote = ElectionDeviceVote.query.filter_by(
                election_id=settings.active_election_id,
                device_token=device_token
            ).first()

            if device_vote:
                log_activity(
                    module="Voting",
                    action="Device Blocked",
                    description=(
                        f"Device already used for election "
                        f"{settings.active_election_id}; "
                        f"Index Number {student_id} was blocked"
                    )
                )
                flash(
                    "This device has already been used to vote in this election.",
                    "warning"
                )

                return redirect(
                    url_for("voting.student_login")
                )

            session["device_token"] = device_token

        session["member_index_id"] = index.id

        response = redirect(
            url_for("voting.ballot")
        )

        if not is_admin:
            response.set_cookie(
                "esa_device_token",
                device_token,
                max_age=60 * 60 * 24 * 365,
                httponly=True,
                samesite="Lax"
            )

        return response

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

    # Log ballot access only once
    log_activity(
        module="Voting",
        action="Ballot Accessed",
        description=f"Index Number {index.student_id} accessed the ballot"
    )

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
    index = MemberIndex.query.get(
        session["member_index_id"]
    )

    log_activity(
        module="Voting",
        action="Vote Confirmation",
        description=f"Index Number {index.student_id} reached vote confirmation"
    )
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

    if not settings or not settings.active_election_id:
        flash(
            "No active election is configured.",
            "danger"
        )

        session.clear()

        return redirect(
            url_for("voting.student_login")
        )

        # Administrator bypasses the device restriction
    is_admin = (
            current_user.is_authenticated
            and getattr(current_user, "role", None) == "Administrator"
    )

    device_token = session.get("device_token")

    if not is_admin:

            if not device_token:
                device_token = request.cookies.get("esa_device_token")

            if not device_token:
                log_activity(
                    module="Voting",
                    action="Session Expired",
                    description="Voting session expired before vote submission"
                )

                flash(
                    "Voting session expired. Please enter your Index Number again.",
                    "warning"
                )

                session.clear()

                return redirect(
                    url_for("voting.student_login")
                )



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

    # Record the device for normal voters
    if not is_admin:
        device_vote = ElectionDeviceVote(
            election_id=settings.active_election_id,
            member_index_id=index.id,
            device_token=device_token
        )

        db.session.add(device_vote)

    db.session.commit()

    if is_admin:
        log_activity(
            module="Voting",
            action="Administrator Vote",
            description=(
                f"Administrator submitted a test vote "
                f"for Index Number {index.student_id} "
                f"in election {settings.active_election_id}"
            )
        )
    else:
        log_activity(
            module="Voting",
            action="Vote Submitted",
            description=(
                f"Vote successfully submitted for "
                f"Index Number {index.student_id} "
                f"in election {settings.active_election_id}"
            )
        )

    # Preserve the ESA Connect login session
    session.pop("member_index_id", None)
    session.pop("device_token", None)

    flash(
        "Your vote has been submitted successfully.",
        "success"
    )

    if current_user.is_authenticated and getattr(current_user, "role", None) == "Member":
        return redirect(
            url_for("member_portal.dashboard")
        )

    return redirect(
        url_for("voting.success")
    )