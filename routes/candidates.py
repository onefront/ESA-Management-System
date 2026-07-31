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

from models.candidate import Candidate
from models.member import Member
from models.election import Election
from models.portfolio import Portfolio

from utils.auth import roles_required


candidates_bp = Blueprint(
    "candidates",
    __name__,
    url_prefix="/candidates"
)


@candidates_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def candidates():

    candidates = Candidate.query.all()

    return render_template(
        "candidates/candidates.html",
        candidates=candidates
    )
@candidates_bp.route("/add", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def add_candidate():

    elections = Election.query.order_by(
        Election.election_name
    ).all()

    portfolios = Portfolio.query.order_by(
        Portfolio.display_order
    ).all()

    members = Member.query.order_by(
        Member.first_name
    ).all()

    if request.method == "POST":

        candidate = Candidate(

            election_id=request.form["election_id"],

            portfolio_id=request.form["portfolio_id"],

            member_id=request.form["member_id"],

            slogan=request.form["slogan"],

            manifesto=request.form["manifesto"],

            status=request.form["status"]

        )

        db.session.add(candidate)
        db.session.commit()

        flash(
            "Candidate registered successfully.",
            "success"
        )

        return redirect(
            url_for("candidates.candidates")
        )

    return render_template(
        "candidates/add.html",
        elections=elections,
        portfolios=portfolios,
        members=members
    )

@candidates_bp.route("/edit/<int:candidate_id>", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def edit_candidate(candidate_id):

    candidate = Candidate.query.get_or_404(candidate_id)

    elections = Election.query.order_by(
        Election.election_name
    ).all()

    portfolios = Portfolio.query.order_by(
        Portfolio.display_order
    ).all()

    members = Member.query.order_by(
        Member.first_name
    ).all()

    if request.method == "POST":

        candidate.election_id = request.form["election_id"]
        candidate.portfolio_id = request.form["portfolio_id"]
        candidate.member_id = request.form["member_id"]
        candidate.slogan = request.form["slogan"]
        candidate.manifesto = request.form["manifesto"]
        candidate.status = request.form["status"]

        db.session.commit()

        flash(
            "Candidate updated successfully.",
            "success"
        )

        return redirect(
            url_for("candidates.candidates")
        )

    return render_template(
        "candidates/edit.html",
        candidate=candidate,
        elections=elections,
        portfolios=portfolios,
        members=members
    )

@candidates_bp.route("/delete/<int:candidate_id>", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def delete_candidate(candidate_id):

    candidate = Candidate.query.get_or_404(candidate_id)

    if request.method == "POST":

        db.session.delete(candidate)
        db.session.commit()

        flash(
            "Candidate deleted successfully.",
            "success"
        )

        return redirect(
            url_for("candidates.candidates")
        )

    return render_template(
        "candidates/delete.html",
        candidate=candidate
    )