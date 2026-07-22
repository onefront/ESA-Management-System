from extensions import db


class ElectionSettings(db.Model):

    __tablename__ = "election_settings"

    id = db.Column(db.Integer, primary_key=True)

    active_election_id = db.Column(
        db.Integer,
        db.ForeignKey("elections.id"),
        nullable=True
    )

    voting_status = db.Column(
        db.String(20),
        default="Closed"
    )
    # Open | Closed | Paused

    results_visible = db.Column(
        db.Boolean,
        default=False
    )

    active_election = db.relationship(
        "Election"
    )