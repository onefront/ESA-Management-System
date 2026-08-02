from services.pdf_timetable_importer import PDFTimetableImporter

pdf = PDFTimetableImporter(
    r"uploads/timetables/FINAL END OF  SEMESTER 2  EXAMS TIMETABLE FOR WEEKEND PROG 2025.2026 (1).pdf"
)

records = pdf.import_pdf()

print("=" * 80)
print("TOTAL RECORDS:", len(records))

for r in records[:20]:
    print(r)