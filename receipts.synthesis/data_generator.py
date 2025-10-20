"""Generate synthetic data for ad-campaign receipts."""
import random
from datetime import datetime, timedelta
from mimesis import Generic, Locale


class DataGenerator:
    """Generate realistic synthetic data for receipts."""
    
    def __init__(self, locale=Locale.EN):
        self.generic = Generic(locale)
        
    def generate_transaction_id(self):
        """Generate a random transaction ID."""
        prefix = random.choice(['TXN', 'INV', 'RCP', 'ORD', 'PAY'])
        number = random.randint(100000, 999999)
        return f"{prefix}-{number}"
    
    def generate_date(self, days_back=365):
        """Generate a random date within the past N days."""
        days_ago = random.randint(0, days_back)
        date = datetime.now() - timedelta(days=days_ago)
        return date.strftime("%Y-%m-%d")
    
    def generate_time(self):
        """Generate a random time."""
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        return f"{hour:02d}:{minute:02d}"
    
    def generate_customer_name(self):
        """Generate a random customer name."""
        return self.generic.person.full_name()
    
    def generate_company_name(self):
        """Generate a random company name."""
        return self.generic.person.name() + " " + random.choice([
            'Inc.', 'LLC', 'Corp.', 'Ltd.', 'Group', 'Agency', 'Media', 'Marketing'
        ])
    
    def generate_email(self):
        """Generate a random email."""
        return self.generic.person.email()
    
    def generate_phone(self):
        """Generate a random phone number."""
        return self.generic.person.telephone()
    
    def generate_address(self):
        """Generate a random address."""
        return {
            'street': self.generic.address.street_name() + " " + str(self.generic.address.street_number()),
            'city': self.generic.address.city(),
            'state': self.generic.address.state(abbr=True),
            'zip': self.generic.address.zip_code()
        }
    
    def generate_campaign_name(self):
        """Generate a random campaign name."""
        adjectives = ['Summer', 'Winter', 'Spring', 'Fall', 'Holiday', 'Launch', 'Premium', 'Flash', 'Grand', 'Ultimate']
        types = ['Sale', 'Campaign', 'Promotion', 'Event', 'Drive', 'Initiative', 'Program', 'Showcase']
        years = ['2024', '2025', 'Q1', 'Q2', 'Q3', 'Q4']
        
        return f"{random.choice(adjectives)} {random.choice(types)} {random.choice(years)}"
    
    def generate_ad_platforms(self, count=None):
        """Generate random ad platforms with spend amounts."""
        platforms = [
            'Google Ads', 'Facebook Ads', 'Instagram Ads', 'LinkedIn Ads',
            'Twitter/X Ads', 'TikTok Ads', 'YouTube Ads', 'Snapchat Ads',
            'Pinterest Ads', 'Reddit Ads', 'Amazon Ads', 'Microsoft Ads'
        ]
        
        if count is None:
            count = random.randint(2, 6)
        
        selected = random.sample(platforms, min(count, len(platforms)))
        
        items = []
        for platform in selected:
            amount = round(random.uniform(500, 15000), 2)
            impressions = random.randint(10000, 500000)
            clicks = random.randint(100, 10000)
            items.append({
                'platform': platform,
                'amount': amount,
                'impressions': impressions,
                'clicks': clicks
            })
        
        return items
    
    def generate_line_items(self, count=None):
        """Generate random line items for receipt."""
        services = [
            'Campaign Management', 'Creative Design', 'Video Production',
            'Copywriting', 'Analytics & Reporting', 'A/B Testing',
            'Audience Targeting', 'Landing Page Design', 'Display Ad Design',
            'Social Media Management', 'SEO Optimization', 'Content Creation'
        ]
        
        if count is None:
            count = random.randint(2, 5)
        
        selected = random.sample(services, min(count, len(services)))
        
        items = []
        for service in selected:
            quantity = random.randint(1, 10)
            unit_price = round(random.uniform(100, 2000), 2)
            items.append({
                'description': service,
                'quantity': quantity,
                'unit_price': unit_price,
                'total': round(quantity * unit_price, 2)
            })
        
        return items
    
    def generate_campaign_details(self):
        """Generate campaign-specific details for display and video ad campaigns."""
        # Generate campaign start and end dates
        start_date = datetime.now() + timedelta(days=random.randint(1, 30))
        duration_days = random.randint(30, 180)
        end_date = start_date + timedelta(days=duration_days)
        
        # Determine campaign content types
        has_display = random.choice([True, False])
        has_video = random.choice([True, False])
        
        # Ensure at least one content type
        if not has_display and not has_video:
            if random.random() < 0.5:
                has_display = True
            else:
                has_video = True
        
        # Generate display ad formats
        display_formats = []
        if has_display:
            all_display_types = [
                'Interstitial Ads', 'Native Ads', 'Interactive Content',
                'Infographics', 'Expanding Ads', 'Lightbox Ads', 'Pop-up Ads'
            ]
            num_formats = random.randint(1, 4)
            display_formats = random.sample(all_display_types, num_formats)
        
        # Generate video ad formats
        video_formats = []
        if has_video:
            video_types = ['Pre-roll', 'Mid-roll', 'Post-roll']
            num_video = random.randint(1, len(video_types))
            video_formats = random.sample(video_types, num_video)
        
        # Build content types string
        content_types = []
        if has_display:
            content_types.append('Display')
        if has_video:
            content_types.append('Video')
        
        # Generate ramp-up timing
        ramp_up_options = [
            'Immediate - Full budget from day 1',
            'Gradual - 25% increase weekly over 4 weeks',
            'Fast - 50% increase weekly over 2 weeks',
            'Conservative - 10% increase daily for 10 days',
            'Aggressive - Double spend every 3 days',
            'Linear - Equal daily increase over 30 days',
            'Step - 33% increments at weeks 1, 2, 3'
        ]
        
        # Generate budget allocation
        daily_budget = round(random.uniform(100, 5000), 2)
        total_budget = round(daily_budget * duration_days, 2)
        
        # Generate target metrics
        target_impressions = random.randint(50000, 5000000)
        target_clicks = random.randint(1000, 100000)
        target_conversions = random.randint(50, 5000)
        
        # Generate key performance metrics
        cpm = round(random.uniform(2.5, 25.0), 2)  # Cost Per Mille
        ctr = round(random.uniform(0.5, 8.5), 2)   # Click-Through Rate (%)
        bounce_rate = round(random.uniform(25.0, 75.0), 1)  # Bounce Rate (%)
        
        # Generate pricing model
        pricing_models = ['CPM', 'CPC', 'CPA', 'CPV', 'Flat Rate']
        pricing_model = random.choice(pricing_models)
        
        # Generate rate based on pricing model
        if pricing_model == 'CPM':
            rate = cpm
            rate_description = f"${rate} per 1,000 impressions"
        elif pricing_model == 'CPC':
            rate = round(random.uniform(0.50, 15.0), 2)
            rate_description = f"${rate} per click"
        elif pricing_model == 'CPA':
            rate = round(random.uniform(10, 200), 2)
            rate_description = f"${rate} per acquisition"
        elif pricing_model == 'CPV':
            rate = round(random.uniform(0.10, 2.0), 2)
            rate_description = f"${rate} per view"
        else:  # Flat Rate
            rate = round(random.uniform(5000, 50000), 2)
            rate_description = f"${rate} flat rate"
        
        # Generate frequency cap
        frequency_caps = [
            '3 impressions per user per day',
            '5 impressions per user per week',
            'No frequency cap',
            '2 impressions per user per day',
            '10 impressions per user per week',
            '1 impression per user per day'
        ]
        
        # Generate targeting info
        geo_targets = random.sample([
            'United States', 'Canada', 'United Kingdom', 'Australia',
            'Germany', 'France', 'Japan', 'Brazil', 'India', 'Mexico'
        ], k=random.randint(1, 4))
        
        age_ranges = random.choice([
            '18-24', '25-34', '35-44', '45-54', '55-64', '18-34', '25-54', '35-65+'
        ])
        
        return {
            'campaign_start_date': start_date.strftime("%Y-%m-%d"),
            'campaign_end_date': end_date.strftime("%Y-%m-%d"),
            'campaign_duration_days': duration_days,
            'content_types': ' & '.join(content_types),
            'has_display': has_display,
            'has_video': has_video,
            'display_formats': ', '.join(display_formats) if display_formats else 'N/A',
            'video_formats': ', '.join(video_formats) if video_formats else 'N/A',
            'ramp_up_strategy': random.choice(ramp_up_options),
            'daily_budget': daily_budget,
            'total_budget': total_budget,
            'target_impressions': target_impressions,
            'target_clicks': target_clicks,
            'target_conversions': target_conversions,
            'pricing_model': pricing_model,
            'rate': rate,
            'rate_description': rate_description,
            'cpm': cpm,
            'ctr': ctr,
            'bounce_rate': bounce_rate,
            'frequency_cap': random.choice(frequency_caps),
            'geo_targets': ', '.join(geo_targets),
            'age_range': age_ranges,
            'devices': random.choice(['All Devices', 'Mobile Only', 'Desktop Only', 'Mobile & Tablet'])
        }
    
    def generate_receipt_data(self):
        """Generate complete receipt data."""
        line_items = self.generate_line_items()
        subtotal = sum(item['total'] for item in line_items)
        tax_rate = random.choice([0, 0.05, 0.07, 0.08, 0.0825, 0.10])
        tax = round(subtotal * tax_rate, 2)
        total = subtotal + tax
        
        return {
            'transaction_id': self.generate_transaction_id(),
            'date': self.generate_date(),
            'time': self.generate_time(),
            'customer_name': self.generate_customer_name(),
            'company_name': self.generate_company_name(),
            'email': self.generate_email(),
            'phone': self.generate_phone(),
            'address': self.generate_address(),
            'campaign_name': self.generate_campaign_name(),
            'line_items': line_items,
            'ad_platforms': self.generate_ad_platforms(),
            'campaign_details': self.generate_campaign_details(),
            'subtotal': subtotal,
            'tax_rate': tax_rate,
            'tax': tax,
            'total': total,
            'payment_method': random.choice(['Credit Card', 'Wire Transfer', 'ACH', 'Check', 'PayPal'])
        }


