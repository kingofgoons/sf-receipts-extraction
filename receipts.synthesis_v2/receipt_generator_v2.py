"""Main receipt generator script for creating synthetic receipts with pricing tables."""
import os
import random
from datetime import datetime
from reportlab.pdfgen import canvas
from data_generator_v2 import DataGeneratorV2
from vendors_v2 import VENDOR_TEMPLATES_V2, VENDOR_NAMES_V2


class ReceiptGeneratorV2:
    """Generate synthetic receipts with pricing tables in various vendor styles."""
    
    def __init__(self, output_dir="../receipts"):
        """
        Initialize the receipt generator.
        
        Args:
            output_dir: Directory to save generated PDFs (default: ../receipts)
        """
        self.output_dir = output_dir
        self.data_generator = DataGeneratorV2()
        self.templates = VENDOR_TEMPLATES_V2
        self.vendor_names = VENDOR_NAMES_V2
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_single_receipt(self, vendor_index=None, filename=None):
        """
        Generate a single receipt PDF with pricing tables.
        
        Args:
            vendor_index: Index of the vendor template to use (0-2). If None, random.
            filename: Custom filename for the PDF. If None, auto-generated.
        
        Returns:
            Path to the generated PDF file
        """
        # Select vendor template
        if vendor_index is None:
            vendor_index = random.randint(0, len(self.templates) - 1)
        else:
            vendor_index = vendor_index % len(self.templates)
        
        template = self.templates[vendor_index]
        vendor_name = self.vendor_names[vendor_index]
        
        # Generate synthetic data
        data = self.data_generator.generate_receipt_data()
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            safe_vendor_name = vendor_name.replace(" ", "_").replace("/", "_")
            filename = f"receipt_v2_{safe_vendor_name}_{timestamp}.pdf"
        
        # Ensure .pdf extension
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF
        c = canvas.Canvas(filepath)
        template(c, data)
        c.save()
        
        return filepath
    
    def generate_batch(self, count=10, vendor_index=None):
        """
        Generate a batch of receipts.
        
        Args:
            count: Number of receipts to generate
            vendor_index: Specific vendor index to use. If None, randomly selected for each.
        
        Returns:
            List of paths to generated PDF files
        """
        generated_files = []
        
        for i in range(count):
            try:
                if vendor_index is None:
                    # Random vendor for each receipt
                    selected_vendor = random.randint(0, len(self.templates) - 1)
                else:
                    selected_vendor = vendor_index
                
                filepath = self.generate_single_receipt(vendor_index=selected_vendor)
                generated_files.append(filepath)
                print(f"Generated ({i+1}/{count}): {os.path.basename(filepath)}")
            except Exception as e:
                print(f"Error generating receipt {i+1}: {e}")
        
        return generated_files
    
    def generate_sample_set(self, receipts_per_vendor=2):
        """
        Generate a sample set with receipts from each vendor.
        
        Args:
            receipts_per_vendor: Number of receipts to generate per vendor (default: 2)
        
        Returns:
            List of paths to generated PDF files
        """
        generated_files = []
        total_vendors = len(self.templates)
        
        print(f"Generating sample set: {receipts_per_vendor} receipts × {total_vendors} vendors = {receipts_per_vendor * total_vendors} total receipts")
        
        for vendor_idx in range(total_vendors):
            vendor_name = self.vendor_names[vendor_idx]
            print(f"\nGenerating from vendor {vendor_idx+1}/{total_vendors}: {vendor_name}")
            
            for i in range(receipts_per_vendor):
                try:
                    filepath = self.generate_single_receipt(vendor_index=vendor_idx)
                    generated_files.append(filepath)
                    print(f"  Generated ({i+1}/{receipts_per_vendor}): {os.path.basename(filepath)}")
                except Exception as e:
                    print(f"  Error generating receipt {i+1} for {vendor_name}: {e}")
        
        return generated_files
    
    def list_vendors(self):
        """List all available vendor templates."""
        print(f"\nAvailable Vendor Templates ({len(self.vendor_names)}):")
        print("=" * 50)
        for idx, vendor_name in enumerate(self.vendor_names):
            print(f"{idx}: {vendor_name}")
        print("=" * 50)


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate synthetic receipts with pricing tables in PDF format"
    )
    parser.add_argument(
        '-n', '--count',
        type=int,
        default=10,
        help='Number of receipts to generate (default: 10)'
    )
    parser.add_argument(
        '-v', '--vendor',
        type=int,
        help='Specific vendor index (0-2) to use. If not specified, random vendors are used.'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='../receipts',
        help='Output directory for generated PDFs (default: ../receipts)'
    )
    parser.add_argument(
        '--sample',
        action='store_true',
        help='Generate a sample set with receipts from each vendor (2 per vendor)'
    )
    parser.add_argument(
        '--list-vendors',
        action='store_true',
        help='List all available vendor templates'
    )
    
    args = parser.parse_args()
    
    generator = ReceiptGeneratorV2(output_dir=args.output)
    
    if args.list_vendors:
        generator.list_vendors()
        return
    
    if args.sample:
        print("Generating sample set...")
        files = generator.generate_sample_set()
        print(f"\n✓ Successfully generated {len(files)} sample receipts")
    else:
        print(f"Generating {args.count} receipts with pricing tables...")
        files = generator.generate_batch(count=args.count, vendor_index=args.vendor)
        print(f"\n✓ Successfully generated {len(files)} receipts")
    
    print(f"   Output directory: {os.path.abspath(generator.output_dir)}")


if __name__ == "__main__":
    main()

