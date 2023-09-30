import requests
import os
import base64
import re
import pandas as pd

def download_images(csv_file_path, output_folder):
    # Load CSV data
    data = pd.read_csv(csv_file_path)

    print('Start downloading images')

    # Create a directory to store the downloaded images
    os.makedirs(output_folder, exist_ok=True)

    images_filename = []
    # Download the images
    for idx, property_data in data.iterrows():  # Iterate through rows
        image_url = property_data['Image URL']
        title = property_data['Title']

        # Skip the property if it doesn't have an image
        if pd.isna(image_url):
            continue

        # Replace invalid characters in the title
        title = re.sub(r'[\/:*?"<>|]', '_', title)

        try:
            if image_url.startswith('data:image'):  # Check if it's a base64-encoded image
                # Extract the base64 data part
                encoded_image = image_url.split(',', 1)[1]

                # Decode the base64 data
                image_content = base64.b64decode(encoded_image)
            else:  # Regular image URL
                response = requests.get(image_url)
                response.raise_for_status()  # Raise an exception for non-200 status codes
                image_content = response.content

            # Ensure filename uniqueness
            filename = os.path.join(output_folder,f'image_{title}_{idx}.jpg')
            with open(filename, 'wb') as file:
                file.write(image_content)
        except Exception as e:
            print(f"Error downloading image for '{title}': {e}")

    print("End downloading images")

csv_file_path = ' .csv'  # Replace with your CSV file path
output_folder = 'folder_name'
download_images(csv_file_path, output_folder)
