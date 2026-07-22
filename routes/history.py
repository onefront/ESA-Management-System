from flask import Blueprint, render_template

from flask_login import login_required

from utils.auth import roles_required

from models.election import Election

history_bp = Blueprint(
    "history",
    __name__,
    url_prefix="/history"
)


@history_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def dashboard():

    elections = Election.query.order_by(
        Election.id.desc()
    ).all()

    return render_template(
        "history/dashboard.html",
        elections=elections
    )
@history_bp.route("/view/<int:election_id>")
@login_required
@roles_required("Administrator", "General Secretary")
def view_election(election_id):

    election = Election.query.get_or_404(election_id)

    return render_template(
        "history/view.html",
        election=election
    )