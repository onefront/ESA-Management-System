from services.pdf_timetable_importer import PDFTimetableImporter

pdf = PDFTimetableImporter(
    "uploads/timetables/sample.pdf"
)

pdf.preview_tables()