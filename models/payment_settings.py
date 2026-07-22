from extensions import db


class PaymentSettings(db.Model):

    __tablename__ = "payment_settings"

    id = db.Column(db.Integer, primary_key=True)

    momo_network = db.Column(
        db.String(30),
        nullable=False
    )

    momo_number = db.Column(
        db.String(30),
        nullable=False
    )

    account_name = db.Column(
        db.String(120),
        nullable=False
    )

    payment_instruction = db.Column(
        db.Text
    )

    qr_code = db.Column(
        db.String(255)
    )

    online_payment_enabled = db.Column(
        db.Boolean,
        default=True
    )