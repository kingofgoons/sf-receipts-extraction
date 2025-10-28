"""Generate synthetic data for ad-campaign receipts with pricing tables."""
import random
from datetime import datetime, timedelta
from mimesis import Generic, Locale


class DataGeneratorV2:
    """Generate realistic synthetic data for receipts with pricing tables."""
    
    def __init__(self, locale=Locale.EN):
        self.generic = Generic(locale)
        
        # Market regions
        self.markets = [
            'North America', 'Europe', 'Asia Pacific', 'Latin America',
            'Middle East', 'Africa', 'Australia', 'Southeast Asia',
            'Eastern Europe', 'Western Europe', 'South America', 'Central America',
            'Nordic Countries', 'UK & Ireland', 'India', 'China', 'Japan', 'Brazil'
        ]
        
        # Pricing table types
        self.table_types = [
            'Geographic Pricing', 'Demographic Pricing', 'Device Pricing',
            'Time-Based Pricing', 'Content Type Pricing', 'Platform Pricing',
            'Engagement Tier Pricing', 'Volume Discount Pricing'
        ]
    
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
    
    def generate_pricing_table(self, table_name=None):
        """
        Generate a single pricing table with markets.
        
        Returns:
            dict with:
                - name: Table name
                - markets: List of dicts with market, min_value_usd, reach
        """
        if table_name is None:
            table_name = random.choice(self.table_types)
        
        # Generate 3-8 markets per table
        num_markets = random.randint(3, 8)
        markets = []
        
        selected_markets = random.sample(self.markets, min(num_markets, len(self.markets)))
        
        for market in selected_markets:
            markets.append({
                'market': market,
                'min_value_usd': random.randint(500, 50000),
                'reach': random.randint(10000, 10000000)
            })
        
        return {
            'name': table_name,
            'markets': markets
        }
    
    def generate_receipt_data(self):
        """Generate complete receipt data with pricing tables."""
        
        # Generate 2-4 pricing tables per receipt
        num_tables = random.randint(2, 4)
        pricing_tables = []
        
        # Ensure variety in table types
        table_types_sample = random.sample(self.table_types, min(num_tables, len(self.table_types)))
        
        for table_type in table_types_sample:
            pricing_tables.append(self.generate_pricing_table(table_type))
        
        # Calculate totals from all pricing tables
        total_min_value = sum(
            sum(market['min_value_usd'] for market in table['markets'])
            for table in pricing_tables
        )
        
        data = {
            'transaction_id': self.generate_transaction_id(),
            'date': self.generate_date(),
            'time': self.generate_time(),
            'customer_name': self.generate_customer_name(),
            'company_name': self.generate_company_name(),
            'campaign_name': f"{random.choice(['Q4', 'Q1', 'Summer', 'Holiday', 'Spring'])} Campaign {random.randint(2024, 2026)}",
            'pricing_tables': pricing_tables,
            'subtotal': total_min_value,
            'tax': total_min_value * 0.08,  # 8% tax
            'total': total_min_value * 1.08,
            'payment_method': random.choice(['Credit Card', 'Wire Transfer', 'ACH', 'Check']),
            'notes': random.choice([
                'Thank you for your business!',
                'Net 30 payment terms',
                'Contact us for volume discounts',
                'Early payment discount available'
            ])
        }
        
        return data

