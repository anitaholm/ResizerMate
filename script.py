import os
import sys

def main(input_image_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    base_name = os.path.splitext(os.path.basename(input_image_path))[0]
    print(base_name)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_image_path> <output_folder>")
        sys.exit(1)

input_image_path = sys.argv[1]
output_path = sys.argv[2]
main(input_image_path, output_path)
    