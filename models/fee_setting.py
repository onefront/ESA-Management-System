from extensions import db
from datetime import datetime


class FeeSetting(db.Model):
    __tablename__ = "fee_settings"

    id = db.Column(db.Integer, primary_key=True)

    academic_year = db.Column(db.String(20), nullable=False)

    registration_fee = db.Column(db.Float, nullable=False, default=200)

    annual_dues = db.Column(db.Float, nullable=False, default=50)

    welfare_levy = db.Column(db.Float, nullable=False, default=0)

    other_fee = db.Column(db.Float, nullable=False, default=0)

    active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)