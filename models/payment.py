from extensions import db
from datetime import datetime


class Payment(db.Model):

    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=False
    )

    payment_type = db.Column(db.String(50))

    amount = db.Column(db.Float)

    payment_method = db.Column(db.String(30))

    reference = db.Column(db.String(100))


    date_paid = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    status = db.Column(
        db.String(20),
        nullable=False,
        default="Pending"
    )

    proof_image = db.Column(
        db.String(255),
        nullable=True
    )

    approved_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    approved_at = db.Column(
        db.DateTime,
        nullable=True
    )

    remarks = db.Column(
        db.Text,
        nullable=True
    )
    member = db.relationship(
        "Member",
        backref=db.backref(
            "payments",
            cascade="all, delete-orphan"
        )
    )