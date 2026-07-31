from extensions import db
from datetime import datetime


class SMSLog(db.Model):
    __tablename__ = "sms_logs"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    message = db.Column(db.Text, nullable=False)

    recipient_count = db.Column(db.Integer, default=0)

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    provider = db.Column(
        db.String(100)
    )

    sent_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )