from extensions import db

class Faculty(db.Model):

    __tablename__ = "faculties"

    id = db.Column(db.Integer, primary_key=True)

    faculty_name = db.Column(db.String(150), unique=True, nullable=False)

    status = db.Column(db.String(20), default="Active")

    programmes = db.relationship(
        "Programme",
        backref="faculty",
        lazy=True
    )

    def __repr__(self):
        return f"<Faculty {self.faculty_name}>"