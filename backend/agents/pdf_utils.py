from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import base64

def generate_pdf(name: str, decision: str, loan_amount: float):
    """
    Generates a simple PDF sanction letter for the loan decision.
    Returns base64-encoded PDF bytes.
    """

    # Create an in-memory PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 100, "Nexus Loan Sanction Letter")

    # Applicant details
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, f"Applicant Name: {name}")
    c.drawString(100, height - 170, f"Loan Amount: ₹{loan_amount:,.2f}")
    c.drawString(100, height - 190, f"Decision: {decision}")

    # Conditional text
    if decision.lower() == "approved":
        msg = (
            "Congratulations! Your loan application has been approved."
            " The sanctioned amount will be credited soon."
        )
    else:
        msg = (
            "We regret to inform you that your loan application was not approved at this time."
            " Please review your credit and income details for improvement."
        )

    c.drawString(100, height - 220, msg)

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(100, 100, "Thank you for choosing Nexus Loan Services.")
    c.drawString(100, 85, "This is a system-generated document. No signature required.")

    # Finalize PDF
    c.showPage()
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()

    # Return as base64 for API
    return base64.b64encode(pdf_bytes).decode("utf-8")
