from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors 
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def contract_builder(date = "1/1/1970", lessor = "Frank Jones", lessee = "Molly Doe"):

	
    # pdf.drawText(text) 
    doc = SimpleDocTemplate("example.pdf", pagesize=letter)
    styles = getSampleStyleSheet()

    content = []

    paragraph_1 = Paragraph("WATER RIGHTS LEASE AGREEMENT", styles['Heading1'])
    content.append(paragraph_1)

    paragraph_2 = Paragraph(
        "This Water Rights Lease Agreement (\"Agreement\") is made and entered into on " + date + " by and between " + lessor + " (\"Lessor\") and " + lessee + " (\"Lessee\").",
        styles['BodyText'])
    content.append(paragraph_2)

    doc.build(content)

    return doc


contract_builder()
