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

## receipts-processor

Process and extract structured data from receipt PDFs using Snowflake Document AI.

### Setup

1. **Run Snowflake setup script:**
   - Execute `receipts-processor/setup.sql` in Snowflake
   - Creates `RECEIPTS_PROCESSING_DB` database
   - Creates `RAW` schema with `RECEIPTS` stage
   - Grants permissions to `ETL_SERVICE_ROLE`

2. **Use Snowflake Notebook:**
   - Upload `receipts-processor/receipts-extractor.ipynb` to Snowflake
   - Or copy cells into Snowflake Notebooks UI

### Extract Receipt Data

The `receipts-extractor.ipynb` Snowflake Notebook provides:

1. **AI-Powered Parsing**: Uses `AI_PARSE_DOCUMENT` to extract text from PDFs
2. **Structured Extraction**: Uses `AI_COMPLETE` with custom schema to extract:
   - Vendor and transaction details
   - Campaign information (display/video formats)
   - Financial totals
   - Performance metrics (CPM, CTR, Bounce Rate)
   - Targeting parameters
   - Line items
3. **Analytics Tables**: Creates queryable tables for analysis
4. **Example Queries**: Spending by vendor, campaign type analysis, pricing model comparison

### Tables Created

- `parsed_receipts` - Raw text extracted from PDFs
- `extracted_receipt_data` - Structured JSON data
- `receipt_analytics` - Flattened table ready for dashboards and reporting

### Files

- `setup.sql` - Snowflake database/schema/stage setup
- `receipts-extractor.ipynb` - Snowflake Notebook for AI extraction

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

### Automated Continuous Receipt Generation

Generate and upload 250 receipts every hour using cron:

#### 1. Create Automation Script

Create `scripts/generate_and_upload.sh`:

```bash
#!/bin/bash
# Automated receipt generation and upload script
# Generates 250 receipts per hour and uploads to Snowflake

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"

# Log file with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/receipt_automation_${TIMESTAMP}.log"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "========================================="
log "Starting receipt generation and upload"
log "========================================="

# Step 1: Generate 250 receipts
log "Step 1: Generating 250 receipts..."
cd "$PROJECT_ROOT/receipts.synthesis"
python receipt_generator.py -n 250 -o "$PROJECT_ROOT/receipts" >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "✓ Successfully generated 250 receipts"
else
    log "✗ Error generating receipts"
    exit 1
fi

# Step 2: Upload to Snowflake
log "Step 2: Uploading receipts to Snowflake..."
cd "$PROJECT_ROOT/receipts-uploader"
source venv/bin/activate
python upload_receipts.py >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "✓ Successfully uploaded receipts to Snowflake"
else
    log "✗ Error uploading receipts"
    exit 1
fi

log "========================================="
log "Automation cycle complete"
log "========================================="

# Clean up old log files (keep last 30 days)
find "$LOG_DIR" -name "receipt_automation_*.log" -mtime +30 -delete

exit 0
```

#### 2. Make Script Executable

```bash
chmod +x scripts/generate_and_upload.sh
```

#### 3. Configure Cron Job

Edit your crontab:

```bash
crontab -e
```

Add this line to run every hour:

```cron
# Generate and upload 250 receipts every hour
0 * * * * /path/to/Receipts.extraction/scripts/generate_and_upload.sh

# Example: Run at 5 minutes past every hour
5 * * * * /path/to/Receipts.extraction/scripts/generate_and_upload.sh

# Example: Run every 2 hours
0 */2 * * * /path/to/Receipts.extraction/scripts/generate_and_upload.sh
```

Replace `/path/to/Receipts.extraction` with the actual absolute path to your project.

#### 4. Verify Cron Setup

```bash
# List current cron jobs
crontab -l

# View logs
tail -f logs/receipt_automation_*.log
```

#### 5. Cron Schedule Examples

```cron
# Every hour
0 * * * * /path/to/scripts/generate_and_upload.sh

# Every 30 minutes
*/30 * * * * /path/to/scripts/generate_and_upload.sh

# Every 6 hours
0 */6 * * * /path/to/scripts/generate_and_upload.sh

# Monday-Friday 9 AM - 5 PM hourly
0 9-17 * * 1-5 /path/to/scripts/generate_and_upload.sh

# Weekdays every 2 hours during business hours
0 9-17/2 * * 1-5 /path/to/scripts/generate_and_upload.sh
```

#### 6. Monitor and Manage

```bash
# View recent logs
ls -lh logs/

# Check last automation run
tail -20 logs/receipt_automation_$(ls -t logs/ | head -1)

# Disable cron job (comment out)
crontab -e
# Add # in front of the line

# Remove cron job entirely
crontab -r  # WARNING: Removes ALL cron jobs for current user
```

#### Prerequisites for Automation

1. ✅ Python virtual environment set up in `receipts-uploader/venv/`
2. ✅ Service account configured with credentials in `config.json`
3. ✅ All dependencies installed in both `receipts.synthesis` and `receipts-uploader`
4. ✅ Snowflake stage created (`RECEIPTS_PROCESSING_DB.RAW.RECEIPTS`)
5. ✅ Write permissions to project directories

#### Production Considerations

- **Error Handling**: Logs capture all errors with timestamps
- **Log Rotation**: Old logs automatically deleted after 30 days
- **Idempotent**: Safe to re-run; uploads only new files
- **Resource Usage**: Adjust generation count based on processing capacity
- **Monitoring**: Set up alerts for failed automation runs

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

