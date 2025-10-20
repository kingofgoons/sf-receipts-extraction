"""
Upload receipt files from local receipts/ folder to Snowflake stage.
Only uploads files that haven't been uploaded yet.
"""
import os
import sys
import json
import glob
from pathlib import Path
import snowflake.connector
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


# Path to the config file (relative to this script)
CONFIG_PATH = Path(__file__).parent / 'config.json'

# Path to the private key file (relative to this script)
PRIVATE_KEY_PATH = Path(__file__).parent.parent / 'rsa_key.p8'


def load_config(config_path):
    """Load configuration from config.json."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {config_path} not found.")
        print("Please copy config.template.json to config.json and fill in your credentials.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing {config_path}: {e}")
        sys.exit(1)


def load_private_key(private_key_path):
    """Load and parse the private key file."""
    try:
        with open(private_key_path, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        
        # Serialize the private key to PEM format
        pkb = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pkb
    except FileNotFoundError:
        print(f"Error: Private key file not found at {private_key_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading private key: {e}")
        sys.exit(1)


def connect_to_snowflake(config):
    """Connect to Snowflake using service account with key-pair authentication."""
    print("Connecting to Snowflake...")
    
    # Load private key
    private_key = load_private_key(PRIVATE_KEY_PATH)
    
    try:
        conn = snowflake.connector.connect(
            user=config['user'],
            account=config['account'],
            private_key=private_key,
            warehouse=config.get('warehouse'),
            database=config.get('database'),
            schema=config.get('schema'),
            role=config.get('role')
        )
        print(f"✓ Connected as {config['user']} using key-pair authentication")
        return conn
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        sys.exit(1)


def get_stage_files(conn, stage_name):
    """Get list of files already in the Snowflake stage."""
    print(f"\nChecking files in stage {stage_name}...")
    
    try:
        cursor = conn.cursor()
        # List files in the stage
        cursor.execute(f"LIST @{stage_name}")
        
        stage_files = set()
        for row in cursor.fetchall():
            # Row format: (name, size, md5, last_modified)
            file_path = row[0]  # Full path in stage
            # Extract just the filename
            filename = file_path.split('/')[-1]
            stage_files.add(filename)
        
        cursor.close()
        print(f"✓ Found {len(stage_files)} file(s) in stage")
        return stage_files
    except Exception as e:
        print(f"Warning: Could not list stage files: {e}")
        print("Assuming stage is empty...")
        return set()


def get_local_receipts(receipts_dir='../receipts'):
    """Get list of PDF files in the local receipts directory."""
    receipts_path = Path(receipts_dir)
    
    if not receipts_path.exists():
        print(f"Error: Receipts directory not found: {receipts_dir}")
        return []
    
    # Find all PDF files
    pdf_files = list(receipts_path.glob('*.pdf'))
    
    print(f"\n✓ Found {len(pdf_files)} PDF file(s) in local receipts directory")
    return pdf_files


def upload_file(conn, local_file, stage_name):
    """Upload a single file to the Snowflake stage."""
    try:
        cursor = conn.cursor()
        
        # Convert to absolute path for PUT command
        abs_path = os.path.abspath(local_file)
        
        # PUT command to upload file
        put_sql = f"PUT file://{abs_path} @{stage_name} AUTO_COMPRESS=FALSE OVERWRITE=FALSE"
        
        cursor.execute(put_sql)
        result = cursor.fetchone()
        cursor.close()
        
        # Check result status
        if result and 'UPLOADED' in str(result[6]).upper():
            return True
        elif result and 'SKIPPED' in str(result[6]).upper():
            return 'SKIPPED'
        else:
            return False
            
    except Exception as e:
        print(f"  Error uploading {local_file.name}: {e}")
        return False


def upload_receipts(config, receipts_dir='../receipts', stage_name='RECEIPTS_PROCESSING_DB.RAW.RECEIPTS'):
    """Main function to upload receipts to Snowflake stage."""
    print("=" * 70)
    print("Receipt Uploader - Snowflake Stage")
    print("=" * 70)
    
    # Connect to Snowflake
    conn = connect_to_snowflake(config)
    
    try:
        # Get local receipt files
        local_files = get_local_receipts(receipts_dir)
        
        if not local_files:
            print("\nNo receipt files found to upload.")
            return
        
        # Get files already in stage
        stage_files = get_stage_files(conn, stage_name)
        
        # Determine which files need to be uploaded
        files_to_upload = []
        for local_file in local_files:
            if local_file.name not in stage_files:
                files_to_upload.append(local_file)
        
        print(f"\n{'=' * 70}")
        print(f"Files to upload: {len(files_to_upload)} of {len(local_files)}")
        print(f"{'=' * 70}\n")
        
        if not files_to_upload:
            print("✓ All files are already uploaded to the stage!")
            return
        
        # Upload files
        uploaded_count = 0
        skipped_count = 0
        failed_count = 0
        
        for i, file_path in enumerate(files_to_upload, 1):
            print(f"Uploading ({i}/{len(files_to_upload)}): {file_path.name}...", end=' ')
            
            result = upload_file(conn, file_path, stage_name)
            
            if result is True:
                print("✓ UPLOADED")
                uploaded_count += 1
            elif result == 'SKIPPED':
                print("⊘ SKIPPED (already exists)")
                skipped_count += 1
            else:
                print("✗ FAILED")
                failed_count += 1
        
        # Summary
        print(f"\n{'=' * 70}")
        print("Upload Summary:")
        print(f"  Uploaded: {uploaded_count}")
        print(f"  Skipped:  {skipped_count}")
        print(f"  Failed:   {failed_count}")
        print(f"  Total:    {len(files_to_upload)}")
        print(f"{'=' * 70}")
        
        # Verify upload
        if uploaded_count > 0:
            print("\nVerifying stage contents...")
            cursor = conn.cursor()
            cursor.execute(f"LIST @{stage_name}")
            total_in_stage = len(cursor.fetchall())
            cursor.close()
            print(f"✓ Total files in stage: {total_in_stage}")
        
    finally:
        conn.close()
        print("\n✓ Connection closed")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Upload receipt PDFs from local folder to Snowflake stage"
    )
    parser.add_argument(
        '-d', '--directory',
        type=str,
        default='../receipts',
        help='Directory containing receipt PDFs (default: ../receipts)'
    )
    parser.add_argument(
        '-s', '--stage',
        type=str,
        default='RECEIPTS_PROCESSING_DB.RAW.RECEIPTS',
        help='Snowflake stage name (default: RECEIPTS_PROCESSING_DB.RAW.RECEIPTS)'
    )
    
    args = parser.parse_args()
    
    # Check if private key file exists
    if not PRIVATE_KEY_PATH.exists():
        print(f"Error: Private key file not found at {PRIVATE_KEY_PATH}")
        print("Please ensure rsa_key.p8 exists in the parent directory")
        sys.exit(1)
    
    # Load configuration
    print("Loading configuration from config.json...")
    config = load_config(CONFIG_PATH)
    
    # Check if account is configured
    if config.get('account') == 'YOUR_ACCOUNT_IDENTIFIER':
        print("Error: Please update the 'account' value in config.json")
        print("Replace 'YOUR_ACCOUNT_IDENTIFIER' with your actual Snowflake account identifier")
        sys.exit(1)
    
    print("✓ Configuration loaded successfully\n")
    
    # Upload receipts
    upload_receipts(config, args.directory, args.stage)


if __name__ == "__main__":
    main()

