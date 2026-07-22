from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import login_required

from extensions import db

from models.election import Election
from models.election_settings import ElectionSettings

from utils.auth import roles_required

settings_bp = Blueprint(
    "election_settings",
    __name__,
    url_prefix="/election-settings"
)


@settings_bp.route("/", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def dashboard():

    settings = ElectionSettings.query.first()

    if not settings:
        settings = ElectionSettings()
        db.session.add(settings)
        db.session.commit()

    if request.method == "POST":

        active_election = request.form.get("active_election_id")

        if active_election:
            settings.active_election_id = int(active_election)
        else:
            settings.active_election_id = None

        settings.voting_status = request.form.get(
            "voting_status"
        )

        settings.results_visible = (
            request.form.get("results_visible") == "on"
        )

        db.session.commit()

        flash(
            "Election settings updated successfully.",
            "success"
        )

        return redirect(
            url_for("settings.dashboard")
        )

    elections = Election.query.order_by(
        Election.election_name
    ).all()

    return render_template(
        "election_settings/dashboard.html",
        settings=settings,
        elections=elections
    )


