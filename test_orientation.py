from PIL import Image
import os

# Test with a vertical image
vertical_img = Image.new('RGB', (100, 200), color='red')
vertical_img.save('test_vertical.png')

# Test with a horizontal image  
horizontal_img = Image.new('RGB', (200, 100), color='blue')
horizontal_img.save('test_horizontal.png')

print('Created test images')
print('Vertical image size:', vertical_img.size)
print('Horizontal image size:', horizontal_img.size)

# Test the orientation detection logic
def test_orientation():
    # Test vertical image
    v_img = Image.open('test_vertical.png')
    width, height = v_img.size
    is_vertical = height > width
    print(f'Vertical image {v_img.size}: is_vertical = {is_vertical}')
    
    # Test horizontal image
    h_img = Image.open('test_horizontal.png')
    width, height = h_img.size
    is_horizontal = width > height
    print(f'Horizontal image {h_img.size}: is_horizontal = {is_horizontal}')

test_orientation()
