"""Vendor-specific receipt templates with pricing tables."""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle


class VendorTemplatesV2:
    """Collection of vendor receipt templates with pricing tables."""
    
    @staticmethod
    def _draw_header(c, vendor_name, x, y, font_size=20, color=colors.black):
        """Helper to draw vendor header."""
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", font_size)
        c.drawString(x, y, vendor_name)
        c.setFillColor(colors.black)
    
    @staticmethod
    def _draw_pricing_table(c, table_data, x, y, width=500):
        """
        Helper to draw a pricing table.
        
        Args:
            table_data: dict with 'name' and 'markets' list
            x, y: Position
            width: Table width
        
        Returns:
            New y position after table
        """
        # Table title
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x, y, table_data['name'])
        y -= 20
        
        # Build table data
        data = [['Market', 'Minimum (USD)', 'Reach']]
        for market in table_data['markets']:
            data.append([
                market['market'],
                f"${market['min_value_usd']:,}",
                f"{market['reach']:,}"
            ])
        
        table = Table(data, colWidths=[width*0.45, width*0.275, width*0.275])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A90E2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')])
        ]))
        
        table.wrapOn(c, width, 400)
        new_y = y - (len(data) * 22) - 10
        table.drawOn(c, x, new_y)
        return new_y - 15
    
    # Template 1: Modern Blue
    @staticmethod
    def template_modern_blue(c, data):
        """Modern Blue - Clean professional style."""
        c.setPageSize(letter)
        y = 710
        
        # Header
        VendorTemplatesV2._draw_header(c, "PREMIUM AD SOLUTIONS", 50, y, 22, colors.HexColor('#2C5AA0'))
        c.setFont("Helvetica", 9)
        c.drawString(450, y, f"Invoice #{data['transaction_id']}")
        
        y -= 25
        c.line(50, y, 550, y)
        y -= 25
        
        # Info section
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Date: {data['date']} {data['time']}")
        c.drawString(50, y-15, f"Customer: {data['customer_name']}")
        c.drawString(50, y-30, f"Company: {data['company_name']}")
        c.drawString(50, y-45, f"Campaign: {data['campaign_name']}")
        c.drawString(50, y-60, f"Payment: {data['payment_method']}")
        
        y -= 90
        
        # Draw each pricing table
        c.setFont("Helvetica-Bold", 13)
        c.drawString(50, y, "PRICING TABLES")
        y -= 25
        
        for table in data['pricing_tables']:
            y = VendorTemplatesV2._draw_pricing_table(c, table, 50, y, 500)
        
        # Totals
        y -= 15
        c.line(50, y, 550, y)
        y -= 20
        
        c.setFont("Helvetica", 10)
        c.drawString(350, y, "Subtotal:")
        c.drawString(480, y, f"${data['subtotal']:,.2f}")
        c.drawString(350, y-15, "Tax (8%):")
        c.drawString(480, y-15, f"${data['tax']:,.2f}")
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(350, y-35, "Total:")
        c.drawString(480, y-35, f"${data['total']:,.2f}")
        
        # Footer
        y -= 60
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(50, y, data['notes'])
        
        c.showPage()
    
    # Template 2: Minimal Gray
    @staticmethod
    def template_minimal_gray(c, data):
        """Minimal Gray - Simple professional style."""
        c.setPageSize(letter)
        y = 710
        
        # Header
        VendorTemplatesV2._draw_header(c, "GLOBAL MEDIA PARTNERS", 50, y, 20, colors.HexColor('#555555'))
        c.setFont("Helvetica", 8)
        c.drawString(470, y+5, f"#{data['transaction_id']}")
        c.drawString(470, y-8, data['date'])
        
        y -= 30
        c.line(50, y, 550, y)
        y -= 20
        
        # Info
        c.setFont("Helvetica", 9)
        c.drawString(50, y, f"Bill To: {data['company_name']}")
        c.drawString(50, y-12, f"Attn: {data['customer_name']}")
        c.drawString(50, y-24, f"Campaign: {data['campaign_name']}")
        
        y -= 50
        
        # Pricing tables with gray theme
        for table in data['pricing_tables']:
            y = VendorTemplatesV2._draw_pricing_table(c, table, 50, y, 500)
        
        # Totals
        y -= 20
        c.line(400, y, 550, y)
        y -= 15
        
        c.setFont("Helvetica", 9)
        c.drawString(400, y, "Subtotal:")
        c.drawString(500, y, f"${data['subtotal']:,.2f}")
        c.drawString(400, y-12, "Tax:")
        c.drawString(500, y-12, f"${data['tax']:,.2f}")
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(400, y-28, "Total Due:")
        c.drawString(500, y-28, f"${data['total']:,.2f}")
        
        c.showPage()
    
    # Template 3: Bold Orange
    @staticmethod
    def template_bold_orange(c, data):
        """Bold Orange - Eye-catching energetic style."""
        c.setPageSize(letter)
        y = 710
        
        # Header with orange
        VendorTemplatesV2._draw_header(c, "IMPACT ADVERTISING", 50, y, 24, colors.HexColor('#FF6600'))
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor('#FF6600'))
        c.drawString(450, y-5, f"INVOICE {data['transaction_id']}")
        c.setFillColor(colors.black)
        
        y -= 35
        c.setStrokeColor(colors.HexColor('#FF6600'))
        c.setLineWidth(2)
        c.line(50, y, 550, y)
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        y -= 30
        
        # Client info
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"CLIENT: {data['company_name']}")
        c.drawString(50, y-15, f"CONTACT: {data['customer_name']}")
        c.drawString(350, y, f"DATE: {data['date']}")
        c.drawString(350, y-15, f"PAYMENT: {data['payment_method']}")
        
        y -= 45
        
        # Campaign
        c.setFont("Helvetica-Bold", 9)
        c.drawString(50, y, f"CAMPAIGN: {data['campaign_name']}")
        
        y -= 30
        
        # Pricing tables
        for i, table in enumerate(data['pricing_tables']):
            y = VendorTemplatesV2._draw_pricing_table(c, table, 50, y, 500)
        
        # Summary
        y -= 20
        c.setFillColor(colors.HexColor('#FF6600'))
        c.rect(400, y-40, 150, 45, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(410, y-15, "TOTAL DUE")
        c.setFont("Helvetica-Bold", 14)
        c.drawString(410, y-32, f"${data['total']:,.2f}")
        c.setFillColor(colors.black)
        
        c.showPage()


# List of all vendor templates
VENDOR_TEMPLATES_V2 = [
    VendorTemplatesV2.template_modern_blue,
    VendorTemplatesV2.template_minimal_gray,
    VendorTemplatesV2.template_bold_orange,
]

# Vendor names corresponding to templates
VENDOR_NAMES_V2 = [
    "Premium Ad Solutions",
    "Global Media Partners",
    "Impact Advertising",
]

