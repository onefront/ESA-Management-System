from extensions import db


class SMSRecipient(db.Model):
    __tablename__ = "sms_recipients"

    id = db.Column(db.Integer, primary_key=True)

    sms_log_id = db.Column(
        db.Integer,
        db.ForeignKey("sms_logs.id"),
        nullable=False
    )

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id")
    )

    phone = db.Column(db.String(20))

    status = db.Column(
        db.String(20),
        default="Sent"
    )

    response = db.Column(db.Text)

    sms_log = db.relationship(
        "SMSLog",
        backref="recipients"
    )

    member = db.relationship(
        "Member"
    )