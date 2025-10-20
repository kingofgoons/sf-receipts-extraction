# Receipts.extraction

A comprehensive project for synthetic ad-campaign receipt generation and extraction.

## Project Structure

```
Receipts.extraction/
├── receipts/               # Generated receipts (not tracked)
├── receipts.synthesis/     # Synthetic receipt generation
│   ├── Python source files
│   ├── 22 vendor templates
│   └── Documentation
│
├── receipts-uploader/      # Upload receipts to Snowflake
│   ├── Service account setup
│   └── Testing scripts
│
└── (Future: receipts.extraction, receipts-processor modules)
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

---

## receipts-uploader

Upload generated receipts to Snowflake using service account authentication.

### Setup

1. **Create and activate a virtual environment:**
   ```bash
   cd receipts-uploader
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   # venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure credentials:**
   ```bash
   # Copy the template
   cp config.template.json config.json
   
   # Edit config.json with your Snowflake credentials
   # (This file is excluded from git)
   ```

4. **Set up Snowflake service account:**
   - Run the SQL script in Snowflake to create the service user
   - Configure key-pair authentication
   - Update config.json with your credentials

### Test Service Account

```bash
cd receipts-uploader

# Test Snowflake service account connection
python test_service_account.py
```

This will verify:
- ✓ Snowflake connection with service account
- ✓ Key-pair authentication
- ✓ Database and schema access
- ✓ Table creation permissions

### Upload Receipts to Snowflake

Upload receipt PDFs from the `receipts/` directory to Snowflake stage:

```bash
cd receipts-uploader

# Activate virtual environment (if not already active)
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Upload all new receipts (skips already uploaded)
python upload_receipts.py

# Upload from custom directory
python upload_receipts.py -d /path/to/receipts

# Upload to custom stage
python upload_receipts.py -s CUSTOM_DB.SCHEMA.STAGE
```

Features:
- ✓ Automatically checks which files are already in the stage
- ✓ Only uploads new/missing files (no duplicates)
- ✓ Shows upload progress and summary
- ✓ Uploads to `RECEIPTS_PROCESSING_DB.RAW.RECEIPTS` by default

### Files

- `config.template.json` - Template for configuration
- `config.json` - Your credentials (NOT tracked by git)
- `create.service.user.sql` - Snowflake service account setup
- `test_service_account.py` - Test service account connection
- `upload_receipts.py` - Upload receipts to Snowflake stage
- `requirements.txt` - Python dependencies

---

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

### receipts-uploader ✅
- **Status**: Available
- **Purpose**: Upload receipts to Snowflake
- **Auth**: Service account with key-pair authentication
- **Testing**: `test_service_account.py` available

### receipts-processor 🔜
- **Status**: In development
- **Purpose**: Process and validate receipt data

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

### receipts-uploader
- Python 3.7+
- snowflake-connector-python
- python-dotenv
- cryptography
- requests

See `receipts-uploader/requirements.txt` for specific versions.

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

