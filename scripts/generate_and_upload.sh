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

