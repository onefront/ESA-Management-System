from flask import Blueprint, render_template

from flask_login import login_required

from utils.auth import roles_required

from models.audit_log import AuditLog

from flask import request
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
        selected_module=module
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