# Receipts.extraction

A comprehensive project for synthetic ad-campaign receipt generation and extraction.

## Project Structure

```
Receipts.extraction/
├── receipts.synthesis/     # Synthetic receipt generation
│   ├── Python source files
│   ├── 22 vendor templates
│   └── Documentation
│
└── (Future: receipts.extraction module for OCR/extraction)
```

## receipts.synthesis

Generate unlimited synthetic ad-campaign receipts in PDF format with 22 unique vendor styles.

### Features

- **22 Unique Vendor Templates** - Each with distinct visual design
- **Display Ad Campaigns** - 7 format types (Interstitial, Native, Interactive, Infographics, Expanding, Lightbox, Pop-up)
- **Video Ad Campaigns** - 3 placement types (Pre-roll, Mid-roll, Post-roll)
- **Key Performance Metrics** - CPM, CTR, Bounce Rate
- **Infinite Generation** - Generate as many receipts as needed
- **Realistic Data** - Uses mimesis library for authentic-looking information

### Quick Start

```bash
cd receipts.synthesis

# Install dependencies
pip install -r requirements.txt

# Test all 22 templates
python test_generator.py

# Generate 10 receipts
python receipt_generator.py -n 10

# Generate sample set (2 per vendor = 44 receipts)
python receipt_generator.py --sample
```

### Documentation

See `receipts.synthesis/README.md` for complete documentation.

## Installation

```bash
# Clone the repository (when ready)
git clone <your-repo-url>
cd Receipts.extraction

# Set up receipts.synthesis
cd receipts.synthesis
pip install -r requirements.txt

# Test
python test_generator.py
```

## Usage

### Generate Receipts

```bash
cd receipts.synthesis

# Generate receipts
python receipt_generator.py -n 100

# List available vendors
python receipt_generator.py --list-vendors

# Generate from specific vendor
python receipt_generator.py -v 5 -n 50
```

### Python API

```python
from receipts.synthesis.receipt_generator import ReceiptGenerator

generator = ReceiptGenerator(output_dir="my_receipts")

# Generate single receipt
receipt = generator.generate_single_receipt()

# Generate batch
receipts = generator.generate_batch(count=1000)
```

## Project Status

### receipts.synthesis ✅
- **Status**: Production ready
- **Templates**: 22/22 working perfectly
- **Quality**: Professional-grade PDFs
- **Features**: Complete

### receipts.extraction 🔜
- **Status**: Future development
- **Purpose**: Extract data from receipt PDFs
- **Tools**: OCR, data extraction, validation

## Requirements

### receipts.synthesis
- Python 3.7+
- reportlab
- mimesis
- pillow

See `receipts.synthesis/requirements.txt` for specific versions.

## License

This is a synthetic data generation tool for testing and development purposes.

## Contributing

Contributions welcome! To add new vendor templates or features:
1. Fork the repository
2. Create your feature branch
3. Test thoroughly with `python test_generator.py`
4. Submit a pull request

## Support

For issues or questions:
1. Check the documentation in `receipts.synthesis/`
2. Review `receipts.synthesis/QUICKSTART.md`
3. Run `python receipt_generator.py --list-vendors` to see available templates

---

**Version**: 1.0  
**Status**: Production Ready  
**Last Updated**: October 2025

