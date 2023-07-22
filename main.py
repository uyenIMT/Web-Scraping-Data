import requests
from bs4 import BeautifulSoup
import csv
import os
import base64
import re
from timestamp_utils import convert_relative_to_exact_timestamp

# Send a GET request to the website and retrieve the HTML content
website = 'https://nhadat24h.net'
response = requests.get(website)
html_content = response.text

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the elements with class 'col_1'
sub_elements = soup.find_all('ul', class_='')

sub_menus = []  # Create an empty list to store the extracted sub menus

for sub_element in sub_elements:
    # Extract the href attribute from the <a> element within each <li> element
    sub_menu_items = sub_element.find_all('li', class_='nav-submenu-item')
    
    for sub_menu_item in sub_menu_items:
        sub_menu = sub_menu_item.find('a').get('href')
        sub_menus.append(sub_menu)
print(sub_menus)
data = []  # Create an empty list to store the scraped data

for sub_menu in sub_menus:
    for i in range (1,16):
        url = f'{website}?page={sub_menu}&page={i}'
        response = requests.get(url)
        html_content = response.text
    
        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
    
        # Extract links, images, titles, prices, area, and timestamps
        property_elements = soup.find_all('div', class_='dv-item')
    
        for property_element in property_elements:
            # Extract image URLs
            image_element = property_element.find('img', class_='imageThumb1')
            image_url = image_element.get('data-src') if image_element else ''
    
            # Extract links
            link = property_element.find('a').get('href')
    
            # Extract title of posts
            title_element = property_element.find('a').get('title')
            if title_element is not None:
                title = title_element.strip()
                # Remove or replace special characters in the title
                title = re.sub(r'[\/:*?"<>|]', '_', title)
            else:
                title = 'N/A'
    
            # Extract the price
            price_element = property_element.find('label', class_='a-txt-cl1')
            if price_element is not None:
                price = price_element.text.strip()
            else:
                price = 'N/A'
            
            # Extract the location
            location_element = property_element.find('label', class_='rvVitri')
            if location_element is not None:
                location = location_element.text.strip()
            else:
                location = 'N/A'
    
            # Extract the area
            area_element = property_element.find('label', class_='a-txt-cl2')
            if area_element is not None:
                area = area_element.text.strip()
            else:
                area = 'N/A'
    
            # Extract the direction
            timestamp_elements = property_element.find('i', class_='fa-clock-o')
            if timestamp_elements:
                timestamp = timestamp_elements.find_next_sibling(string=True)
                if timestamp:
                    timestamp = timestamp.strip()
                    timestamp = convert_relative_to_exact_timestamp(timestamp)
                else:
                    timestamp = 'N/A'
            else:
                timestamp = 'N/A'
                        
            # Extract the direction
            direction_elements = property_element.find('i', class_='fa-compass')
            if direction_elements:
                text_element = direction_elements.find_next_sibling(string=True)
                if text_element:
                    extracted_text = text_element.strip()
                    # Remove the word "Hướng:" from the output
                    direction = extracted_text.replace("Hướng:", "").strip()
                else:
                    direction = 'N/A'
            else:
                direction = 'N/A'
            
            # Extract the number of floor
            floor_elements = property_element.find('i', class_='fa-building')
            if floor_elements:
                text_element = floor_elements.find_next_sibling(string=True)
                if text_element:
                    floor = text_element.replace("tầng", "").strip()
                else:
                    floor = 'N/A'
            else:
                floor = 'N/A'
                                
            # Extract the number of bedroom
            bedroom_elements = property_element.find('i', class_='fa-bed')
            if bedroom_elements:
                text_element = bedroom_elements.find_next_sibling(string=True)
                if text_element:
                    bedroom = text_element.replace("Phòng ngủ", "").strip()
                else:
                    bedroom = 'N/A'
            else:
                bedroom = 'N/A'
            
            # Extract the number of wc
            wc_elements = property_element.find('i', class_='fa-bath')
            if wc_elements:
                text_element = wc_elements.find_next_sibling(string=True)
                if text_element:
                    wc = text_element.replace("WC", "").strip()
                else:
                    wc = 'N/A'
            else:
                wc = 'N/A'
                
            property_data = {
                'Category': sub_menu,
                'Title': title,
                'Price': price,
                'Location': location,
                'Area': area,
                'Timestamp': timestamp,
                'Direction': direction,
                'Floor': floor,
                'Bedroom': bedroom,
                'Bathroom': wc,
                'Link': link,
                'Image URL': image_url
            }
            data.append(property_data)


# Print the scraped data for all properties
# for property_data in data:
#     print(f"Category: {sub_menus})
#     print(f"Title: {property_data['Title']}")
#     print(f"Price: {property_data['Price']}")
#     print(f"Area: {property_data['Area']}")
#     print(f"Timestamp: {property_data['Timestamp']}")
#     print(f"Link: {property_data['Link']}")
#     print()

# Create a directory to store the downloaded images
os.makedirs('scraped_images', exist_ok=True)

# Download the images
for property_data in data:
    image_url = property_data['Image URL']
    title = property_data['Title']

    # Skip the property if it doesn't have an image
    if not image_url:
        continue

    # Replace invalid characters in the title
    title = re.sub(r'[\/:*?"<>|]', '_', title)

    if image_url.startswith('data:image'):  # Check if it's a base64-encoded image
        # Extract the base64 data part
        encoded_image = image_url.split(',', 1)[1]

        # Decode the base64 data
        image_content = base64.b64decode(encoded_image)
    else:  # Regular image URL
        response = requests.get(image_url)
        image_content = response.content

    filename = f'scraped_images/image_{title}.jpg'  # Modify the filename as needed
    with open(filename, 'wb') as file:
        file.write(image_content)
        
print('Writing CSV file')
# Specify the CSV file path
csv_file = 'scraped_data.csv'

# Write the data to CSV
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['Category','Title', 'Price','Location', 'Area', 'Timestamp','Direction', 'Floor', 'Bedroom', 'Bathroom','Link', 'Image URL']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # Write the header row
    writer.writerows(data)  # Write the data rows


print(f'Scraped data and images are saved successfully.')
