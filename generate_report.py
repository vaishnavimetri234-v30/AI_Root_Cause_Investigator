
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os
from xml.sax.saxutils import escape

def generate_pdf(
    machine_id,
    temperature,
    vibration,
    pressure,
    runtime_hours,
    prediction,
    causes,
    recommendations,
    ai_report
):
    # Create reports folder if it does not exist
    os.makedirs("reports", exist_ok=True)

    # Create PDF filename
    filename = f"reports/{machine_id}_investigation_report.pdf"

    # Set up PDF document
    pdf = SimpleDocTemplate(
        filename,
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    content = []

    # Report title
    content.append(
        Paragraph("AI MACHINE FAILURE INVESTIGATION REPORT",
                  styles["Title"])
    )

    content.append(Spacer(1, 0.3 * inch))

    # Machine details
    content.append(
        Paragraph("1. Machine Details", styles["Heading2"])
    )

    machine_data = [
        ["Parameter", "Value"],
        ["Machine ID", str(machine_id)],
        ["Temperature", f"{temperature}"],
        ["Vibration", f"{vibration}"],
        ["Pressure", f"{pressure}"],
        ["Runtime Hours", f"{runtime_hours}"]
    ]

    table = Table(machine_data, colWidths=[2 * inch, 3 * inch])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8)
    ]))

    content.append(table)
    content.append(Spacer(1, 0.3 * inch))

    # ML prediction
    content.append(
        Paragraph("2. Machine Learning Prediction", styles["Heading2"])
    )
    content.append(Paragraph(str(prediction), styles["BodyText"]))
    content.append(Spacer(1, 0.2 * inch))

    # Possible causes
    content.append(
        Paragraph("3. Possible Root Causes", styles["Heading2"])
    )

    for cause in causes:
        content.append(Paragraph(f"- {cause}", styles["BodyText"]))

    content.append(Spacer(1, 0.2 * inch))

    # Recommendations
    content.append(
        Paragraph("4. Maintenance Recommendations", styles["Heading2"])
    )

    for recommendation in recommendations:
        content.append(
            Paragraph(f"- {recommendation}", styles["BodyText"])
        )

    content.append(Spacer(1, 0.2 * inch))

    # AI report
    content.append(
        Paragraph("5. AI Investigation Explanation", styles["Heading2"])
    )

    for line in ai_report.split("\n"):
        if line.strip():
            content.append(
                           Paragraph(escape(line), styles["BodyText"])
            )
            content.append(Spacer(1, 0.08 * inch))

    content.append(Spacer(1, 0.2 * inch))
    content.append(
        Paragraph(
            "Note: This is an AI-assisted preliminary investigation. "
            "Possible causes and model predictions require verification "
            "by a qualified maintenance engineer.",
            styles["Italic"]
        )
    )

    # Generate PDF
    pdf.build(content)

    print("\nPDF report generated successfully!")
    print("Saved at:", filename)

    return filename
