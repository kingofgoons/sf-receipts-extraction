"""Main receipt generator script for creating synthetic ad-campaign receipts."""
import os
import random
from datetime import datetime
from reportlab.pdfgen import canvas
from data_generator import DataGenerator
from vendors import VENDOR_TEMPLATES, VENDOR_NAMES


class ReceiptGenerator:
    """Generate synthetic ad-campaign receipts in various vendor styles."""
    
    def __init__(self, output_dir="output"):
        """
        Initialize the receipt generator.
        
        Args:
            output_dir: Directory to save generated PDFs
        """
        self.output_dir = output_dir
        self.data_generator = DataGenerator()
        self.templates = VENDOR_TEMPLATES
        self.vendor_names = VENDOR_NAMES
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_single_receipt(self, vendor_index=None, filename=None):
        """
        Generate a single receipt PDF.
        
        Args:
            vendor_index: Index of the vendor template to use (0-21). If None, random.
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
            filename = f"receipt_{safe_vendor_name}_{timestamp}.pdf"
        
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
            receipts_per_vendor: Number of receipts to generate per vendor style
        
        Returns:
            Dictionary mapping vendor names to lists of generated file paths
        """
        results = {}
        
        for i, vendor_name in enumerate(self.vendor_names):
            print(f"\nGenerating receipts for {vendor_name}...")
            vendor_files = []
            
            for j in range(receipts_per_vendor):
                try:
                    filepath = self.generate_single_receipt(vendor_index=i)
                    vendor_files.append(filepath)
                    print(f"  Generated ({j+1}/{receipts_per_vendor}): {os.path.basename(filepath)}")
                except Exception as e:
                    print(f"  Error generating receipt {j+1}: {e}")
            
            results[vendor_name] = vendor_files
        
        return results
    
    def get_vendor_count(self):
        """Get the number of available vendor templates."""
        return len(self.templates)
    
    def list_vendors(self):
        """List all available vendor names."""
        return self.vendor_names.copy()


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate synthetic ad-campaign receipts in PDF format"
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
        help='Specific vendor index (0-21) to use. If not specified, random vendors are used.'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='output',
        help='Output directory for generated PDFs (default: output)'
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
    
    # Initialize generator
    generator = ReceiptGenerator(output_dir=args.output)
    
    # List vendors if requested
    if args.list_vendors:
        print("Available vendor templates:")
        for i, vendor in enumerate(generator.list_vendors()):
            print(f"  {i}: {vendor}")
        return
    
    # Generate sample set if requested
    if args.sample:
        print(f"Generating sample set with receipts from all {generator.get_vendor_count()} vendors...")
        results = generator.generate_sample_set()
        total = sum(len(files) for files in results.values())
        print(f"\n✓ Successfully generated {total} receipts in '{args.output}' directory")
        return
    
    # Generate batch
    print(f"Generating {args.count} receipts...")
    if args.vendor is not None:
        vendor_name = generator.vendor_names[args.vendor % len(generator.vendor_names)]
        print(f"Using vendor: {vendor_name}")
    else:
        print("Using random vendors")
    
    files = generator.generate_batch(count=args.count, vendor_index=args.vendor)
    print(f"\n✓ Successfully generated {len(files)} receipts in '{args.output}' directory")


if __name__ == "__main__":
    main()


