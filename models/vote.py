from datetime import datetime

from extensions import db


class Vote(db.Model):

    __tablename__ = "votes"
    __table_args__ = (
        db.UniqueConstraint(
            "election_id",
            "portfolio_id",
            "member_id",
            name="unique_member_vote"
        ),
    )

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

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey("candidates.id"),
        nullable=False
    )

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=False
    )

    vote_time = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    election = db.relationship("Election")

    portfolio = db.relationship("Portfolio")

    candidate = db.relationship("Candidate")

    member = db.relationship("Member")

    def __repr__(self):
        return f"<Vote {self.id}>"