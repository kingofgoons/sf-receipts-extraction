# Feature Summary

## Overview
Complete synthetic ad-campaign receipt generator with 22 unique vendor styles and comprehensive campaign details.

## Key Features

### 1. **22 Unique Vendor Templates**
Each vendor has a distinct visual style:
- Different color schemes
- Unique layouts and typography
- Brand-specific headers and graphics
- Varying table styles and formatting

### 2. **Compact Campaign Details Section**
Every receipt includes a compact, 2-column campaign details table with all essential information:

#### Budget & Pricing
- **Pricing Model**: CPM, CPC, CPA, CPV, or Flat Rate
- **Rate**: Varies by pricing model (e.g., "$5.50 per click" or "$12.00 per 1,000 impressions")
- **Daily Budget**: Random amount between $100-$5,000
- **Total Budget**: Calculated based on daily budget × campaign duration

#### Campaign Timeline
- **Campaign Period**: Start and end dates
- **Duration**: Between 30-180 days
- **Ramp-Up Strategy**: 7 different strategies including:
  - Immediate - Full budget from day 1
  - Gradual - 25% increase weekly over 4 weeks
  - Fast - 50% increase weekly over 2 weeks
  - Conservative - 10% increase daily for 10 days
  - Aggressive - Double spend every 3 days
  - Linear - Equal daily increase over first 30 days
  - Step - 33% increments at weeks 1, 2, and 3

#### Target Metrics
- **Target Impressions**: 50,000 - 5,000,000
- **Target Clicks**: 1,000 - 100,000
- **Target Conversions**: 50 - 5,000

#### Targeting Parameters
- **Frequency Cap**: Various options (e.g., "3 impressions per user per day")
- **Geographic Targets**: 1-4 countries from a pool of 10
- **Age Range**: Multiple demographic segments
- **Devices**: All Devices, Mobile Only, Desktop Only, or Mobile & Tablet

### 3. **Realistic Synthetic Data**
Generated using the `mimesis` library:
- Customer names and company names
- Email addresses and phone numbers
- Complete addresses (street, city, state, zip)
- Transaction IDs with various prefixes
- Dates and times
- Campaign names
- Service line items with quantities and prices

### 4. **Multiple Pricing Models**
Different pricing models with appropriate rate descriptions:
- **CPM (Cost Per Mille)**: $2.50 - $25.00 per 1,000 impressions
- **CPC (Cost Per Click)**: $0.50 - $15.00 per click
- **CPA (Cost Per Acquisition)**: $10 - $200 per acquisition
- **CPV (Cost Per View)**: $0.10 - $2.00 per view
- **Flat Rate**: $5,000 - $50,000 flat rate

### 5. **Flexible Generation Options**

#### Command Line Interface
```bash
# Generate N receipts with random vendors
python receipt_generator.py -n 10

# Generate from specific vendor
python receipt_generator.py -n 50 -v 5

# Generate sample set (2 per vendor)
python receipt_generator.py --sample

# List all vendors
python receipt_generator.py --list-vendors

# Custom output directory
python receipt_generator.py -n 10 -o my_receipts
```

#### Python API
```python
from receipt_generator import ReceiptGenerator

generator = ReceiptGenerator()

# Generate single receipt
receipt = generator.generate_single_receipt()

# Generate from specific vendor
receipt = generator.generate_single_receipt(vendor_index=5)

# Generate batch
receipts = generator.generate_batch(count=100)

# Generate sample set
sample = generator.generate_sample_set(receipts_per_vendor=2)
```

### 6. **Infinite Generation**
- Can generate unlimited receipts
- Each receipt has unique synthetic data
- 22 different visual styles ensure variety

### 7. **Production-Ready Output**
- Professional PDF format
- Print-ready quality
- Proper formatting and alignment
- Realistic appearance for testing/development

## Use Cases

1. **Testing OCR/Document Processing Systems**: Train and test document extraction systems with diverse receipt formats
2. **ML/AI Training Data**: Generate large datasets for machine learning models
3. **UI/UX Development**: Create realistic mockups and prototypes
4. **QA Testing**: Test ad-campaign management platforms
5. **Demo & Presentations**: Show realistic ad-campaign receipts without exposing real data

## Technical Stack

- **PDF Generation**: ReportLab
- **Synthetic Data**: Mimesis
- **Image Support**: Pillow
- **Python**: 3.7+

## File Structure

```
receipts.synthesis/
├── data_generator.py       # Synthetic data generation
├── vendors.py              # 22 vendor templates
├── receipt_generator.py    # Main generator & CLI
├── example.py              # Usage examples
├── test_generator.py       # Test script
├── requirements.txt        # Dependencies
├── README.md               # Full documentation
├── QUICKSTART.md          # Quick start guide
├── FEATURES.md            # This file
└── .gitignore             # Git ignore rules
```

## Statistics

- **22** unique vendor templates
- **5** pricing models (CPM, CPC, CPA, CPV, Flat Rate)
- **7** ramp-up strategies
- **10** geographic targeting options
- **15** campaign detail parameters per receipt
- **∞** receipts can be generated

## Tested & Verified

✓ All 22 templates generate successfully  
✓ Campaign details section appears on all receipts  
✓ Realistic data generation  
✓ Proper PDF formatting  
✓ Command-line interface works  
✓ Python API works  
✓ No linter errors (except expected missing package warning)

