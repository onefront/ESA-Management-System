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
from models.portfolio import Portfolio
from utils.auth import roles_required

portfolios_bp = Blueprint(
    "portfolios",
    __name__,
    url_prefix="/portfolios"
)


@portfolios_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def portfolios():

    portfolios = Portfolio.query.order_by(
        Portfolio.display_order
    ).all()

    return render_template(
        "portfolios/portfolios.html",
        portfolios=portfolios
    )
@portfolios_bp.route("/add", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def add_portfolio():

    if request.method == "POST":

        portfolio = Portfolio(

            portfolio_name=request.form["portfolio_name"],

            description=request.form.get("description"),

            display_order=request.form["display_order"],

            status=request.form["status"]

        )

        db.session.add(portfolio)
        db.session.commit()

        flash(
            "Portfolio added successfully.",
            "success"
        )

        return redirect(
            url_for("portfolios.portfolios")
        )

    return render_template(
        "portfolios/add.html"
    )

@portfolios_bp.route("/edit/<int:portfolio_id>", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def edit_portfolio(portfolio_id):

    portfolio = Portfolio.query.get_or_404(portfolio_id)

    if request.method == "POST":

        portfolio.portfolio_name = request.form["portfolio_name"]
        portfolio.description = request.form.get("description")
        portfolio.display_order = request.form["display_order"]
        portfolio.status = request.form["status"]

        db.session.commit()

        flash(
            "Portfolio updated successfully.",
            "success"
        )

        return redirect(
            url_for("portfolios.portfolios")
        )

    return render_template(
        "portfolios/edit.html",
        portfolio=portfolio
    )


@portfolios_bp.route("/delete/<int:portfolio_id>", methods=["GET", "POST"])
@login_required
@roles_required("Administrator", "General Secretary")
def delete_portfolio(portfolio_id):

    portfolio = Portfolio.query.get_or_404(portfolio_id)

    if request.method == "POST":

        db.session.delete(portfolio)
        db.session.commit()

        flash(
            "Portfolio deleted successfully.",
            "success"
        )

        return redirect(
            url_for("portfolios.portfolios")
        )

    return render_template(
        "portfolios/delete.html",
        portfolio=portfolio
    )