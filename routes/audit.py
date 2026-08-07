from flask import Blueprint, render_template

from flask_login import login_required

from utils.auth import roles_required
from reportlab.platypus import Image
import os
from flask import current_app
from models.audit_log import AuditLog
from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from flask import send_file
from flask import request
from datetime import datetime, timedelta
from extensions import db
audit_bp = Blueprint(
    "audit",
    __name__,
    url_prefix="/audit"
)


@audit_bp.route("/")
@login_required
@roles_required("Administrator", "General Secretary")
def dashboard():

    search = request.args.get("search", "").strip()

    module = request.args.get("module", "").strip()

    query = AuditLog.query
    today = datetime.today().date()

    today_count = AuditLog.query.filter(
        db.func.date(AuditLog.action_time) == today
    ).count()

    week_start = today - timedelta(days=today.weekday())

    week_count = AuditLog.query.filter(
        AuditLog.action_time >= week_start
    ).count()

    month_count = AuditLog.query.filter(
        db.extract("year", AuditLog.action_time) == today.year,
        db.extract("month", AuditLog.action_time) == today.month
    ).count()

    total_count = AuditLog.query.count()
    if search:

        query = query.filter(
            db.or_(
                AuditLog.user.ilike(f"%{search}%"),
                AuditLog.action.ilike(f"%{search}%"),
                AuditLog.description.ilike(f"%{search}%")
            )
        )

    if module:

        query = query.filter(
            AuditLog.module == module
        )

    logs = query.order_by(
        AuditLog.action_time.desc()
    ).all()

    modules = (
        db.session.query(AuditLog.module)
        .distinct()
        .order_by(AuditLog.module)
        .all()
    )

    return render_template(
        "audit/dashboard.html",
        logs=logs,
        modules=[m[0] for m in modules],
        search=search,
        selected_module=module,
        today_count=today_count,
        week_count=week_count,
        month_count=month_count,
        total_count=total_count
    )


@audit_bp.route("/<int:audit_id>")
@login_required
@roles_required("Administrator", "General Secretary")
def view_audit(audit_id):
    audit = AuditLog.query.get_or_404(audit_id)

    changes = []

    if audit.action == "Updated" and audit.description:

        parts = audit.description.split("|")

        if len(parts) > 1:

            for item in parts[1].split(";"):

                if "→" in item and ":" in item:
                    field, values = item.split(":", 1)

                    old, new = values.split("→", 1)

                    changes.append({
                        "field": field.strip(),
                        "old": old.strip(),
                        "new": new.strip()
                    })

    return render_template(
        "audit/view.html",
        audit=audit,
        changes=changes
    )

@audit_bp.route("/user/<username>")
@login_required
@roles_required("Administrator", "General Secretary")
def user_logs(username):

    logs = (
        AuditLog.query
        .filter_by(user=username)
        .order_by(AuditLog.action_time.desc())
        .all()
    )

    return render_template(
        "audit/user_logs.html",
        logs=logs,
        username=username
    )



@audit_bp.route("/module/<module>")
@login_required
@roles_required("Administrator", "General Secretary")
def module_logs(module):

    logs = (
        AuditLog.query
        .filter_by(module=module)
        .order_by(AuditLog.action_time.desc())
        .all()
    )

    return render_template(
        "audit/module_logs.html",
        logs=logs,
        module=module
    )

@audit_bp.route("/export/pdf")
@login_required
@roles_required("Administrator", "General Secretary")
def export_pdf():

    logs = (
        AuditLog.query
        .order_by(AuditLog.action_time.desc())
        .all()
    )

    buffer = BytesIO()

    from reportlab.lib.pagesizes import landscape, A4

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=20,
        rightMargin=20,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    elements = []
    logo_path = os.path.join(
        current_app.static_folder,
        "images",
        "logo.png"
    )

    if os.path.exists(logo_path):
        logo = Image(
            logo_path,
            width=1.0 * inch,
            height=1.0 * inch
        )

        logo.hAlign = "CENTER"

        elements.append(logo)
    today = datetime.now()




    elements.append(
        Paragraph(
            f"Generated On: {today.strftime('%d %B %Y %I:%M %p')}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Generated By: {request.remote_addr}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph("<br/>", styles["Normal"])
    )

    elements.append(
        Paragraph(
            "<b>EXECUTIVE STUDENT ASSOCIATION</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "ESA Management System",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            "System Audit Report",
            styles["Heading1"]
        )
    )

    data = [[
        "Date",
        "User",
        "Module",
        "Action",
        "Description",
        "IP Address"
    ]]

    for log in logs:
        data.append([

            log.action_time.strftime("%d-%m-%Y %H:%M"),

            Paragraph(log.user, styles["BodyText"]),

            Paragraph(log.module, styles["BodyText"]),

            Paragraph(log.action, styles["BodyText"]),

            Paragraph(log.description or "", styles["BodyText"]),

            Paragraph(log.ip_address or "", styles["BodyText"])

        ])

    table = Table(
        data,
        colWidths=[
            1.3 * inch,
            1.2 * inch,
            1.0 * inch,
            1.0 * inch,
            2.8 * inch,
            1.2 * inch
        ]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("BOTTOMPADDING",(0,0),(-1,0),8)

        ])

    )

    elements.append(table)

    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Audit_Report.pdf",
        mimetype="application/pdf"
    )