from datetime import datetime

from extensions import db


class AuditLog(db.Model):

    __tablename__ = "audit_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user = db.Column(
        db.String(100),
        nullable=False
    )

    module = db.Column(
        db.String(100),
        nullable=False,
        default="System"
    )

    action = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    ip_address = db.Column(
        db.String(50),
        nullable=True
    )

    action_time = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<AuditLog {self.id}>"