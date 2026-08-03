from flask import Blueprint
from flask import render_template
from services.sms_service import SMSService
from flask import request, jsonify
from flask_login import login_required
from flask import jsonify, request
from models.member import Member
from utils.auth import roles_required
from models.programme import Programme
from flask_login import current_user
from extensions import db
from datetime import datetime, timedelta
from models.sms_log import SMSLog
from models.sms_recipient import SMSRecipient
from models.department import Department
from models.faculty import Faculty
sms_bp = Blueprint(
    "sms",
    __name__
)


@sms_bp.route("/sms")
@login_required
@roles_required(
    "Administrator",
    "CEO",
    "General Secretary"
)
def dashboard():

    return render_template(
        "sms/dashboard.html"
    )


@sms_bp.route("/sms/compose")
@login_required
@roles_required(
    "Administrator",
    "CEO",
    "General Secretary"
)
def compose():

    programme_list = [
        {
            "id": p.id,
            "programme_name": p.programme_name
        }
        for p in Programme.query
        .filter_by(status="Active")
        .order_by(Programme.programme_name)
        .all()
    ]

    department_list = [
        {
            "id": d.id,
            "department_name": d.department_name
        }
        for d in Department.query
        .filter_by(status="Active")
        .order_by(Department.department_name)
        .all()
    ]

    faculty_list = [
        {
            "id": f.id,
            "faculty_name": f.faculty_name
        }
        for f in Faculty.query
        .filter_by(status="Active")
        .order_by(Faculty.faculty_name)
        .all()
    ]

    return render_template(
        "sms/compose.html",
        programmes=programme_list,
        departments=department_list,
        faculties=faculty_list
    )


@sms_bp.route("/sms/history")
@login_required
@roles_required(
    "Administrator",
    "CEO",
    "General Secretary"
)
def history():
    search = request.args.get("search", "").strip()

    query = SMSLog.query

    if search:
        query = query.filter(

            (SMSLog.title.ilike(f"%{search}%")) |

            (SMSLog.message.ilike(f"%{search}%")) |

            (SMSLog.recipient_group.ilike(f"%{search}%")) |

            (SMSLog.campaign_id.ilike(f"%{search}%"))

        )
    filter_by = request.args.get("filter")
    status = request.args.get("status")
    logs = (
        query
        .order_by(SMSLog.created_at.desc())
        .all()
    )

    total_campaigns = SMSLog.query.count()

    total_sms = db.session.query(
        db.func.sum(SMSLog.recipient_count)
    ).scalar() or 0

    total_credits = db.session.query(
        db.func.sum(SMSLog.credits_used)
    ).scalar() or 0

    successful = SMSLog.query.filter_by(
        status="Success"
    ).count()

    partial = SMSLog.query.filter_by(
        status="Partial"
    ).count()

    return render_template(
        "sms/history.html",
        logs=logs,
        total_campaigns=total_campaigns,
        total_sms=total_sms,
        total_credits=total_credits,
        successful=successful,
        partial=partial
    )


@sms_bp.route("/sms/templates")
@login_required
@roles_required(
    "Administrator",
    "CEO",
    "General Secretary"
)
def templates():

    return render_template(
        "sms/templates.html"
    )




@sms_bp.route("/sms/templates/new")
@login_required
@roles_required(
    "Administrator",
    "CEO",
    "General Secretary"
)
def new_template():

    return render_template(
        "sms/new_template.html"
    )



@sms_bp.route("/sms/history/<int:id>")
@login_required
@roles_required(
    "Administrator",
    "CEO",
    "General Secretary"
)
def history_details(id):

    sms = SMSLog.query.get_or_404(id)

    return render_template(
        "sms/history_details.html",
        sms=sms
    )




@sms_bp.route("/sms/search-members")
@login_required
@roles_required(
    "Administrator",
    "CEO",
    "General Secretary"
)
def search_members():

    search = request.args.get("q", "").strip()

    query = Member.query.filter_by(status="Active")

    if search:
        query = query.filter(
            (Member.first_name.ilike(f"%{search}%")) |
            (Member.last_name.ilike(f"%{search}%")) |
            (Member.student_id.ilike(f"%{search}%"))
        )

    members = (
        query
        .order_by(Member.first_name)
        .limit(100)
        .all()
    )

    return jsonify([
        {
            "id": m.id,
            "name": m.full_name,
            "student_id": m.student_id,
            "programme": m.programme,
            "department": m.department,
            "level": m.level
        }
        for m in members
    ])

@sms_bp.route("/sms/send", methods=["POST"])
@login_required
@roles_required(
    "Administrator",
    "CEO",
    "General Secretary"
)
def send_sms():

    data = request.get_json()

    message = data.get("message", "").strip()
    recipient_group = data.get("recipient_group")
    selected_members = data.get("selected_members", [])

    if not message:
        return jsonify({
            "success": False,
            "message": "Message cannot be empty."
        })

    recipients = []

    # -------------------------
    # ALL MEMBERS
    # -------------------------
    if recipient_group == "all":

        recipients = Member.query.filter_by(
            status="Active"
        ).all()

    # -------------------------
    # SELECTED MEMBERS
    # -------------------------
    elif recipient_group == "selected":

        recipients = Member.query.filter(
            Member.id.in_(selected_members)
        ).all()

    else:

        return jsonify({
            "success": False,
            "message": f"{recipient_group} sending is not yet connected."
        })

    sent = 0
    failed = 0
    errors = []

    first_success_response = None
    total_credits_used = 0

    # Create SMS Log
    sms_log = SMSLog(
        title=data.get("title"),
        message=message,
        recipient_group=recipient_group,
        recipient_count=len(recipients),
        provider="MNotify",
        sent_by=current_user.id,
        status="Processing"
    )

    db.session.add(sms_log)
    db.session.flush()

    # Send SMS
    for member in recipients:

        success, response = SMSService.send_sms(
            member.phone,
            message
        )

        print("=" * 60)
        print("PHONE:", member.phone)
        print("SUCCESS:", success)
        print("RESPONSE:", response)
        print("=" * 60)

        recipient = SMSRecipient(
            sms_log_id=sms_log.id,
            member_id=member.id,
            phone=member.phone,
            status="Sent" if success else "Failed",
            response=str(response)
        )

        db.session.add(recipient)

        if success:

            sent += 1

            summary = response.get("summary", {})

            total_credits_used += summary.get("credit_used", 0)

            if first_success_response is None:
                first_success_response = response

        else:

            failed += 1

            errors.append({
                "phone": member.phone,
                "response": response
            })

    # Update campaign details
    sms_log.status = (
        "Success"
        if failed == 0
        else "Partial"
    )

    if first_success_response:

        summary = first_success_response.get("summary", {})

        sms_log.campaign_id = summary.get("_id")
        sms_log.message_id = summary.get("message_id")
        sms_log.credits_used = total_credits_used

    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"SMS completed.\nSent: {sent}\nFailed: {failed}",
        "errors": errors
    })


