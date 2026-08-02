from extensions import db


class Programme(db.Model):

    __tablename__ = "programmes"

    id = db.Column(db.Integer, primary_key=True)

    # Full programme name
    programme_name = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    # Programme abbreviation
    programme_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("faculties.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )

    def __repr__(self):
        return f"<Programme {self.programme_code} - {self.programme_name}>"