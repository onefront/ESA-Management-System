from extensions import db
from datetime import datetime


class Candidate(db.Model):

    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)

    election_id = db.Column(
        db.Integer,
        db.ForeignKey("elections.id"),
        nullable=False
    )

    portfolio_id = db.Column(
        db.Integer,
        db.ForeignKey("portfolios.id"),
        nullable=False
    )

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=False
    )

    slogan = db.Column(
        db.String(255)
    )

    manifesto = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )

    date_added = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    election = db.relationship(
        "Election",
        backref=db.backref(
            "candidates",
            cascade="all, delete-orphan"
        )
    )

    portfolio = db.relationship(
        "Portfolio",
        backref=db.backref(
            "candidates",
            cascade="all, delete-orphan"
        )
    )

    member = db.relationship(
        "Member",
        backref=db.backref(
            "candidacies",
            cascade="all, delete-orphan"
        )
    )

    def __repr__(self):
        return f"<Candidate {self.member.first_name} {self.member.last_name}>"