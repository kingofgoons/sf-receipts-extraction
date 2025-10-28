# Quick Start - Receipts Synthesis V2

Generate synthetic receipts with pricing tables in 60 seconds.

## 1. Install Dependencies

```bash
cd receipts.synthesis_v2
pip install -r requirements.txt
```

## 2. Test Templates

```bash
# Test all 3 vendor templates
python test_generator_v2.py
```

This generates one receipt per vendor in `../receipts_test_v2/` to verify all templates work.

## 3. Generate Receipts

```bash
# Generate 10 receipts
python receipt_generator_v2.py -n 10

# Generate 100 receipts
python receipt_generator_v2.py -n 100

# Generate from specific vendor (0-2)
python receipt_generator_v2.py -v 0 -n 50
```

## 4. View Generated Receipts

Receipts are saved to `../receipts/` by default.

```bash
# List generated receipts
ls -lh ../receipts/receipt_v2_*.pdf

# Open a receipt
open ../receipts/receipt_v2_Premium_Ad_Solutions_*.pdf
```

## What You Get

Each receipt contains:
- **2-4 Pricing Tables** with names like:
  - Geographic Pricing
  - Demographic Pricing
  - Device Pricing
  - Time-Based Pricing
- **Markets** with:
  - Market name (e.g., "North America", "Europe")
  - Minimum value (USD): $500 - $50,000
  - Reach (impressions): 10,000 - 10,000,000
- Transaction details and totals

## Common Commands

```bash
# List vendors
python receipt_generator_v2.py --list-vendors

# Generate sample set (2 per vendor = 6 receipts)
python receipt_generator_v2.py --sample

# Custom output directory
python receipt_generator_v2.py -n 50 -o /path/to/receipts

# Specific vendor (Impact Advertising = vendor 2)
python receipt_generator_v2.py -v 2 -n 25
```

## Python API

```python
from receipt_generator_v2 import ReceiptGeneratorV2

# Initialize
generator = ReceiptGeneratorV2(output_dir="my_receipts")

# Generate single receipt
receipt_path = generator.generate_single_receipt()

# Generate batch
receipt_paths = generator.generate_batch(count=100)

# Sample set
samples = generator.generate_sample_set(receipts_per_vendor=3)
```

## Next Steps

- Generate receipts: `python receipt_generator_v2.py -n 250`
- Upload to Snowflake: See `../receipts-uploader/`
- Extract pricing tables: Use AI_EXTRACT to parse pricing table data

---

That's it! You're ready to generate receipts with pricing tables. 🚀

