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
