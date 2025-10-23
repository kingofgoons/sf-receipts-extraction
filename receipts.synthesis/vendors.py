"""Vendor-specific receipt templates with different styles."""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle


class VendorTemplates:
    """Collection of 20+ different vendor receipt templates."""
    
    @staticmethod
    def _draw_header(c, vendor_name, x, y, font_size=20, color=colors.black):
        """Helper to draw vendor header."""
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", font_size)
        c.drawString(x, y, vendor_name)
        c.setFillColor(colors.black)
    
    @staticmethod
    def _draw_line_items(c, items, x, y, width=500):
        """Helper to draw line items as a table."""
        data = [['Description', 'Qty', 'Unit Price', 'Total']]
        for item in items:
            data.append([
                item['description'],
                str(item['quantity']),
                f"${item['unit_price']:.2f}",
                f"${item['total']:.2f}"
            ])
        
        table = Table(data, colWidths=[width*0.5, width*0.15, width*0.15, width*0.2])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        table.wrapOn(c, width, 400)
        table.drawOn(c, x, y - len(data) * 25)
        return y - len(data) * 25 - 20
    
    # Template 1: Modern Minimalist
    @staticmethod
    def template_1_techads_pro(c, data):
        """TechAds Pro - Modern minimalist style."""
        c.setPageSize(letter)
        y = 710  # Adjusted from 750 to prevent header cropping
        
        # Header with blue accent
        VendorTemplates._draw_header(c, "TECHADS PRO", 50, y, 24, colors.HexColor('#0066CC'))
        c.setFont("Helvetica", 10)
        c.drawString(450, y, f"Receipt #{data['transaction_id']}")
        
        y -= 30
        c.line(50, y, 550, y)
        y -= 30
        
        # Info section
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Date: {data['date']} {data['time']}")
        c.drawString(50, y-15, f"Customer: {data['customer_name']}")
        c.drawString(50, y-30, f"Company: {data['company_name']}")
        c.drawString(50, y-45, f"Campaign: {data['campaign_name']}")
        
        y -= 80
        
        # Line items
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Paragraph format
        y -= 15
        details = data['campaign_details']
        details = data['campaign_details']
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.HexColor('#0066CC'))
        c.drawString(50, y, "CAMPAIGN DETAILS")
        c.setFillColor(colors.black)
        y -= 15
        
        c.setFont("Helvetica", 8)
        # Paragraph style description
        campaign_text = f"{details['content_types']} campaign from {details['campaign_start_date']} to {details['campaign_end_date']}. "
        campaign_text += f"Budget: ${details['daily_budget']:.0f}/day. Pricing: {details['pricing_model']} at {details['rate_description']}. "
        campaign_text += f"Metrics: CPM ${details['cpm']:.2f}, CTR {details['ctr']:.1f}%, Bounce {details['bounce_rate']:.1f}%. "
        campaign_text += f"Targeting: {details['geo_targets']}, {details['age_range']}, {details['devices']}."
        
        # Wrap text
        from reportlab.platypus import Paragraph
        from reportlab.lib.styles import ParagraphStyle
        style = ParagraphStyle('campaign', fontSize=7, leading=9)
        para = Paragraph(campaign_text, style)
        para.wrapOn(c, 500, 100)
        para.drawOn(c, 50, y - 40)
        y -= 50
        
        # Totals
        y -= 10
        c.setFont("Helvetica", 10)
        c.drawString(400, y, "Subtotal:")
        c.drawString(500, y, f"${data['subtotal']:.2f}")
        c.drawString(400, y-15, f"Tax ({data['tax_rate']*100:.1f}%):")
        c.drawString(500, y-15, f"${data['tax']:.2f}")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y-35, "TOTAL:")
        c.drawString(500, y-35, f"${data['total']:.2f}")
    
    # Template 2: Classic Formal
    @staticmethod
    def template_2_admaster_global(c, data):
        """AdMaster Global - Classic formal style."""
        c.setPageSize(letter)
        
        # Header box (adjusted to prevent cropping - was 730+92=822, now 700+92=792)
        c.setFillColor(colors.HexColor('#1a1a1a'))
        c.rect(0, 700, 612, 92, fill=True, stroke=False)  # Adjusted from 730 to 700
        
        c.setFillColor(colors.white)
        c.setFont("Times-Bold", 28)
        c.drawString(50, 750, "AdMaster Global")  # Adjusted from 780 to 750
        c.setFont("Times-Roman", 10)
        c.drawString(50, 730, "Premium Advertising Solutions")  # Adjusted from 760 to 730
        c.drawString(50, 715, "www.admasterglobal.com | support@admasterglobal.com")  # Adjusted from 745 to 715
        
        c.setFillColor(colors.black)
        y = 670  # Adjusted from 700 to 670
        
        # Receipt info box
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "RECEIPT")
        c.setFont("Helvetica", 10)
        c.drawString(50, y-20, f"Receipt #: {data['transaction_id']}")
        c.drawString(50, y-35, f"Date: {data['date']}")
        c.drawString(50, y-50, f"Payment Method: {data['payment_method']}")
        
        c.drawString(350, y-20, f"Customer: {data['customer_name']}")
        c.drawString(350, y-35, f"Company: {data['company_name']}")
        
        y -= 90
        
        # Campaign info
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Campaign:")
        c.setFont("Helvetica", 10)
        c.drawString(120, y, data['campaign_name'])
        
        y -= 30
        
        # Line items
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Individual line items format
        y -= 15
        details = data['campaign_details']
        c.setFont("Helvetica-Bold", 9)
        c.drawString(50, y, "CAMPAIGN DETAILS:")
        y -= 14
        
        c.setFont("Helvetica", 8)
        c.drawString(50, y, f"CPM: ${details['cpm']:.2f}")
        c.drawString(150, y, f"CTR: {details['ctr']:.1f}%")
        c.drawString(250, y, f"Bounce Rate: {details['bounce_rate']:.1f}%")
        y -= 10
        c.drawString(50, y, f"Content: {details['content_types']}")
        c.drawString(250, y, f"Model: {details['pricing_model']}")
        y -= 10
        c.drawString(50, y, f"Period: {details['campaign_start_date']} to {details['campaign_end_date']}")
        y -= 10
        c.drawString(50, y, f"Budget: ${details['daily_budget']:.0f}/day (${details['total_budget']:,.0f} total)")
        y -= 10
        c.drawString(50, y, f"Targeting: {details['geo_targets']}, {details['age_range']}")
        y -= 15
        
        # Totals in a box
        y -= 10
        c.rect(380, y-55, 170, 55)
        c.setFont("Helvetica", 10)
        c.drawString(390, y-20, "Subtotal:")
        c.drawString(500, y-20, f"${data['subtotal']:.2f}")
        c.drawString(390, y-35, "Tax:")
        c.drawString(500, y-35, f"${data['tax']:.2f}")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(390, y-50, "Total:")
        c.drawString(500, y-50, f"${data['total']:.2f}")
    
    # Template 3: Colorful Creative
    @staticmethod
    def template_3_creative_campaigns(c, data):
        """Creative Campaigns - Colorful creative style."""
        c.setPageSize(letter)
        
        # Colorful header
        c.setFillColor(colors.HexColor('#FF6B35'))
        c.rect(0, 720, 612, 62, fill=True, stroke=False)  # Adjusted from 760 to prevent cropping
        
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(306, 745, "Creative Campaigns")  # Adjusted from 785
        c.setFont("Helvetica", 11)
        c.drawCentredString(306, 728, "Where Ideas Come to Life")  # Adjusted from 768
        
        c.setFillColor(colors.black)
        y = 690  # Adjusted from 730
        
        # Receipt number in colored box
        c.setFillColor(colors.HexColor('#FFE66D'))
        c.rect(50, y-25, 500, 25, fill=True, stroke=True)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y-18, f"Receipt: {data['transaction_id']} | {data['date']} | {data['customer_name']}")
        
        y -= 50
        
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Campaign: {data['campaign_name']}")
        c.drawString(50, y-15, f"Company: {data['company_name']}")
        
        y -= 40
        
        # Line items
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Bullet list format
        y -= 15
        details = data['campaign_details']
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor('#FF6B35'))
        c.drawString(50, y, "• CAMPAIGN INFO")
        c.setFillColor(colors.black)
        y -= 12
        
        c.setFont("Helvetica", 8)
        c.drawString(55, y, f"• {details['content_types']} | {details['pricing_model']} @ {details['rate_description']}")
        y -= 9
        c.drawString(55, y, f"• Period: {details['campaign_duration_days']} days | Budget ${details['total_budget']:,.0f}")
        y -= 9
        c.drawString(55, y, f"• Performance: CPM ${details['cpm']:.2f} | CTR {details['ctr']:.1f}% | Bounce {details['bounce_rate']:.1f}%")
        y -= 9
        c.drawString(55, y, f"• Target: {details['target_impressions']:,} impressions, {details['target_clicks']:,} clicks")
        y -= 9
        c.drawString(55, y, f"• Reach: {details['geo_targets']} | {details['age_range']} on {details['devices']}")
        y -= 12
        
        # Totals with colored background
        y -= 10
        c.setFillColor(colors.HexColor('#4ECDC4'))
        c.rect(380, y-60, 170, 60, fill=True, stroke=True)
        
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(390, y-20, "Subtotal:")
        c.drawString(500, y-20, f"${data['subtotal']:.2f}")
        c.drawString(390, y-35, "Tax:")
        c.drawString(500, y-35, f"${data['tax']:.2f}")
        c.setFont("Helvetica-Bold", 14)
        c.drawString(390, y-52, "TOTAL:")
        c.drawString(500, y-52, f"${data['total']:.2f}")
    
    # Template 4: Simple Invoice Style
    @staticmethod
    def template_4_digital_reach(c, data):
        """Digital Reach - Simple invoice style."""
        c.setPageSize(letter)
        y = 710  # Adjusted from 780 to prevent header cropping
        
        c.setFont("Helvetica-Bold", 22)
        c.drawString(50, y, "Digital Reach")
        c.setFont("Helvetica", 10)
        c.drawString(50, y-15, "Digital Marketing Excellence")
        
        c.setFont("Helvetica-Bold", 16)
        c.drawRightString(550, y, "RECEIPT")
        c.setFont("Helvetica", 10)
        c.drawRightString(550, y-15, data['transaction_id'])
        c.drawRightString(550, y-30, data['date'])
        
        y -= 60
        c.line(50, y, 550, y)
        y -= 20
        
        # Billing info
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "BILL TO:")
        c.setFont("Helvetica", 10)
        c.drawString(50, y-15, data['company_name'])
        c.drawString(50, y-30, data['customer_name'])
        c.drawString(50, y-45, data['email'])
        
        y -= 70
        
        # Line items
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Box with key metrics
        y -= 15
        details = data['campaign_details']
        c.setStrokeColor(colors.grey)
        c.rect(50, y-60, 500, 60)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(55, y-12, "CAMPAIGN METRICS")
        c.setFont("Helvetica", 8)
        c.drawString(55, y-22, f"CPM: ${details['cpm']:.2f} | CTR: {details['ctr']:.1f}% | Bounce: {details['bounce_rate']:.1f}%")
        c.drawString(55, y-32, f"{details['content_types']} • {details['campaign_duration_days']} days • ${details['daily_budget']:.0f}/day")
        c.drawString(55, y-42, f"Period: {details['campaign_start_date']} to {details['campaign_end_date']}")
        c.drawString(55, y-52, f"{details['pricing_model']} • {details['geo_targets']}")
        y -= 70
        
        c.line(350, y, 550, y)
        
        # Totals
        c.setFont("Helvetica", 10)
        c.drawString(400, y-15, "Subtotal:")
        c.drawRightString(545, y-15, f"${data['subtotal']:.2f}")
        c.drawString(400, y-30, "Tax:")
        c.drawRightString(545, y-30, f"${data['tax']:.2f}")
        c.drawString(50, y, f"Campaign Period: {details['campaign_start_date']} to {details['campaign_end_date']}")
        
        y -= 12
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y-50, "TOTAL DUE:")
        c.drawRightString(545, y-50, f"${data['total']:.2f}")
    
    # Template 5: Bold & Modern
    @staticmethod
    def template_5_apex_media(c, data):
        """Apex Media - Bold and modern style."""
        c.setPageSize(letter)
        
        # Bold diagonal accent (adjusted to prevent cropping)
        c.setFillColor(colors.HexColor('#8B5CF6'))
        c.saveState()
        c.translate(0, 760)  # Adjusted from 800 to 760
        c.rotate(-15)
        c.rect(-100, -50, 400, 100, fill=True, stroke=False)
        c.restoreState()
        
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 30)
        c.drawString(50, 745, "APEX")  # Adjusted from 785 to 745
        c.drawString(50, 720, "MEDIA")  # Adjusted from 760 to 720
        
        c.setFillColor(colors.black)
        y = 680  # Adjusted from 720 to 680
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"RECEIPT #{data['transaction_id']}")
        c.setFont("Helvetica", 10)
        c.drawString(50, y-18, f"{data['date']} at {data['time']}")
        
        c.drawString(350, y, f"Client: {data['company_name']}")
        c.drawString(350, y-18, f"Contact: {data['customer_name']}")
        
        y -= 50
        
        c.setFillColor(colors.HexColor('#8B5CF6'))
        c.rect(50, y-5, 500, 2, fill=True, stroke=False)
        c.setFillColor(colors.black)
        
        y -= 25
        
        # Line items
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Single-line compact format
        y -= 15
        details = data['campaign_details']
        c.setFont("Helvetica-Bold", 8)
        c.drawString(50, y, "CAMPAIGN:")
        c.setFont("Helvetica", 8)
        y -= 10
        compact = f"{details['content_types']} | {details['campaign_start_date']} to {details['campaign_end_date']} | CPM ${details['cpm']:.2f} CTR {details['ctr']:.1f}% | {details['geo_targets']}"
        c.drawString(50, y, compact)
        y -= 12
        
        # Totals
        y -= 10
        c.setFont("Helvetica", 11)
        c.drawString(400, y, "Subtotal:")
        c.drawString(500, y, f"${data['subtotal']:.2f}")
        c.drawString(400, y-18, "Tax:")
        c.drawString(500, y-18, f"${data['tax']:.2f}")
        
        c.setFillColor(colors.HexColor('#8B5CF6'))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(400, y-40, "TOTAL:")
        c.drawString(500, y-40, f"${data['total']:.2f}")
    
    # Template 6-20: Additional templates with variations
    @staticmethod
    def template_6_social_boost(c, data):
        """Social Boost - Social media focused style."""
        c.setPageSize(letter)
        
        # Gradient-like header with multiple colors (adjusted to prevent cropping)
        c.setFillColor(colors.HexColor('#E91E63'))
        c.rect(0, 730, 204, 52, fill=True, stroke=False)  # Adjusted from 770
        c.setFillColor(colors.HexColor('#9C27B0'))
        c.rect(204, 730, 204, 52, fill=True, stroke=False)  # Adjusted from 770
        c.setFillColor(colors.HexColor('#3F51B5'))
        c.rect(408, 730, 204, 52, fill=True, stroke=False)  # Adjusted from 770
        
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(306, 750, "Social Boost")  # Adjusted from 790
        
        c.setFillColor(colors.black)
        y = 700  # Adjusted from 740
        
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Receipt: {data['transaction_id']}")
        c.drawString(50, y-15, f"Date: {data['date']}")
        c.drawString(300, y, f"Customer: {data['customer_name']}")
        c.drawString(300, y-15, f"Campaign: {data['campaign_name']}")
        
        y -= 45
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Colored inline format
        y -= 15
        details = data['campaign_details']
        c.setFillColor(colors.HexColor('#FFE66D'))
        c.rect(50, y-38, 500, 38, fill=True, stroke=False)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(55, y-10, f"Campaign: {details['content_types']} • CPM ${details['cpm']:.2f} CTR {details['ctr']:.1f}% Bounce {details['bounce_rate']:.1f}%")
        c.drawString(55, y-20, f"Period: {details['campaign_start_date']} to {details['campaign_end_date']}")
        c.drawString(55, y-30, f"Budget: ${details['daily_budget']:.0f}/day • {details['pricing_model']} • {details['geo_targets']}, {details['age_range']}")
        y -= 45
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(400, y, "Total:")
        c.drawString(500, y, f"${data['total']:.2f}")
    
    @staticmethod
    def template_7_prime_ads(c, data):
        """Prime Ads - Premium gold accent style."""
        c.setPageSize(letter)
        
        # Gold header (adjusted to prevent cropping - box must fit within page)
        c.setFillColor(colors.HexColor('#FFD700'))
        c.rect(0, 678, 612, 72, fill=True, stroke=False)  # Adjusted from 750 to 678 (750+72=822 was above page edge)
        
        c.setFillColor(colors.HexColor('#1a1a1a'))
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(306, 713, "PRIME ADS")  # Adjusted from 785 to 713
        c.setFont("Helvetica", 11)
        c.drawCentredString(306, 693, "Elite Advertising Services")  # Adjusted from 765 to 693
        
        c.setFillColor(colors.black)
        y = 648  # Adjusted from 720 to 648
        
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Receipt #: {data['transaction_id']}")
        c.drawString(50, y-15, f"Date: {data['date']}")
        c.drawString(350, y, f"Client: {data['company_name']}")
        
        y -= 45
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Vertical key-value pairs
        y -= 15
        details = data['campaign_details']
        c.setFont("Courier-Bold", 8)
        c.drawString(50, y, "CAMPAIGN DATA:")
        y -= 12
        c.setFont("Courier", 8)
        c.drawString(50, y, f"Type........: {details['content_types']}")
        y -= 8
        c.drawString(50, y, f"Start-Date..: {details['campaign_start_date']}")
        y -= 8
        c.drawString(50, y, f"End-Date....: {details['campaign_end_date']}")
        y -= 8
        c.drawString(50, y, f"CPM.........: ${details['cpm']:.2f}")
        y -= 8
        c.drawString(50, y, f"CTR.........: {details['ctr']:.1f}%")
        y -= 8
        c.drawString(50, y, f"Bounce......: {details['bounce_rate']:.1f}%")
        y -= 8
        c.drawString(50, y, f"Budget......: ${details['daily_budget']:.0f}/day")
        y -= 8
        c.drawString(50, y, f"Geography...: {details['geo_targets']}")
        y -= 15
        
        c.setFillColor(colors.HexColor('#FFD700'))
        c.rect(380, y-45, 170, 45, fill=True, stroke=True)
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(390, y-25, "TOTAL:")
        c.drawString(490, y-25, f"${data['total']:.2f}")
    
    @staticmethod
    def template_8_click_velocity(c, data):
        """Click Velocity - Fast and dynamic style."""
        c.setPageSize(letter)
        y = 710  # Adjusted from 790 to prevent header cropping
        
        c.setFont("Helvetica-Bold", 26)
        c.setFillColor(colors.HexColor('#00BCD4'))
        c.drawString(50, y, "CLICK")
        c.setFillColor(colors.HexColor('#FF5722'))
        c.drawString(160, y, "VELOCITY")
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 9)
        c.drawString(50, y-15, "Lightning Fast Results")
        
        y -= 40
        
        # Angled line
        c.setStrokeColor(colors.HexColor('#00BCD4'))
        c.setLineWidth(3)
        c.line(50, y, 550, y-10)
        c.setLineWidth(1)
        c.setStrokeColor(colors.black)
        
        y -= 30
        
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Receipt: {data['transaction_id']} | {data['date']}")
        c.drawString(50, y-15, f"Customer: {data['customer_name']}")
        
        y -= 40
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Metrics-first format
        y -= 15
        details = data['campaign_details']
        c.setFont("Helvetica-Bold", 9)
        c.drawString(50, y, f"CPM: ${details['cpm']:.2f}")
        c.drawString(150, y, f"CTR: {details['ctr']:.1f}%")
        c.drawString(250, y, f"BOUNCE: {details['bounce_rate']:.1f}%")
        y -= 12
        c.setFont("Helvetica", 8)
        c.drawString(50, y, f"{details['content_types']} • {details['campaign_start_date']} to {details['campaign_end_date']}")
        y -= 10
        c.drawString(50, y, f"${details['daily_budget']:.0f}/day • {details['pricing_model']} • {details['geo_targets']}")
        y -= 12
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y, "TOTAL:")
        c.drawString(500, y, f"${data['total']:.2f}")
    
    @staticmethod
    def template_9_brand_builders(c, data):
        """Brand Builders - Professional corporate style."""
        c.setPageSize(letter)
        
        # Corporate header with border (adjusted to prevent cropping - was 740+82=822)
        c.setStrokeColor(colors.HexColor('#2C3E50'))
        c.setLineWidth(3)
        c.rect(40, 710, 532, 82, fill=False, stroke=True)  # Adjusted from 740 to 710 (now 710+82=792)
        
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(306, 760, "BRAND BUILDERS")  # Adjusted from 790 to 760
        c.setFont("Helvetica", 10)
        c.drawCentredString(306, 745, "Building Tomorrow's Brands Today")  # Adjusted from 775 to 745
        c.drawCentredString(306, 725, f"Receipt #{data['transaction_id']} | {data['date']}")  # Adjusted from 755 to 725
        
        y = 680  # Adjusted from 710 to 680
        
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Billed To: {data['company_name']}")
        c.drawString(50, y-15, f"Attention: {data['customer_name']}")
        c.drawString(50, y-30, f"Campaign: {data['campaign_name']}")
        
        y -= 60
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Boxed table format
        y -= 15
        details = data['campaign_details']
        c.setStrokeColor(colors.HexColor('#2C3E50'))
        c.setLineWidth(2)
        c.rect(50, y-65, 500, 65)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(55, y-12, "CAMPAIGN")
        c.setFont("Helvetica", 8)
        c.drawString(55, y-22, f"Content: {details['content_types']} | Display: {details['display_formats'][:30]}...")
        c.drawString(55, y-30, f"Period: {details['campaign_start_date']} to {details['campaign_end_date']}")
        c.drawString(55, y-38, f"Metrics: CPM ${details['cpm']:.2f} | CTR {details['ctr']:.1f}% | Bounce {details['bounce_rate']:.1f}%")
        c.drawString(55, y-46, f"Budget: ${details['daily_budget']:.0f}/day for {details['campaign_duration_days']} days")
        c.drawString(55, y-54, f"Targeting: {details['geo_targets'][:40]}, {details['age_range']}, {details['devices']}")
        y -= 75
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(400, y, "Amount Due:")
        c.drawString(500, y, f"${data['total']:.2f}")
    
    @staticmethod
    def template_10_viral_marketing(c, data):
        """Viral Marketing - Trendy and energetic style."""
        c.setPageSize(letter)
        
        # Energetic zigzag background (adjusted to prevent cropping - max was 822, now 780)
        c.setFillColor(colors.HexColor('#FF1744'))
        points = [(0, 768), (100, 790), (200, 768), (300, 790), (400, 768), (500, 790), (612, 768), (612, 718), (0, 718)]
        # Adjusted all y values: 800→768, 822→790, 750→718
        p = c.beginPath()
        p.moveTo(points[0][0], points[0][1])
        for x, y in points[1:]:
            p.lineTo(x, y)
        p.close()
        c.drawPath(p, fill=True, stroke=False)
        
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 26)
        c.drawString(50, 748, "VIRAL MARKETING")  # Adjusted from 780 to 748
        
        c.setFillColor(colors.black)
        y = 688  # Adjusted from 720 to 688
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, f"Receipt: {data['transaction_id']}")
        c.setFont("Helvetica", 10)
        c.drawString(50, y-15, f"Date: {data['date']}")
        c.drawString(50, y-30, f"Client: {data['company_name']}")
        
        y -= 55
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Hashtag style format
        y -= 15
        details = data['campaign_details']
        c.setFont("Helvetica-BoldOblique", 8)
        c.setFillColor(colors.HexColor('#FF1744'))
        hashtags = f"#{details['content_types'].replace(' ', '')} #CPM{details['cpm']:.0f} #CTR{details['ctr']:.1f} #Bounce{details['bounce_rate']:.0f}"
        c.drawString(50, y, hashtags)
        y -= 10
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.black)
        c.drawString(50, y, f"Campaign: {details['campaign_start_date']} to {details['campaign_end_date']} • ${details['daily_budget']:.0f}/day • {details['pricing_model']}")
        y -= 10
        c.drawString(50, y, f"{details['campaign_duration_days']} days • {details['geo_targets']}")
        y -= 12
        
        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(colors.HexColor('#FF1744'))
        c.drawString(400, y, "TOTAL:")
        c.drawString(490, y, f"${data['total']:.2f}")
    
    @staticmethod
    def template_11_metric_masters(c, data):
        """Metric Masters - Data-focused analytical style."""
        c.setPageSize(A4)
        
        c.setFont("Courier-Bold", 20)
        c.drawString(50, 730, "METRIC MASTERS")  # Adjusted from 800
        c.setFont("Courier", 10)
        c.drawString(50, 715, "Data-Driven Advertising")  # Adjusted from 785
        
        y = 690  # Adjusted from 760
        
        # Table-like info
        c.setFont("Courier", 9)
        c.drawString(50, y, f"RECEIPT_ID    : {data['transaction_id']}")
        c.drawString(50, y-15, f"DATE          : {data['date']}")
        c.drawString(50, y-30, f"TIME          : {data['time']}")
        c.drawString(50, y-45, f"CLIENT        : {data['company_name']}")
        c.drawString(50, y-60, f"CONTACT       : {data['customer_name']}")
        
        y -= 90
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y, 450)
        
        # Campaign details - Code/data format
        y -= 15
        details = data['campaign_details']
        c.setFont("Courier-Bold", 8)
        c.drawString(50, y, "[ CAMPAIGN_METRICS ]")
        y -= 10
        c.setFont("Courier", 8)
        c.drawString(50, y, f"  start_date.: {details['campaign_start_date']}")
        y -= 8
        c.drawString(50, y, f"  end_date...: {details['campaign_end_date']}")
        y -= 8
        c.drawString(50, y, f"  cpm........: {details['cpm']:.2f}")
        y -= 8
        c.drawString(50, y, f"  ctr........: {details['ctr']:.1f}")
        y -= 8
        c.drawString(50, y, f"  bounce.....: {details['bounce_rate']:.1f}")
        y -= 8
        c.drawString(50, y, f"  budget/day.: {details['daily_budget']:.0f}")
        y -= 8
        c.drawString(50, y, f"  type.......: {details['content_types']}")
        y -= 8
        c.drawString(50, y, f"  geography..: {details['geo_targets'][:30]}")
        y -= 15
        
        c.setFont("Courier-Bold", 11)
        c.drawString(350, y, "TOTAL_AMOUNT  :")
        c.drawString(470, y, f"${data['total']:.2f}")
    
    @staticmethod
    def template_12_ad_genius(c, data):
        """Ad Genius - Smart and sleek style."""
        c.setPageSize(letter)
        
        # Sleek header (adjusted to prevent cropping)
        c.setFillColor(colors.HexColor('#6200EA'))
        c.rect(0, 740, 300, 42, fill=True, stroke=False)  # Adjusted from 780
        
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(50, 755, "Ad Genius")  # Adjusted from 795
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 9)
        c.drawString(320, 765, f"Receipt: {data['transaction_id']}")  # Adjusted from 805
        c.drawString(320, 752, f"Date: {data['date']}")  # Adjusted from 792
        
        y = 710  # Adjusted from 750
        
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Customer: {data['customer_name']}")
        c.drawString(50, y-15, f"Company: {data['company_name']}")
        
        y -= 40
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Minimal badges format
        y -= 15
        details = data['campaign_details']
        c.setFont("Helvetica", 8)
        badges = f"[{details['content_types']}] [CPM: ${details['cpm']:.2f}] [CTR: {details['ctr']:.1f}%] [Bounce: {details['bounce_rate']:.1f}%] [{details['pricing_model']}]"
        c.drawString(50, y, badges)
        y -= 8
        c.drawString(50, y, f"[{details['campaign_start_date']}] to [{details['campaign_end_date']}] • [${details['daily_budget']:.0f}/day] [{details['geo_targets'][:30]}]")
        y -= 12
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y, "Total:")
        c.drawString(500, y, f"${data['total']:.2f}")
    
    @staticmethod
    def template_13_campaign_central(c, data):
        """Campaign Central - Organized grid style."""
        c.setPageSize(letter)
        
        # Grid header (properly aligned within boundaries)
        c.setStrokeColor(colors.HexColor('#009688'))
        c.setLineWidth(2)
        c.rect(45, 698, 522, 52, fill=False, stroke=True)  # Box: 698 to 750
        c.line(45, 728, 567, 728)  # Horizontal divider (middle of box)
        c.line(306, 698, 306, 750)  # Vertical divider (full height)
        
        c.setFont("Helvetica-Bold", 18)
        c.drawString(60, 733, "Campaign Central")  # Top section, centered vertically
        c.setFont("Helvetica", 9)
        c.drawString(320, 738, f"Receipt: {data['transaction_id']}")  # Right top
        c.drawString(320, 726, f"Date: {data['date']}")  # Right top (below divider start)
        c.drawString(320, 714, f"Time: {data['time']}")  # Right bottom
        c.drawString(60, 708, f"Client: {data['company_name']}")  # Left bottom
        
        y = 668  # Start below the grid box
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Grid table format
        y -= 15
        details = data['campaign_details']
        c.setStrokeColor(colors.HexColor('#009688'))
        c.setFont("Courier", 8)
        c.drawString(50, y, f"CPM: ${details['cpm']:<6.2f} | CTR: {details['ctr']:<5.1f}% | Bounce: {details['bounce_rate']:<5.1f}%")
        c.line(50, y-2, 550, y-2)
        y -= 10
        c.drawString(50, y, f"Content: {details['content_types']:<20} Budget: ${details['daily_budget']:<8.0f}/day")
        c.line(50, y-2, 550, y-2)
        y -= 10
        c.drawString(50, y, f"Geography: {details['geo_targets'][:50]}")
        y -= 15
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(400, y, "Total Amount:")
        c.drawString(500, y, f"${data['total']:.2f}")
    
    @staticmethod
    def template_14_pixel_perfect(c, data):
        """Pixel Perfect - Designer-focused style."""
        c.setPageSize(letter)
        
        # Artistic header (adjusted to prevent cropping)
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.HexColor('#E91E63'))
        c.drawString(50, 760, "Pixel")  # Adjusted from 800
        c.setFillColor(colors.HexColor('#9C27B0'))
        c.drawString(50, 735, "Perfect")  # Adjusted from 775
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 9)
        c.drawString(150, 750, "Design • Strategy • Results")  # Adjusted from 790
        
        c.setFont("Helvetica", 10)
        c.drawString(400, 760, f"#{data['transaction_id']}")  # Adjusted from 800
        c.drawString(400, 745, data['date'])  # Adjusted from 785
        
        y = 710  # Adjusted from 750
        
        c.drawString(50, y, f"Client: {data['company_name']}")
        c.drawString(50, y-15, f"Contact: {data['customer_name']}")
        
        y -= 40
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Multi-column metrics format
        y -= 15
        details = data['campaign_details']
        c.setFont("Helvetica-Bold", 8)
        c.drawString(50, y, "PERFORMANCE:")
        c.drawString(200, y, "BUDGET:")
        c.drawString(350, y, "TARGETING:")
        y -= 10
        c.setFont("Helvetica", 8)
        c.drawString(50, y, f"CPM ${details['cpm']:.2f}")
        c.drawString(200, y, f"${details['daily_budget']:.0f}/day")
        c.drawString(350, y, details['geo_targets'][:30])
        y -= 8
        c.drawString(50, y, f"CTR {details['ctr']:.1f}%")
        c.drawString(200, y, f"${details['total_budget']:,.0f} total")
        c.drawString(350, y, f"{details['age_range']}, {details['devices']}")
        y -= 8
        c.drawString(50, y, f"Bounce {details['bounce_rate']:.1f}%")
        c.drawString(200, y, details['pricing_model'])
        y -= 8
        c.setFont("Helvetica-Bold", 8)
        c.drawString(50, y, f"Campaign Period: {details['campaign_start_date']} to {details['campaign_end_date']}")
        y -= 15
        
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.HexColor('#E91E63'))
        c.drawString(400, y, "Total:")
        c.drawString(490, y, f"${data['total']:.2f}")
    
    @staticmethod
    def template_15_impact_ads(c, data):
        """Impact Ads - Bold impact style."""
        c.setPageSize(letter)
        
        # Large bold header (adjusted to prevent cropping)
        c.setFont("Helvetica-Bold", 32)
        c.setFillColor(colors.HexColor('#D32F2F'))
        c.drawString(50, 750, "IMPACT")  # Adjusted from 790
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        c.drawString(50, 735, "Maximum Impact. Minimum Waste.")  # Adjusted from 775
        
        y = 710  # Adjusted from 750
        
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Receipt: {data['transaction_id']} | {data['date']}")
        c.drawString(50, y-15, f"Customer: {data['customer_name']} | {data['company_name']}")
        
        y -= 40
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Bold stats format
        y -= 15
        details = data['campaign_details']
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor('#D32F2F'))
        c.drawString(50, y, f"${details['cpm']:.2f} CPM")
        c.drawString(150, y, f"{details['ctr']:.1f}% CTR")
        c.drawString(250, y, f"{details['bounce_rate']:.1f}% BOUNCE")
        c.setFillColor(colors.black)
        y -= 14
        c.setFont("Helvetica", 8)
        c.drawString(50, y, f"{details['content_types']} • {details['campaign_duration_days']}d @ ${details['daily_budget']:.0f}/day • {details['geo_targets']}")
        y -= 10
        c.drawString(50, y, f"Campaign Period: {details['campaign_start_date']} to {details['campaign_end_date']}")
        y -= 12
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(400, y, "TOTAL:")
        c.drawString(490, y, f"${data['total']:.2f}")
    
    @staticmethod
    def template_16_growth_engine(c, data):
        """Growth Engine - Performance-focused style."""
        c.setPageSize(letter)
        
        # Engine graphic simulation (adjusted to prevent cropping)
        c.setFillColor(colors.HexColor('#388E3C'))
        c.circle(100, 750, 25, fill=True, stroke=False)  # Adjusted from 790
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(100, 745, "GO")  # Adjusted from 785
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(140, 745, "Growth Engine")  # Adjusted from 785
        
        c.setFont("Helvetica", 9)
        c.drawString(140, 732, "Accelerating Your Success")  # Adjusted from 772
        
        y = 700  # Adjusted from 740
        
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Receipt: {data['transaction_id']}")
        c.drawString(50, y-15, f"Date: {data['date']}")
        c.drawString(300, y, f"Client: {data['company_name']}")
        
        y -= 40
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Simple list format
        y -= 15
        details = data['campaign_details']
        c.setFont("Helvetica", 8)
        c.drawString(50, y, f"Campaign: {details['content_types']} ({details['campaign_duration_days']} days)")
        y -= 9
        c.drawString(50, y, f"Performance: CPM ${details['cpm']:.2f}, CTR {details['ctr']:.1f}%, Bounce {details['bounce_rate']:.1f}%")
        y -= 9
        c.drawString(50, y, f"Budget: ${details['daily_budget']:.0f}/day ({details['pricing_model']})")
        y -= 9
        c.drawString(50, y, f"Target: {details['geo_targets']}, {details['age_range']}, {details['devices']}")
        y -= 15
        
        c.setFillColor(colors.HexColor('#388E3C'))
        c.setFont("Helvetica-Bold", 13)
        c.drawString(400, y, "Total:")
        c.drawString(490, y, f"${data['total']:.2f}")
    
    @staticmethod
    def template_17_ad_lab(c, data):
        """Ad Lab - Experimental scientific style."""
        c.setPageSize(letter)
        
        # Lab-like header (adjusted to prevent cropping)
        c.setFont("Courier-Bold", 22)
        c.drawString(50, 760, "AD LAB")  # Adjusted from 800
        c.setFont("Courier", 10)
        c.drawString(50, 745, "Experimental Marketing Solutions")  # Adjusted from 785
        
        c.setStrokeColor(colors.HexColor('#00897B'))
        c.setLineWidth(2)
        c.line(50, 738, 550, 738)  # Adjusted from 778
        
        y = 715  # Adjusted from 755
        
        c.setFont("Courier", 9)
        c.drawString(50, y, f"EXPERIMENT ID : {data['transaction_id']}")
        c.drawString(50, y-15, f"DATE          : {data['date']}")
        c.drawString(50, y-30, f"SUBJECT       : {data['company_name']}")
        c.drawString(50, y-45, f"RESEARCHER    : {data['customer_name']}")
        
        y -= 70
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Lab report format
        y -= 15
        details = data['campaign_details']
        c.setFont("Courier-Bold", 8)
        c.drawString(50, y, "[ EXPERIMENT PARAMETERS ]")
        y -= 10
        c.setFont("Courier", 8)
        c.drawString(50, y, f"START_DATE......: {details['campaign_start_date']:<12}  |  END_DATE......: {details['campaign_end_date']}")
        y -= 8
        c.drawString(50, y, f"METRIC_CPM......: ${details['cpm']:>6.2f}  |  METRIC_CTR.....: {details['ctr']:>5.1f}%  |  BOUNCE........: {details['bounce_rate']:>5.1f}%")
        y -= 8
        c.drawString(50, y, f"CONTENT_TYPE....: {details['content_types']:<20}  |  PRICING_MODEL.: {details['pricing_model']}")
        y -= 8
        c.drawString(50, y, f"DAILY_BUDGET....: ${details['daily_budget']:>7.0f}  |  CAMPAIGN_DAYS.: {details['campaign_duration_days']:>4} days")
        y -= 8
        c.drawString(50, y, f"GEO_TARGETS.....: {details['geo_targets'][:45]}")
        y -= 15
        
        c.setFont("Courier-Bold", 11)
        c.drawString(400, y, "TOTAL COST :")
        c.drawString(500, y, f"${data['total']:.2f}")
    
    @staticmethod
    def template_18_market_movers(c, data):
        """Market Movers - Dynamic market style."""
        c.setPageSize(letter)
        
        # Arrow graphic (adjusted to prevent cropping)
        c.setFillColor(colors.HexColor('#FF6F00'))
        c.saveState()
        c.translate(500, 760)  # Adjusted from 800
        c.rotate(45)
        points = [(0, 0), (30, 0), (30, -10), (40, 5), (30, 20), (30, 10), (0, 10)]
        p = c.beginPath()
        p.moveTo(points[0][0], points[0][1])
        for x, y in points[1:]:
            p.lineTo(x, y)
        p.close()
        c.drawPath(p, fill=True, stroke=False)
        c.restoreState()
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 26)
        c.drawString(50, 750, "Market Movers")  # Adjusted from 790
        
        c.setFont("Helvetica", 10)
        c.drawString(50, 735, f"Receipt #{data['transaction_id']} | {data['date']}")  # Adjusted from 775
        
        y = 705  # Adjusted from 745
        
        c.drawString(50, y, f"Client: {data['company_name']}")
        c.drawString(50, y-15, f"Contact: {data['customer_name']}")
        
        y -= 40
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Arrow/trend format
        y -= 15
        details = data['campaign_details']
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor('#FF6F00'))
        c.drawString(50, y, "↗ CAMPAIGN METRICS")
        c.setFillColor(colors.black)
        y -= 12
        c.setFont("Helvetica", 8)
        c.drawString(55, y, f"→ CPM: ${details['cpm']:.2f} | CTR: {details['ctr']:.1f}% | Bounce: {details['bounce_rate']:.1f}%")
        y -= 9
        c.drawString(55, y, f"→ {details['content_types']} Campaign | {details['pricing_model']} Pricing")
        y -= 9
        c.drawString(55, y, f"→ Budget: ${details['daily_budget']:.0f}/day × {details['campaign_duration_days']} days = ${details['total_budget']:,.0f}")
        y -= 9
        c.drawString(55, y, f"→ Targeting: {details['geo_targets']}, {details['age_range']}")
        y -= 9
        c.drawString(55, y, f"→ Period: {details['campaign_start_date']} to {details['campaign_end_date']}")
        y -= 15
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y, "Total:")
        c.drawString(490, y, f"${data['total']:.2f}")
    
    @staticmethod
    def template_19_conversion_kings(c, data):
        """Conversion Kings - ROI-focused style."""
        c.setPageSize(letter)
        
        # Crown graphic (adjusted to prevent cropping)
        c.setFillColor(colors.HexColor('#FFD700'))
        c.rect(280, 760, 10, 20, fill=True, stroke=False)  # Adjusted from 800
        c.rect(300, 760, 10, 25, fill=True, stroke=False)  # Adjusted from 800
        c.rect(320, 760, 10, 20, fill=True, stroke=False)  # Adjusted from 800
        c.rect(275, 755, 50, 8, fill=True, stroke=False)  # Adjusted from 795
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, 745, "Conversion Kings")  # Adjusted from 785
        c.setFont("Helvetica", 10)
        c.drawString(50, 730, "Turning Clicks into Customers")  # Adjusted from 770
        
        y = 700  # Adjusted from 740
        
        c.drawString(50, y, f"Receipt: {data['transaction_id']} | Date: {data['date']}")
        c.drawString(50, y-15, f"Client: {data['company_name']}")
        c.drawString(50, y-30, f"Campaign: {data['campaign_name']}")
        
        y -= 55
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - ROI-focused format
        y -= 15
        details = data['campaign_details']
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.HexColor('#FFD700'))
        c.drawString(50, y, "ROI METRICS:")
        c.setFillColor(colors.black)
        y -= 12
        c.setFont("Helvetica-Bold", 8)
        c.drawString(50, y, f"CPM: ${details['cpm']:.2f}")
        c.drawString(150, y, f"CTR: {details['ctr']:.1f}%")
        c.drawString(250, y, f"Bounce: {details['bounce_rate']:.1f}%")
        y -= 11
        c.setFont("Helvetica", 8)
        c.drawString(50, y, f"{details['content_types']} • ${details['daily_budget']:.0f}/day • {details['pricing_model']} • {details['geo_targets'][:35]}")
        y -= 9
        c.drawString(50, y, f"Period: {details['campaign_start_date']} - {details['campaign_end_date']}")
        y -= 12
        
        c.setFillColor(colors.HexColor('#FFD700'))
        c.rect(380, y-35, 170, 35, fill=True, stroke=True)
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(390, y-20, "TOTAL:")
        c.drawString(490, y-20, f"${data['total']:.2f}")
    
    @staticmethod
    def template_20_ad_wave(c, data):
        """Ad Wave - Flowing wave style."""
        c.setPageSize(letter)
        
        # Wave graphic (adjusted to prevent cropping - max was 822, now 790)
        c.setFillColor(colors.HexColor('#00ACC1'))
        p = c.beginPath()
        p.moveTo(0, 718)  # Adjusted from 750
        for i in range(0, 620, 20):
            p.curveTo(i, 738, i+10, 738, i+20, 718)  # Adjusted from 770/750
        p.lineTo(620, 790)  # Adjusted from 822 (was 30 points over!)
        p.lineTo(0, 790)    # Adjusted from 822
        p.close()
        c.drawPath(p, fill=True, stroke=False)
        
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 28)
        c.drawString(50, 748, "AD WAVE")  # Adjusted from 780
        c.setFont("Helvetica", 11)
        c.drawString(50, 733, "Riding the Wave of Success")  # Adjusted from 765
        
        c.setFillColor(colors.black)
        y = 688  # Adjusted from 720
        
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Receipt: {data['transaction_id']} | {data['date']}")
        c.drawString(50, y-15, f"Client: {data['company_name']} | {data['customer_name']}")
        
        y -= 40
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Wave/flowing format
        y -= 15
        details = data['campaign_details']
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColor(colors.HexColor('#00ACC1'))
        c.drawString(50, y, f"~ {details['content_types']} Campaign ~")
        c.setFillColor(colors.black)
        y -= 11
        c.setFont("Helvetica", 8)
        c.drawString(50, y, f"~ Metrics: CPM ${details['cpm']:.2f} ~ CTR {details['ctr']:.1f}% ~ Bounce {details['bounce_rate']:.1f}% ~")
        y -= 8
        c.drawString(50, y, f"~ Budget: ${details['daily_budget']:.0f}/day for {details['campaign_duration_days']} days ~ {details['pricing_model']} ~")
        y -= 8
        c.drawString(50, y, f"~ Reach: {details['geo_targets']}, {details['age_range']} on {details['devices']} ~")
        y -= 8
        c.drawString(50, y, f"~ Period: {details['campaign_start_date']} ~ {details['campaign_end_date']} ~")
        y -= 15
        
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.HexColor('#00ACC1'))
        c.drawString(400, y, "TOTAL:")
        c.drawString(490, y, f"${data['total']:.2f}")
    
    @staticmethod
    def template_21_strategy_sphere(c, data):
        """Strategy Sphere - Strategic circular style."""
        c.setPageSize(letter)
        
        # Circular elements (adjusted to prevent cropping)
        c.setFillColor(colors.HexColor('#5E35B1'))
        c.circle(520, 750, 40, fill=True, stroke=False)  # Adjusted from 790
        
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(520, 745, "PAID")  # Adjusted from 785
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 26)
        c.drawString(50, 745, "Strategy Sphere")  # Adjusted from 785
        
        c.setFont("Helvetica", 10)
        c.drawString(50, 730, "360° Marketing Solutions")  # Adjusted from 770
        
        y = 695  # Adjusted from 735
        
        c.drawString(50, y, f"Receipt: {data['transaction_id']}")
        c.drawString(50, y-15, f"Date: {data['date']}")
        c.drawString(300, y, f"Client: {data['company_name']}")
        
        y -= 40
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Circular/360 format
        y -= 15
        details = data['campaign_details']
        c.setFont("Helvetica-Bold", 8)
        c.drawString(50, y, "360° CAMPAIGN VIEW")
        y -= 11
        c.setFont("Helvetica", 8)
        c.drawString(50, y, f"○ Performance: CPM ${details['cpm']:.2f} • CTR {details['ctr']:.1f}% • Bounce {details['bounce_rate']:.1f}%")
        y -= 8
        c.drawString(50, y, f"○ Investment: ${details['daily_budget']:.0f}/day • {details['campaign_duration_days']} days • {details['pricing_model']}")
        y -= 8
        c.drawString(50, y, f"○ Content: {details['content_types']} • {details['display_formats'][:35] if details['display_formats'] != 'N/A' else details['video_formats'][:35]}")
        y -= 8
        c.drawString(50, y, f"○ Audience: {details['geo_targets']}, {details['age_range']}, {details['devices']}")
        y -= 8
        c.drawString(50, y, f"○ Period: {details['campaign_start_date']} to {details['campaign_end_date']}")
        y -= 15
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y, "Total:")
        c.drawString(490, y, f"${data['total']:.2f}")
    
    @staticmethod
    def template_22_performance_plus(c, data):
        """Performance Plus - Plus symbol style."""
        c.setPageSize(letter)
        
        # Plus symbol (adjusted to prevent cropping)
        c.setFillColor(colors.HexColor('#43A047'))
        c.rect(490, 730, 15, 50, fill=True, stroke=False)  # Adjusted from 770
        c.rect(475, 745, 45, 15, fill=True, stroke=False)  # Adjusted from 785
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, 750, "Performance Plus")  # Adjusted from 790
        c.setFont("Helvetica", 10)
        c.drawString(50, 735, "Adding Value to Every Campaign")  # Adjusted from 775
        
        y = 705  # Adjusted from 745
        
        c.drawString(50, y, f"Receipt #{data['transaction_id']} - {data['date']}")
        c.drawString(50, y-15, f"Billed to: {data['company_name']}")
        c.drawString(50, y-30, f"Attention: {data['customer_name']}")
        
        y -= 55
        y = VendorTemplates._draw_line_items(c, data['line_items'], 50, y)
        
        # Campaign details - Plus/positive format
        y -= 15
        details = data['campaign_details']
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor('#43A047'))
        c.drawString(50, y, "+ CAMPAIGN BOOST +")
        c.setFillColor(colors.black)
        y -= 11
        c.setFont("Helvetica", 8)
        c.drawString(50, y, f"+ CPM: ${details['cpm']:.2f} + CTR: {details['ctr']:.1f}% + Bounce: {details['bounce_rate']:.1f}%")
        y -= 9
        c.drawString(50, y, f"+ {details['content_types']} + {details['pricing_model']} + ${details['daily_budget']:.0f}/day")
        y -= 9
        c.drawString(50, y, f"+ {details['campaign_duration_days']} days + {details['geo_targets'][:40]}")
        y -= 9
        c.drawString(50, y, f"+ Period: {details['campaign_start_date']} to {details['campaign_end_date']}")
        y -= 15
        
        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(colors.HexColor('#43A047'))
        c.drawString(400, y, "TOTAL+:")
        c.drawString(490, y, f"${data['total']:.2f}")


# Mapping of templates
VENDOR_TEMPLATES = [
    VendorTemplates.template_1_techads_pro,
    VendorTemplates.template_2_admaster_global,
    VendorTemplates.template_3_creative_campaigns,
    VendorTemplates.template_4_digital_reach,
    VendorTemplates.template_5_apex_media,
    VendorTemplates.template_6_social_boost,
    VendorTemplates.template_7_prime_ads,
    VendorTemplates.template_8_click_velocity,
    VendorTemplates.template_9_brand_builders,
    VendorTemplates.template_10_viral_marketing,
    VendorTemplates.template_11_metric_masters,
    VendorTemplates.template_12_ad_genius,
    VendorTemplates.template_13_campaign_central,
    VendorTemplates.template_14_pixel_perfect,
    VendorTemplates.template_15_impact_ads,
    VendorTemplates.template_16_growth_engine,
    VendorTemplates.template_17_ad_lab,
    VendorTemplates.template_18_market_movers,
    VendorTemplates.template_19_conversion_kings,
    VendorTemplates.template_20_ad_wave,
    VendorTemplates.template_21_strategy_sphere,
    VendorTemplates.template_22_performance_plus,
]

VENDOR_NAMES = [
    "TechAds Pro",
    "AdMaster Global",
    "Creative Campaigns",
    "Digital Reach",
    "Apex Media",
    "Social Boost",
    "Prime Ads",
    "Click Velocity",
    "Brand Builders",
    "Viral Marketing",
    "Metric Masters",
    "Ad Genius",
    "Campaign Central",
    "Pixel Perfect",
    "Impact Ads",
    "Growth Engine",
    "Ad Lab",
    "Market Movers",
    "Conversion Kings",
    "Ad Wave",
    "Strategy Sphere",
    "Performance Plus",
]


