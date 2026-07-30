from extensions import db


class SMSSetting(db.Model):
    __tablename__ = "sms_settings"

    id = db.Column(db.Integer, primary_key=True)

    provider = db.Column(
        db.String(50),
        nullable=False,
        default="Arkesel"
    )

    api_key = db.Column(
        db.Text,
        nullable=True
    )

    sender_id = db.Column(
        db.String(20),
        nullable=True
    )

    base_url = db.Column(
        db.String(255),
        nullable=False,
        default="https://sms.arkesel.com/api/v2"
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    def __repr__(self):
        return f"<SMSSetting {self.provider}>"