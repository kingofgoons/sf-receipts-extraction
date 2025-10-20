# Quick Start Guide

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the generator:**
   ```bash
   python test_generator.py
   ```
   
   This will create one receipt from each of the 22 vendor templates in the `test_output/` directory.

## Usage Examples

### Generate 10 receipts with random vendors
```bash
python receipt_generator.py -n 10
```

### Generate a sample set (2 receipts from each vendor = 44 total)
```bash
python receipt_generator.py --sample
```

### Generate 50 receipts from a specific vendor
```bash
python receipt_generator.py --list-vendors  # See available vendors
python receipt_generator.py -n 50 -v 5      # Generate from vendor #5
```

### Run the example script
```bash
python example.py
```

## What's in Each Receipt?

Every generated receipt includes:

1. **Header Section**: Vendor branding with unique visual style
2. **Transaction Info**: Receipt ID, date, time, customer info
3. **Line Items**: Services provided with quantities and prices
4. **Campaign Details Table** (Compact 2-column layout):
   - **Left Column**: Period/Duration, Content Types (Display/Video), Display Formats, Video Formats, Pricing + Rate
   - **Right Column**: Budget, Key Metrics (CPM/CTR/Bounce Rate), Target Metrics, Geo, Demographics
5. **Totals**: Subtotal, tax, and final total

### Layout Features
- **Compact Design**: Campaign details use a space-efficient 2-column layout (~52px height)
- **No Overlaps**: Clean spacing ensures all sections are clearly separated
- **Full Information**: All campaign parameters included despite compact size

## Output

All receipts are saved as PDF files in the `output/` directory (or custom directory specified with `-o` flag).

Filename format: `receipt_VendorName_YYYYMMDD_HHMMSS_microseconds.pdf`

## Notes

- Each of the 22 vendor templates has a unique visual style and color scheme
- All data is randomly generated using the `mimesis` library for realistic values
- The generator can create an unlimited number of receipts with unique data
- Campaign details vary based on pricing model (CPM, CPC, CPA, CPV, or Flat Rate)

