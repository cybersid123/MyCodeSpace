"""
import os
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from PIL import Image as PILImage
from ..config import PDF_OUTPUT_DIR, COMPANY_NAME, COMPANY_LOGO

class PDFCreator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        # Add custom styles
        self.styles.add(ParagraphStyle(
            name='CenteredTitle',
            parent=self.styles['Title'],
            alignment=1,  # 0=left, 1=center, 2=right
        ))
        self.styles.add(ParagraphStyle(
            name='PersonInfo',
            parent=self.styles['Normal'],
            fontSize=12,
            leading=14,
            spaceAfter=6,
        ))
    
    def create_person_pdf(self, person, qr_code_img):
        """
        Create a PDF document for a person
        
        Args:
            person: The Person object from the database
            qr_code_img: BytesIO object with the QR code image
            
        Returns:
            Path to the created PDF file
        """
        filename = f"{person.unique_code}_{person.last_name}_{person.first_name}.pdf"
        filepath = os.path.join(PDF_OUTPUT_DIR, filename)
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Content elements
        elements = []
        
        # Add company logo if available
        if COMPANY_LOGO and os.path.exists(COMPANY_LOGO):
            logo = Image(COMPANY_LOGO, width=2*inch, height=1*inch)
            elements.append(logo)
            elements.append(Spacer(1, 12))
        
        # Title
        elements.append(Paragraph(f"{COMPANY_NAME} - Personal Identification", self.styles['CenteredTitle']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Person's photo
        if person.photo:
            # Convert binary data to image
            photo_data = BytesIO(person.photo)
            try:
                img = PILImage.open(photo_data)
                
                # Resize if necessary
                max_width, max_height = 2*inch, 2*inch
                img.thumbnail((max_width, max_height))
                
                # Save to BytesIO
                img_buffer = BytesIO()
                img.save(img_buffer, format=img.format or 'JPEG')
                img_buffer.seek(0)
                
                # Add image to PDF
                photo = Image(img_buffer, width=2*inch, height=2*inch)
                elements.append(photo)
                elements.append(Spacer(1, 0.2*inch))
            except Exception as e:
                elements.append(Paragraph(f"Error loading photo: {e}", self.styles['Normal']))
                elements.append(Spacer(1, 0.2*inch))
        
        # Person information
        elements.append(Paragraph(f"<b>Name:</b> {person.first_name} {person.last_name}", self.styles['PersonInfo']))
        elements.append(Paragraph(f"<b>Date of Birth:</b> {person.date_of_birth.strftime('%B %d, %Y')}", self.styles['PersonInfo']))
        if person.email:
            elements.append(Paragraph(f"<b>Email:</b> {person.email}", self.styles['PersonInfo']))
        if person.phone:
            elements.append(Paragraph(f"<b>Phone:</b> {person.phone}", self.styles['PersonInfo']))
        if person.address:
            elements.append(Paragraph(f"<b>Address:</b> {person.address}", self.styles['PersonInfo']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Unique code information
        elements.append(Paragraph(f"<b>Unique ID Code:</b> {person.unique_code}", self.styles['PersonInfo']))
        elements.append(Spacer(1, 0.2*inch))
        
        # QR Code
        qr_image = Image(qr_code_img, width=2*inch, height=2*inch)
        elements.append(qr_image)
        
        # Footer with generation date
        elements.append(Spacer(1, 1*inch))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.styles['Normal']))
        
        # Build the PDF
        doc.build(elements)
        
        return filepath
"""
