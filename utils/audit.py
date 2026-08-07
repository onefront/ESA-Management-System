from flask import request
from flask_login import current_user

from extensions import db
from models.audit_log import AuditLog


def log_activity(module, action, description=None):
    try:

        user = "System"

        if current_user.is_authenticated:
            user = current_user.full_name

        log = AuditLog(
            user=user,
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


def get_changes(old_values, new_values):
    """
    Compare two dictionaries and return a readable list of changes.
    """

    changes = []

    for field, old_value in old_values.items():

        new_value = new_values.get(field)

        old_value = "" if old_value is None else str(old_value)
        new_value = "" if new_value is None else str(new_value)

        if old_value != new_value:
            changes.append(
                f"{field}: {old_value} → {new_value}"
            )

    return changes


def log_create(module, record_name, record_id):
    """
    Log creation of a record.
    """

    log_activity(
        module=module,
        action="Created",
        description=f"{record_name} ({record_id})"
    )


def log_delete(module, record_name, record_id):
    """
    Log deletion of a record.
    """

    log_activity(
        module=module,
        action="Deleted",
        description=f"{record_name} ({record_id})"
    )


def log_update(module, record_name, record_id, old_values, new_values):
    """
    Log updates showing exactly what changed.
    """

    changes = get_changes(old_values, new_values)

    if changes:
        description = (
            f"{record_name} ({record_id}) | "
            + "; ".join(changes)
        )
    else:
        description = (
            f"{record_name} ({record_id}) | "
            "No changes detected."
        )

    log_activity(
        module=module,
        action="Updated",
        description=description
    )