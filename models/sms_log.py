from datetime import datetime
from extensions import db


class SMSLog(db.Model):
    __tablename__ = "sms_logs"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=False)

    recipient_group = db.Column(db.String(100), nullable=False)
    recipient_count = db.Column(db.Integer, default=0)

    provider = db.Column(db.String(50), default="MNotify")

    campaign_id = db.Column(db.String(100))
    message_id = db.Column(db.String(100))

    credits_used = db.Column(db.Integer, default=0)

    status = db.Column(
        db.String(20),
        default="Success"
    )

    sent_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="sms_logs"
    )