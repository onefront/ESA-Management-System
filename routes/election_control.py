from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import login_required

from extensions import db
from models.vote import Vote
from models.member_index import MemberIndex
from models.election_settings import ElectionSettings
from models.audit_log import AuditLog
from flask_login import current_user

from utils.auth import roles_required


control_bp = Blueprint(
    "control",
    __name__,
    url_prefix="/control"
)


@control_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def dashboard():

    settings = ElectionSettings.query.first()

    return render_template(
        "control/dashboard.html",
        settings=settings
    )

@control_bp.route("/open")
@login_required
@roles_required("Administrator", "General Secretary")
def open_voting():

    settings = ElectionSettings.query.first()

    settings.voting_status = "Open"

    log = AuditLog(
        user=current_user.full_name if hasattr(current_user, "full_name") else current_user.username,
        action="Opened Voting"
    )

    db.session.add(log)

    db.session.commit()

    flash(
        "Voting has been opened successfully.",
        "success"
    )

    return redirect(
        url_for("control.dashboard")
    )


@control_bp.route("/pause")
@login_required
@roles_required("Administrator", "General Secretary")
def pause_voting():

    settings = ElectionSettings.query.first()

    settings.voting_status = "Paused"

    log = AuditLog(
        user=current_user.full_name if hasattr(current_user, "full_name") else current_user.username,
        action="Paused Voting"
    )

    db.session.add(log)

    db.session.commit()

    flash(
        "Voting has been paused.",
        "warning"
    )

    return redirect(
        url_for("control.dashboard")
    )

@control_bp.route("/close")
@login_required
@roles_required("Administrator", "General Secretary")
def close_voting():

    settings = ElectionSettings.query.first()

    settings.voting_status = "Closed"

    log = AuditLog(
        user=current_user.full_name if hasattr(current_user, "full_name") else current_user.username,
        action="Closed Voting"
    )

    db.session.add(log)

    db.session.commit()

    flash(
        "Voting has been closed.",
        "danger"
    )

    return redirect(
        url_for("control.dashboard")
    )





@control_bp.route("/reset")
@login_required
@roles_required("Administrator")
def reset_election():

    Vote.query.delete()

    MemberIndex.query.update(
        {
            MemberIndex.used: False,
            MemberIndex.used_at: None,
            MemberIndex.used_by: None
        },
        synchronize_session=False
    )

    log = AuditLog(
        user=current_user.full_name if hasattr(current_user, "full_name") else current_user.username,
        action="Reset Election"
    )

    db.session.add(log)
    db.session.commit()

    flash(
        "Election has been reset successfully.",
        "success"
    )

    return redirect(
        url_for("control.dashboard")
    )




@control_bp.route("/show-results")
@login_required
@roles_required("Administrator", "General Secretary")
def show_results():

    settings = ElectionSettings.query.first()

    settings.results_visible = True

    log = AuditLog(
        user=current_user.full_name if hasattr(current_user, "full_name") else current_user.username,
        action="Published Results"
    )

    db.session.add(log)

    db.session.commit()

    flash(
        "Results are now visible.",
        "success"
    )

    return redirect(
        url_for("control.dashboard")
    )


@control_bp.route("/hide-results")
@login_required
@roles_required("Administrator", "General Secretary")
def hide_results():

    settings = ElectionSettings.query.first()

    settings.results_visible = False

    log = AuditLog(
        user=current_user.full_name if hasattr(current_user, "full_name") else current_user.username,
        action="Hid Results"
    )

    db.session.add(log)

    db.session.commit()

    flash(
        "Results have been hidden.",
        "warning"
    )

    return redirect(
        url_for("control.dashboard")
    )