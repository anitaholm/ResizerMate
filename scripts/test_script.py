from script import process_image
from PIL import Image
import os

# Test with vertical image
print("Testing with vertical image...")
if os.path.exists('input/vertical.png'):
    img = Image.open('input/vertical.png')
    print(f"Vertical image size: {img.size}")
    print(f"Is vertical: {img.size[1] > img.size[0]}")
    
    # Create test output directory
    test_output = "test_output_vertical"
    if not os.path.exists(test_output):
        os.makedirs(test_output)
    
    # Process a small subset to test
    process_image('input/vertical.png', test_output, 'Test')
    print("Vertical image processed successfully!")

# Test with horizontal image
print("\nTesting with horizontal image...")
if os.path.exists('input/horizontal.png'):
    img = Image.open('input/horizontal.png')
    print(f"Horizontal image size: {img.size}")
    print(f"Is horizontal: {img.size[0] > img.size[1]}")
    
    # Create test output directory
    test_output = "test_output_horizontal"
    if not os.path.exists(test_output):
        os.makedirs(test_output)
    
    # Process a small subset to test
    process_image('input/horizontal.png', test_output, 'Test')
    print("Horizontal image processed successfully!")
