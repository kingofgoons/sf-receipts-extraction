"""Quick test script to verify the receipt generator works correctly."""
from receipt_generator import ReceiptGenerator
import os


def test_generator():
    """Test the receipt generator with all templates."""
    print("Testing Receipt Generator...")
    print("="*60)
    
    # Initialize generator (using default ../receipts directory)
    generator = ReceiptGenerator()
    output_dir = generator.output_dir
    
    print(f"\n✓ Generator initialized with {generator.get_vendor_count()} vendor templates")
    
    # Test 1: Generate one receipt from each vendor
    print("\nTest 1: Generating one receipt from each vendor template...")
    success_count = 0
    failed = []
    
    for i in range(generator.get_vendor_count()):
        try:
            receipt_path = generator.generate_single_receipt(vendor_index=i)
            if os.path.exists(receipt_path):
                success_count += 1
                print(f"  ✓ Template {i+1:2d}/{generator.get_vendor_count()}: {generator.vendor_names[i]}")
            else:
                failed.append(generator.vendor_names[i])
                print(f"  ✗ Template {i+1:2d}/{generator.get_vendor_count()}: {generator.vendor_names[i]} - File not created")
        except Exception as e:
            failed.append(generator.vendor_names[i])
            print(f"  ✗ Template {i+1:2d}/{generator.get_vendor_count()}: {generator.vendor_names[i]} - Error: {str(e)}")
    
    print("\n" + "="*60)
    print(f"Results: {success_count}/{generator.get_vendor_count()} templates succeeded")
    
    if failed:
        print(f"\nFailed templates: {', '.join(failed)}")
        return False
    else:
        print(f"\n✓ All templates generated successfully!")
        print(f"✓ Receipts saved to: {output_dir}/")
        return True


if __name__ == "__main__":
    success = test_generator()
    exit(0 if success else 1)

