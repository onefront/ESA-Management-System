from extensions import db
from datetime import datetime


class Election(db.Model):

    __tablename__ = "elections"

    id = db.Column(db.Integer, primary_key=True)

    election_name = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    start_date = db.Column(
        db.DateTime,
        nullable=False
    )

    end_date = db.Column(
        db.DateTime,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )
    # Pending
    # Active
    # Closed

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Election {self.election_name}>"