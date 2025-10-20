"""Example usage of the receipt generator."""
from receipt_generator import ReceiptGenerator


def main():
    """Demonstrate various ways to use the receipt generator."""
    
    print("="*60)
    print("Synthetic Ad-Campaign Receipt Generator - Examples")
    print("="*60)
    
    # Initialize the generator
    generator = ReceiptGenerator(output_dir="example_output")
    
    print(f"\n✓ Initialized generator with {generator.get_vendor_count()} vendor templates")
    
    # Example 1: Generate a single receipt with random vendor
    print("\n" + "="*60)
    print("Example 1: Generate a single receipt (random vendor)")
    print("="*60)
    receipt = generator.generate_single_receipt()
    print(f"✓ Generated: {receipt}")
    
    # Example 2: Generate a single receipt from specific vendor
    print("\n" + "="*60)
    print("Example 2: Generate receipt from 'Creative Campaigns' (vendor #2)")
    print("="*60)
    receipt = generator.generate_single_receipt(vendor_index=2)
    print(f"✓ Generated: {receipt}")
    
    # Example 3: Generate a batch of 5 receipts with random vendors
    print("\n" + "="*60)
    print("Example 3: Generate batch of 5 receipts (random vendors)")
    print("="*60)
    receipts = generator.generate_batch(count=5)
    print(f"✓ Generated {len(receipts)} receipts")
    
    # Example 4: Generate 3 receipts from the same vendor
    print("\n" + "="*60)
    print("Example 4: Generate 3 receipts from 'Apex Media' (vendor #4)")
    print("="*60)
    receipts = generator.generate_batch(count=3, vendor_index=4)
    print(f"✓ Generated {len(receipts)} receipts")
    
    # Example 5: List all vendors
    print("\n" + "="*60)
    print("Example 5: List all available vendors")
    print("="*60)
    vendors = generator.list_vendors()
    for i, vendor in enumerate(vendors):
        print(f"  {i:2d}. {vendor}")
    
    # Example 6: Generate one receipt from each vendor
    print("\n" + "="*60)
    print("Example 6: Generate sample set (1 receipt per vendor)")
    print("="*60)
    sample_set = generator.generate_sample_set(receipts_per_vendor=1)
    total = sum(len(files) for files in sample_set.values())
    print(f"\n✓ Generated {total} receipts across {len(sample_set)} vendors")
    
    print("\n" + "="*60)
    print("All examples completed!")
    print(f"Check the 'example_output' directory for generated PDFs")
    print("="*60)


if __name__ == "__main__":
    main()


