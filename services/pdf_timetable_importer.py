import re
from datetime import datetime

import pdfplumber

from services.timetable_importer import TimetableImporter


class PDFTimetableImporter:

    def __init__(self, filepath):
        self.filepath = filepath
        self.helper = TimetableImporter(filepath)

    def import_pdf(self):

        records = []

        current_day = ""
        current_time = ""
        current_course_code = ""
        current_course_title = ""
        current_venue = ""
        current_examiner = ""
        with pdfplumber.open(self.filepath) as pdf:

            for page in pdf.pages:

                tables = page.extract_tables()

                for table in tables:

                    for row in table:

                        if not row:
                            continue

                        # Convert None cells to empty strings
                        row = [
                            (cell or "").strip()
                            for cell in row
                        ]

                        # Ignore short/incomplete table rows
                        if len(row) < 8:
                            continue

                        # Skip table headers
                        header_text = " ".join(cell.upper() for cell in row)

                        if (
                                "DAY/DATE" in header_text
                                or "COURSE CODE" in header_text
                                or "COURSE TITLE" in header_text
                                or "CLASS" in header_text
                                or "NO. OF STDS" in header_text
                        ):
                            continue

                        # ---------------------------------
                        # Remember merged Day/Date
                        # ---------------------------------

                        if row[0]:
                            current_day = row[0]

                        # ---------------------------------
                        # Remember merged Time
                        # ---------------------------------

                        if row[1]:
                            current_time = row[1]

                        # ---------------------------------
                        # Extract Date
                        # ---------------------------------

                        day_text = " ".join(
                            current_day.split()
                        )

                        date_match = re.search(
                            r"\d{2}/\d{2}/\d{4}",
                            day_text
                        )

                        exam_date = None

                        if date_match:

                            try:

                                exam_date = datetime.strptime(
                                    date_match.group(),
                                    "%d/%m/%Y"
                                ).date()

                            except ValueError:
                                exam_date = None

                        # ---------------------------------
                        # Extract Day
                        # ---------------------------------

                        letters_only = re.sub(
                            r"[^A-Z]",
                            "",
                            day_text.upper()
                        )

                        if "SATURDAY" in letters_only:

                            day = "Saturday"

                        elif "SUNDAY" in letters_only:

                            day = "Sunday"

                        else:

                            day = ""

                        # ---------------------------------
                        # Extract Start/End Time
                        # ---------------------------------

                        time_text = current_time.replace(
                            "\n",
                            " "
                        )

                        time_matches = re.findall(
                            r"\d{1,2}:\d{2}\s*[ap]m",
                            time_text,
                            re.IGNORECASE
                        )

                        start_time = None
                        end_time = None

                        if len(time_matches) >= 2:

                            try:

                                start_time = datetime.strptime(
                                    time_matches[0]
                                    .replace(" ", "")
                                    .upper(),
                                    "%I:%M%p"
                                ).time()

                                end_time = datetime.strptime(
                                    time_matches[1]
                                    .replace(" ", "")
                                    .upper(),
                                    "%I:%M%p"
                                ).time()

                            except ValueError:

                                start_time = None
                                end_time = None

                        # ---------------------------------
                        # Extract remaining columns
                        # ---------------------------------
                        class_name = row[2].replace("\n", " ").strip()

                        course_code = row[3].replace("\n", " ").strip()
                        course_title = row[4].replace("\n", " ").strip()
                        students = row[5].replace("\n", " ").strip()
                        venue = row[6].replace("\n", " ").strip()
                        examiner = row[7].replace("\n", " ").strip()

                        # Carry forward merged values

                        if course_code:
                            current_course_code = course_code
                        else:
                            course_code = current_course_code

                        if course_title:
                            current_course_title = course_title
                        else:
                            course_title = current_course_title

                        if venue:
                            current_venue = venue
                        else:
                            venue = current_venue

                        if examiner:
                            current_examiner = examiner
                        else:
                            examiner = current_examiner
                        # Ignore rows without class information
                        if not class_name:
                            continue

                        # ---------------------------------
                        # Programme and Level
                        # ---------------------------------

                        programme, level = (
                            self.helper.extract_class_details(
                                class_name
                            )
                        )

                        # ---------------------------------
                        # Add Record
                        # ---------------------------------
                        if exam_date is None:
                            continue
                        records.append({

                            "day": day,

                            "exam_date": exam_date,

                            "start_time": start_time,

                            "end_time": end_time,

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

        return records