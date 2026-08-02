from docx import Document
from services.timetable_importer import TimetableImporter

print(">>> LOADED: docx_timetable_importer.py")


class DocxTimetableImporter:

    def __init__(self, filepath):
        print(">>> DocxTimetableImporter created")
        self.filepath = filepath
        self.helper = TimetableImporter(filepath)

    def import_docx(self):

        doc = Document(self.filepath)

        records = []

        for table in doc.tables:

            # Skip header row
            for row in table.rows[1:]:

                cells = [cell.text.strip() for cell in row.cells]

                if len(cells) < 8:
                    continue

                day_date = cells[0]
                time = cells[1]
                class_name = cells[2]
                course_code = cells[3]
                course_title = cells[4]
                students = cells[5]
                venue = cells[6]
                examiner = cells[7]

                programme, level = self.helper.extract_class_details(class_name)

                records.append({

                    "day": day_date,
                    "exam_date": None,

                    "start_time": None,
                    "end_time": None,

                    "programme": programme,
                    "level": level,
                    "session": "Weekend",

                    "class": class_name,

                    "course_code": course_code,
                    "course_title": course_title,

                    "students": students,

                    "venue": venue,
                    "examiner": examiner

                })

        print("=" * 80)
        print("TOTAL RECORDS:", len(records))

        for r in records[:10]:
            print(r)

        print("=" * 80)
        print("CLASS METHODS:", [m for m in dir(DocxTimetableImporter) if not m.startswith("_")])
        return records