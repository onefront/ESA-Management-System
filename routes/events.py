import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    current_app,flash
)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from utils.audit import log_activity
from extensions import db
from models.event import Event

events_bp = Blueprint("events", __name__)


# ==========================================
# View Events
# ==========================================
@events_bp.route("/events")
def events():

    events = Event.query.order_by(
        Event.event_date.desc()
    ).all()

    return render_template(
        "events/index.html",
        events=events
    )
# ==========================================
# Edit Event
# ==========================================
@events_bp.route("/events/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):


    event = Event.query.get_or_404(event_id)

    if current_user.role not in ["Administrator", "General Secretary"]:
        flash("You are not authorized to perform that action.", "warning")

        if current_user.role == "Member":
            return redirect(url_for("member_portal.dashboard"))

        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":

        event.title = request.form["title"]
        event.venue = request.form["venue"]
        event.event_date = request.form["event_date"]
        event.event_time = request.form["event_time"]
        event.description = request.form["description"]
        event.status = request.form["status"]

        db.session.commit()

        return redirect(
            url_for(
                "events.event_profile",
                event_id=event.id
            )
        )

    return render_template(
        "events/edit.html",
        event=event
    )
# ==========================================
# Delete Event
# ==========================================
@events_bp.route("/events/delete/<int:event_id>",
                 methods=["GET", "POST"])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    if current_user.role not in ["Administrator", "General Secretary"]:
        flash("You are not authorized to perform that action.", "warning")

        if current_user.role == "Member":
            return redirect(url_for("member_portal.dashboard"))

        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":

        db.session.delete(event)
        db.session.commit()

        return redirect(
            url_for("events.events")
        )

    return render_template(
        "events/delete.html",
        event=event
    )
# ==========================================
# Event Details
# ==========================================
@events_bp.route("/events/<int:event_id>")
def event_profile(event_id):

    event = Event.query.get_or_404(event_id)

    return render_template(
        "events/profile.html",
        event=event
    )
# ==========================================
# Add Event
# ==========================================
@events_bp.route("/events/add", methods=["GET", "POST"])
def add_event():

    if request.method == "POST":

        # Upload Banner
        banner = request.files.get("banner")

        filename = ""

        if banner and banner.filename:

            filename = secure_filename(banner.filename)

            banner.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        # Generate Event Code
        last = Event.query.order_by(
            Event.id.desc()
        ).first()

        next_id = 1 if last is None else last.id + 1

        event_code = f"ESA-EVT-{next_id:03d}"

        event = Event(

            event_code=event_code,

            title=request.form["title"],

            venue=request.form["venue"],

            event_date=request.form["event_date"],

            event_time=request.form["event_time"],

            description=request.form["description"],

            banner=filename

        )

        db.session.add(event)
        db.session.commit()
        log_activity(
            module="Events",
            action="Created Event",
            description=event.title
        )
        return redirect(
            url_for("events.events")
        )

    return render_template("events/add.html")