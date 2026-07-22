from flask import request
from flask_login import current_user

from extensions import db
from models.audit_log import AuditLog


def log_activity(module, action, description=None):

    try:

        log = AuditLog(

            user=current_user.full_name,

            module=module,

            action=action,

            description=description,

            ip_address=request.remote_addr

        )

        db.session.add(log)
        db.session.commit()

    except Exception as e:

        db.session.rollback()

        print("Audit Log Error:", e)