# Synthetic Ad-Campaign Receipt Generator

Generate realistic synthetic ad-campaign receipts in PDF format with 22 different vendor styles.

## Features

- **22 Unique Vendor Styles**: Each vendor has a distinct visual design, color scheme, and layout
- **Realistic Data**: Uses the `mimesis` library to generate realistic customer names, companies, addresses, and transaction details
- **Infinite Generation**: Generate as many receipts as needed with randomized data
- **Flexible API**: Command-line interface and Python API for easy integration

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Generate 10 Random Receipts

Receipts are generated to `../receipts/` directory by default:

```bash
python receipt_generator.py -n 10
```

### Generate Sample Set (2 receipts from each of 22 vendors)

```bash
python receipt_generator.py --sample
```

### Generate 50 Receipts from a Specific Vendor

```bash
python receipt_generator.py -n 50 -v 0
```

### List All Available Vendors

```bash
python receipt_generator.py --list-vendors
```

## Command-Line Options

```
-n, --count N         Number of receipts to generate (default: 10)
-v, --vendor INDEX    Specific vendor index (0-21) to use
-o, --output DIR      Output directory for PDFs (default: output)
--sample              Generate sample set with 2 receipts per vendor
--list-vendors        List all available vendor templates
```

## Available Vendors

1. **TechAds Pro** - Modern minimalist style
2. **AdMaster Global** - Classic formal style
3. **Creative Campaigns** - Colorful creative style
4. **Digital Reach** - Simple invoice style
5. **Apex Media** - Bold and modern style
6. **Social Boost** - Social media focused style
7. **Prime Ads** - Premium gold accent style
8. **Click Velocity** - Fast and dynamic style
9. **Brand Builders** - Professional corporate style
10. **Viral Marketing** - Trendy and energetic style
11. **Metric Masters** - Data-focused analytical style
12. **Ad Genius** - Smart and sleek style
13. **Campaign Central** - Organized grid style
14. **Pixel Perfect** - Designer-focused style
15. **Impact Ads** - Bold impact style
16. **Growth Engine** - Performance-focused style
17. **Ad Lab** - Experimental scientific style
18. **Market Movers** - Dynamic market style
19. **Conversion Kings** - ROI-focused style
20. **Ad Wave** - Flowing wave style
21. **Strategy Sphere** - Strategic circular style
22. **Performance Plus** - Plus symbol style

## Python API Usage

```python
from receipt_generator import ReceiptGenerator

# Initialize generator
generator = ReceiptGenerator(output_dir="my_receipts")

# Generate a single receipt with random vendor
receipt_path = generator.generate_single_receipt()

# Generate a single receipt from specific vendor
receipt_path = generator.generate_single_receipt(vendor_index=5)

# Generate batch of 100 receipts
receipts = generator.generate_batch(count=100)

# Generate sample set (2 per vendor)
sample_set = generator.generate_sample_set(receipts_per_vendor=2)

# List available vendors
vendors = generator.list_vendors()
print(f"Available vendors: {len(vendors)}")
```

## Data Generator

The `DataGenerator` class creates realistic synthetic data including:

- Transaction IDs
- Dates and times
- Customer names and company names
- Email addresses and phone numbers
- Addresses (street, city, state, zip)
- Campaign names
- Ad platforms with spend amounts (Google Ads, Facebook Ads, etc.)
- Line items for services (Campaign Management, Creative Design, etc.)
- **Compact Campaign Details Section** (2-column layout) with:
  - **Left Column:**
    - Campaign period (start and end dates with duration)
    - Content types (Display and/or Video Ads)
    - Display formats (Interstitial, Native, Interactive, Infographics, Expanding, Lightbox, Pop-up)
    - Video formats (Pre-roll, Mid-roll, Post-roll)
    - Pricing model and rate
  - **Right Column:**
    - Budget (daily and total)
    - Key metrics (CPM, CTR %, Bounce Rate %)
    - Target metrics (impressions, clicks)
    - Geographic targets
    - Demographics (age range and device targeting)
- Subtotals, tax, and totals

## Customization

To add your own vendor template:

1. Open `vendors.py`
2. Add a new static method to the `VendorTemplates` class
3. Implement your custom design using reportlab's canvas API
4. Add the template to the `VENDOR_TEMPLATES` list
5. Add the vendor name to the `VENDOR_NAMES` list

Example:

```python
@staticmethod
def template_23_my_vendor(c, data):
    """My Vendor - Custom style."""
    c.setPageSize(letter)
    # Your custom design here
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, 750, "My Vendor Name")
    # ... rest of your design
```

## Output

All receipts are saved as PDF files in the output directory (default: `output/`).

Filename format: `receipt_VendorName_YYYYMMDD_HHMMSS_microseconds.pdf`

Example: `receipt_TechAds_Pro_20241020_143022_456789.pdf`

## License

This is a synthetic data generation tool for testing and development purposes.


