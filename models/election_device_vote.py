from datetime import datetime

from extensions import db


class ElectionDeviceVote(db.Model):
    __tablename__ = "election_device_votes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    election_id = db.Column(
        db.Integer,
        db.ForeignKey("elections.id"),
        nullable=False
    )

    device_token = db.Column(
        db.String(128),
        nullable=False
    )

    voted_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "election_id",
            "device_token",
            name="unique_election_device_vote"
        ),
    )

    election = db.relationship(
        "Election"
    )

    def __repr__(self):
        return f"<ElectionDeviceVote {self.id}>"