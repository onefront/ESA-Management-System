from extensions import db


class Department(db.Model):

    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)

    department_name = db.Column(
        db.String(150),
        nullable=False
    )

    programme_id = db.Column(
        db.Integer,
        db.ForeignKey("programmes.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )

    programme = db.relationship(
        "Programme",
        backref="departments"
    )

    def __repr__(self):
        return f"<Department {self.department_name}>"