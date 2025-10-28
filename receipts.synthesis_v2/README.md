# Receipts Synthesis V2 - Pricing Tables Edition

Generate synthetic ad-campaign receipts with **multiple pricing tables** instead of line items.

## What's Different from V1?

### V1 (Original)
- ❌ Line items (Description, Qty, Unit Price, Total)
- ❌ Single table format
- ❌ Focus on services rendered

### V2 (This Version)
- ✅ **Multiple pricing tables** per receipt (2-4 tables)
- ✅ Each table has a **name** (Geographic Pricing, Demographic Pricing, etc.)
- ✅ Markets with **minimum value (USD)** and **reach (number)**
- ✅ Better for market-based advertising pricing

## Receipt Structure

Each receipt contains:
- Transaction details (ID, date, customer, company)
- Campaign name
- **2-4 Pricing Tables**, each with:
  - **Table Name**: Geographic Pricing, Demographic Pricing, Device Pricing, etc.
  - **Markets List**:
    - Market name (e.g., "North America", "Europe", "Asia Pacific")
    - Minimum value (USD) - e.g., $5,000
    - Reach (number) - e.g., 1,500,000 impressions
- Subtotal, tax, total
- Payment method

## Quick Start

```bash
cd receipts.synthesis_v2

# Install dependencies
pip install -r requirements.txt

# Generate 10 receipts with pricing tables
python receipt_generator_v2.py -n 10

# Generate sample set (2 per vendor = 6 receipts)
python receipt_generator_v2.py --sample

# List available vendors
python receipt_generator_v2.py --list-vendors
```

## Example Pricing Table

**Geographic Pricing**
| Market | Minimum (USD) | Reach |
|--------|---------------|-------|
| North America | $25,000 | 5,000,000 |
| Europe | $18,000 | 3,200,000 |
| Asia Pacific | $15,000 | 4,500,000 |

**Demographic Pricing**
| Market | Minimum (USD) | Reach |
|--------|---------------|-------|
| Age 18-24 | $8,000 | 1,200,000 |
| Age 25-34 | $12,000 | 1,800,000 |
| Age 35-44 | $10,000 | 1,500,000 |

## Vendor Templates

This version includes **3 vendor templates**:

0. **Premium Ad Solutions** - Modern blue professional style
1. **Global Media Partners** - Minimal gray simple style  
2. **Impact Advertising** - Bold orange energetic style

## Command Line Options

```bash
# Generate 50 receipts
python receipt_generator_v2.py -n 50

# Generate from specific vendor (0-2)
python receipt_generator_v2.py -v 1 -n 20

# Custom output directory
python receipt_generator_v2.py -n 100 -o /path/to/output

# Sample set (all vendors)
python receipt_generator_v2.py --sample

# List vendors
python receipt_generator_v2.py --list-vendors
```

## Python API

```python
from receipt_generator_v2 import ReceiptGeneratorV2

generator = ReceiptGeneratorV2(output_dir="my_receipts")

# Generate single receipt
receipt = generator.generate_single_receipt()

# Generate batch
receipts = generator.generate_batch(count=100)

# Generate sample set
samples = generator.generate_sample_set(receipts_per_vendor=5)
```

## Pricing Table Types

Receipts can include combinations of:
- **Geographic Pricing**: Regional market pricing
- **Demographic Pricing**: Age/demographic segment pricing
- **Device Pricing**: Desktop, mobile, tablet pricing
- **Time-Based Pricing**: Peak hours, seasonal pricing
- **Content Type Pricing**: Video, display, native pricing
- **Platform Pricing**: Social media, search, display network pricing
- **Engagement Tier Pricing**: Click, view, conversion pricing
- **Volume Discount Pricing**: Tiered volume pricing

## Use Cases

Perfect for testing:
- **Market-based extraction** algorithms
- **Multi-table parsing** with AI_EXTRACT
- **Complex data structures** in receipts
- **International pricing** models
- **Reach and minimum spend** analytics

## Files

- `data_generator_v2.py` - Generate synthetic pricing table data
- `vendors_v2.py` - 3 vendor templates with pricing table rendering
- `receipt_generator_v2.py` - Main script to generate receipts
- `requirements.txt` - Python dependencies (same as V1)

## Requirements

- Python 3.7+
- reportlab
- mimesis
- pillow

Install with:
```bash
pip install -r requirements.txt
```

## Differences vs V1

| Feature | V1 (Line Items) | V2 (Pricing Tables) |
|---------|----------------|---------------------|
| Data Structure | Line items list | Multiple pricing tables |
| Item Format | Qty × Unit Price | Market + Min Value + Reach |
| Tables per Receipt | 1 | 2-4 |
| Vendor Templates | 22 | 3 (expandable) |
| Use Case | Service billing | Market-based pricing |

## Future Enhancements

- [ ] Add more vendor templates (target: 10+)
- [ ] Support nested pricing tiers
- [ ] Add currency conversions
- [ ] Include contract terms
- [ ] Add visual charts/graphs
- [ ] Support multiple pages for complex pricing

---

**Version**: 2.0  
**Status**: Beta  
**Created**: October 2025

