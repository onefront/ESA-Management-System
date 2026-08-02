from extensions import db


class Timetable(db.Model):
    __tablename__ = "timetables"

    id = db.Column(db.Integer, primary_key=True)

    timetable_type = db.Column(db.String(20), nullable=False)

    academic_year = db.Column(db.String(20), nullable=False)

    semester = db.Column(db.String(50), nullable=False)

    programme = db.Column(db.String(150), nullable=False)

    level = db.Column(db.String(20), nullable=False)

    session = db.Column(db.String(20), nullable=False)

    exam_date = db.Column(db.Date, nullable=False)

    day = db.Column(db.String(20), nullable=False)

    start_time = db.Column(db.Time, nullable=False)

    end_time = db.Column(db.Time, nullable=False)

    course_code = db.Column(db.String(30), nullable=False)

    course_title = db.Column(db.String(250), nullable=False)

    venue = db.Column(db.String(150), nullable=False)

    examiner = db.Column(db.String(200))

    status = db.Column(db.String(20))

    created_at = db.Column(db.DateTime)
