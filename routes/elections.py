from flask import Blueprint, render_template
from flask_login import login_required
from models.vote import Vote
from models.election_settings import ElectionSettings
from utils.auth import roles_required
from models.election import Election
from models.vote import Vote
elections_bp = Blueprint(
    "elections",
    __name__,
    url_prefix="/elections"
)

from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from extensions import db

@elections_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def dashboard():

    total_elections = Election.query.count()

    active_elections = Election.query.filter_by(
        status="Active"
    ).count()

    pending_elections = Election.query.filter_by(
        status="Pending"
    ).count()

    closed_elections = Election.query.filter_by(
        status="Closed"
    ).count()

    return render_template(
        "elections/dashboard.html",
        total_elections=total_elections,
        active_elections=active_elections,
        pending_elections=pending_elections,
        closed_elections=closed_elections
    )

@elections_bp.route("/list")
@login_required
@roles_required("Administrator", "General Secretary")
def elections():

    elections = Election.query.order_by(
        Election.start_date.desc()
    ).all()

    return render_template(
        "elections/elections.html",
        elections=elections
    )
@elections_bp.route("/add", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def add_election():

    if request.method == "POST":

        election = Election(

            election_name=request.form["election_name"],

            description=request.form.get("description"),

            start_date=datetime.strptime(
                request.form["start_date"],
                "%Y-%m-%dT%H:%M"
            ),

            end_date=datetime.strptime(
                request.form["end_date"],
                "%Y-%m-%dT%H:%M"
            ),

            status=request.form["status"]

        )

        db.session.add(election)
        db.session.commit()

        flash("Election created successfully.", "success")

        return redirect(
            url_for("elections.dashboard")
        )

    return render_template("elections/add.html")
@elections_bp.route("/edit/<int:election_id>", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def edit_election(election_id):

    election = Election.query.get_or_404(election_id)

    if request.method == "POST":

        election.election_name = request.form["election_name"]
        election.description = request.form.get("description")

        election.start_date = datetime.strptime(
            request.form["start_date"],
            "%Y-%m-%dT%H:%M"
        )

        election.end_date = datetime.strptime(
            request.form["end_date"],
            "%Y-%m-%dT%H:%M"
        )

        election.status = request.form["status"]

        db.session.commit()

        flash("Election created successfully.", "success")

        return redirect(
            url_for("elections.dashboard")
        )

    return render_template(
        "elections/edit.html",
        election=election
    )
@elections_bp.route("/delete/<int:election_id>", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def delete_election(election_id):

    election = Election.query.get_or_404(election_id)

    if request.method == "POST":

        try:

            # ------------------------------------
            # Remove active election reference
            # ------------------------------------
            settings = ElectionSettings.query.first()

            if settings and settings.active_election_id == election.id:
                settings.active_election_id = None

            # ------------------------------------
            # Delete all votes for this election
            # ------------------------------------
            Vote.query.filter_by(
                election_id=election.id
            ).delete()

            # ------------------------------------
            # Delete the election
            # Candidates will be removed automatically
            # because of cascade="all, delete-orphan"
            # ------------------------------------
            db.session.delete(election)

            db.session.commit()

            flash(
                "Election deleted successfully.",
                "success"
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"Unable to delete election: {str(e)}",
                "danger"
            )

        return redirect(
            url_for("elections.elections")
        )

    return render_template(
        "elections/delete.html",
        election=election
    )
@elections_bp.route("/view/<int:election_id>")
@login_required
@roles_required("Administrator", "General Secretary")
def view_election(election_id):

    election = Election.query.get_or_404(election_id)

    return render_template(
        "elections/view.html",
        election=election
    )