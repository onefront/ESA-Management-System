import os

from io import BytesIO

from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from flask import current_app


def generate_member_id_pdf(member):

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    width, height = pdf._pagesize

    # -----------------------------
    # Background
    # -----------------------------
    pdf.setFillColor(HexColor("#0B4EA2"))
    pdf.rect(0, 0, width, height, fill=1)

    # -----------------------------
    # Gold Header
    # -----------------------------
    pdf.setFillColor(HexColor("#FFD700"))
    pdf.rect(0, height - 90, width, 90, fill=1)

    # -----------------------------
    # Logo
    # -----------------------------
    logo = os.path.join(
        current_app.static_folder,
        "images",
        "logo.png"
    )

    if os.path.exists(logo):

        pdf.drawImage(
            ImageReader(logo),
            40,
            height - 80,
            width=55,
            height=55,
            mask="auto"
        )

    # -----------------------------
    # Title
    # -----------------------------
    pdf.setFillColor(HexColor("#0B4EA2"))
    pdf.setFont("Helvetica-Bold", 20)

    pdf.drawString(
        110,
        height - 45,
        "EXECUTIVE STUDENT ASSOCIATION"
    )

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        110,
        height - 65,
        "Together We Build"
    )

    # -----------------------------
    # Passport
    # -----------------------------
    if member.passport:

        passport = os.path.join(
            current_app.static_folder,
            "uploads",
            member.passport
        )

        if os.path.exists(passport):

            pdf.drawImage(
                ImageReader(passport),
                45,
                height - 270,
                width=110,
                height=130,
                mask="auto"
            )

    # -----------------------------
    # Member Details
    # -----------------------------
    x = 200
    y = height - 150

    pdf.setFillColor(HexColor("#FFFFFF"))

    pdf.setFont("Helvetica-Bold", 22)

    pdf.drawString(
        x,
        y,
        f"{member.first_name.title()} {member.last_name.title()}"
    )

    pdf.setFont("Helvetica", 13)

    y -= 40

    details = [

        ("ESA ID", member.esa_id),

        ("Index Number", member.student_id),

        ("Programme", member.programme or "Not Completed"),

        ("Level", str(member.level)),

        ("Session", member.session),

        ("Issued", member.date_registered.strftime("%d %b %Y")),

        ("Expires", member.expiry_date.strftime("%d %b %Y"))

    ]

    for label, value in details:

        pdf.drawString(
            x,
            y,
            f"{label}: {value}"
        )

        y -= 25

    # -----------------------------
    # QR Code
    # -----------------------------
    qr = os.path.join(
        current_app.static_folder,
        "qrcodes",
        f"{member.esa_id}.png"
    )

    if os.path.exists(qr):

        pdf.drawImage(
            ImageReader(qr),
            width - 120,
            80,
            width=80,
            height=80
        )

    pdf.setFont("Helvetica", 9)

    pdf.drawString(
        width - 125,
        65,
        "Scan to Verify"
    )

    pdf.save()

    buffer.seek(0)

    return buffer