from extensions import db


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)

    event_code = db.Column(db.String(20), unique=True)

    title = db.Column(db.String(200), nullable=False)

    venue = db.Column(db.String(200), nullable=False)

    event_date = db.Column(db.Date, nullable=False)

    event_time = db.Column(db.String(20), nullable=False)

    description = db.Column(db.Text)

    banner = db.Column(db.String(200))

    status = db.Column(
        db.String(20),
        default="Upcoming"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )