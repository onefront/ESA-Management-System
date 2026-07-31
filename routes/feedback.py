from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required
)
from models.user import User
from models.executive import Executive
from models.feedback_reply import FeedbackReply
from flask import request, flash, redirect, url_for
from flask_login import current_user
from models.member import Member
from utils.auth import roles_required
from datetime import datetime
from extensions import db
from models.feedback import Feedback
from models.member import Member
from flask_login import current_user
from flask import (
    flash,
    request,
    redirect,
    url_for
)
from models.feedback import Feedback

feedback_bp = Blueprint(
    "feedback",
    __name__
)


# ==========================================
# Complaint Dashboard
# ==========================================
@feedback_bp.route("/feedback")
@login_required
@roles_required(
    "Administrator",
    "General Secretary",
    "CEO"
)
def dashboard():

    total_tickets = Feedback.query.count()

    new_tickets = Feedback.query.filter_by(
        status="New"
    ).count()

    assigned_tickets = Feedback.query.filter_by(
        status="Assigned"
    ).count()

    review_tickets = Feedback.query.filter_by(
        status="Under Review"
    ).count()

    resolved_tickets = Feedback.query.filter_by(
        status="Resolved"
    ).count()

    closed_tickets = Feedback.query.filter_by(
        status="Closed"
    ).count()

    recent_feedback = (
        Feedback.query
        .order_by(Feedback.created_at.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "feedback/dashboard.html",

        total_tickets=total_tickets,

        new_tickets=new_tickets,

        assigned_tickets=assigned_tickets,

        review_tickets=review_tickets,

        resolved_tickets=resolved_tickets,

        closed_tickets=closed_tickets,

        recent_feedback=recent_feedback
    )



# ==========================================
# Submit Complaint
# ==========================================
@feedback_bp.route(
    "/complaints/new",
    methods=["GET", "POST"]
)
@login_required
@roles_required(
    "Administrator",
    "General Secretary",
    "CEO",
    "Member"
)
def create_complaint():

    if request.method == "POST":

        member = Member.query.filter_by(
            user_id=current_user.id
        ).first()

        if not member:

            flash(
                "Member profile not found.",
                "danger"
            )

            return redirect(
                url_for("feedback.create_complaint")
            )

        feedback = Feedback(

            member_id=member.id,

            feedback_type=request.form.get("feedback_type"),

            subject=request.form.get("subject"),

            description=request.form.get("description"),

            priority=request.form.get("priority"),

            anonymous=bool(
                int(request.form.get("anonymous", 0))
            ),

            status="New"
        )

        # Generate Ticket Number
        last_feedback = Feedback.query.order_by(
            Feedback.id.desc()
        ).first()

        if last_feedback:
            next_number = last_feedback.id + 1
        else:
            next_number = 1

        feedback.ticket_no = (
            f"ESA-{datetime.utcnow().year}-{next_number:06d}"
        )

        db.session.add(feedback)
        db.session.commit()

        flash(
            f"Complaint submitted successfully. Ticket No: {feedback.ticket_no}",
            "success"
        )

        return redirect(
            url_for("feedback.my_complaints")
        )

    return render_template(
        "feedback/create.html"
    )

# ==========================================
# My Complaints
# ==========================================
@feedback_bp.route("/complaints/my")
@login_required
@roles_required(
    "Administrator",
    "General Secretary",
    "CEO",
    "Member"
)
def my_complaints():

    member = Member.query.filter_by(
        user_id=current_user.id
    ).first()

    if not member:

        flash(
            "Member profile not found.",
            "danger"
        )

        return redirect(url_for("dashboard.dashboard"))

    complaints = (
        Feedback.query
        .filter_by(member_id=member.id)
        .order_by(Feedback.created_at.desc())
        .all()
    )

    return render_template(
        "feedback/my_complaints.html",
        complaints=complaints
    )



# ==========================================
# Complaint Details
# ==========================================
@feedback_bp.route(
    "/complaints/<int:feedback_id>",
    methods=["GET", "POST"]
)
@login_required
@roles_required(
    "Administrator",
    "General Secretary",
    "CEO",
    "Member"
)
def complaint_details(feedback_id):

    complaint = Feedback.query.get_or_404(feedback_id)

    member = Member.query.filter_by(
        user_id=current_user.id
    ).first()

    # Members can only view their own complaint
    if (
        current_user.role == "Member"
        and member
        and complaint.member_id != member.id
    ):
        flash(
            "You are not allowed to view this complaint.",
            "danger"
        )

        return redirect(
            url_for("feedback.my_complaints")
        )

    # ---------------------------------------
    # Handle POST Actions
    # ---------------------------------------
    if request.method == "POST":

        action = request.form.get("action")

        # ---------------------------------------
        # Update Status
        # ---------------------------------------
        if (
            action == "update_status"
            and current_user.role in
            ["Administrator", "CEO", "General Secretary"]
        ):

            complaint.status = request.form.get("status")

            db.session.commit()

            flash(
                "Complaint status updated successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "feedback.complaint_details",
                    feedback_id=complaint.id
                )
            )


        # ---------------------------------------
        # Assign Executive
        # ---------------------------------------
        elif action == "assign":

            assigned_to = request.form.get("assigned_to")

            if assigned_to:

                complaint.assigned_to = int(assigned_to)

                if complaint.status == "New":
                    complaint.status = "Assigned"

                db.session.commit()

                flash(
                    "Complaint assigned successfully.",
                    "success"
                )

            else:

                flash(
                    "Please select an executive.",
                    "warning"
                )

            return redirect(
                url_for(
                    "feedback.complaint_details",
                    feedback_id=complaint.id
                )
            )

        # ---------------------------------------
        # Reply
        # ---------------------------------------
        message = request.form.get("message")

        if message:

            reply = FeedbackReply(
                feedback_id=complaint.id,
                user_id=current_user.id,
                message=message
            )

            db.session.add(reply)
            db.session.commit()

            flash(
                "Reply added successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "feedback.complaint_details",
                    feedback_id=complaint.id
                )
            )

    # ---------------------------------------
    # Load Executives
    # ---------------------------------------
    executives = Executive.query.order_by(
        Executive.position,
        Executive.full_name
    ).all()

    # ---------------------------------------
    # Load Replies
    # ---------------------------------------
    replies = FeedbackReply.query.filter_by(
        feedback_id=complaint.id
    ).order_by(
        FeedbackReply.created_at.asc()
    ).all()

    return render_template(
        "feedback/details.html",
        complaint=complaint,
        replies=replies,
        executives=executives
    )
# ==========================================
# All Complaints (Admin)
# ==========================================
@feedback_bp.route("/feedback/all")
@login_required
@roles_required(
    "Administrator",
    "General Secretary",
    "CEO"
)
def all_complaints():

    complaints = (
        Feedback.query
        .order_by(Feedback.created_at.desc())
        .all()
    )

    return render_template(
        "feedback/all_complaints.html",
        complaints=complaints
    )