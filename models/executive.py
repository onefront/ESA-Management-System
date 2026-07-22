from extensions import db


class Executive(db.Model):
    __tablename__ = "executives"
    member_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "members.id",
            ondelete="SET NULL",
            onupdate="CASCADE"
        ),
        nullable=True
    )

    member = db.relationship(
        "Member",
        backref="executive_profile"
    )
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=True
    )

    member = db.relationship(
        "Member",
        backref="executive_profile"
    )

    executive_id = db.Column(db.String(20), unique=True)

    full_name = db.Column(db.String(150), nullable=False)

    position = db.Column(db.String(100), nullable=False)

    phone = db.Column(db.String(30))

    email = db.Column(db.String(120))

    photo = db.Column(db.String(200))

    year = db.Column(db.String(20), default="2026/2027")

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )