"""Test script to verify all vendor templates work correctly."""
from receipt_generator_v2 import ReceiptGeneratorV2


def test_all_templates():
    """Test each vendor template by generating one receipt."""
    generator = ReceiptGeneratorV2(output_dir="../receipts_test_v2")
    
    print("Testing all vendor templates with pricing tables...")
    print("=" * 60)
    
    for idx, vendor_name in enumerate(generator.vendor_names):
        print(f"\nTesting Template {idx}: {vendor_name}")
        try:
            filepath = generator.generate_single_receipt(vendor_index=idx)
            print(f"✓ Success: {filepath}")
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False
    
    print("\n" + "=" * 60)
    print(f"✓ All {len(generator.vendor_names)} templates tested successfully!")
    print(f"   Test receipts saved to: {generator.output_dir}/")
    return True


if __name__ == "__main__":
    test_all_templates()

