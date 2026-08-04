from flask import Blueprint, render_template

pwa_bp = Blueprint("pwa", __name__)

@pwa_bp.route("/offline")
def offline():
    return render_template("offline.html")