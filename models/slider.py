from datetime import datetime

from extensions import db


class Slider(db.Model):
    __tablename__ = "sliders"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    subtitle = db.Column(
        db.String(500)
    )

    image = db.Column(
        db.String(255),
        nullable=False
    )

    button_text = db.Column(
        db.String(100)
    )

    button_link = db.Column(
        db.String(255)
    )

    display_order = db.Column(
        db.Integer,
        default=1
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Slider {self.title}>"