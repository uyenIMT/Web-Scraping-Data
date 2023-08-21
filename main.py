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
    for i in range (1,2):
        url = f'{website}?page={sub_menu}&page={i}'
        response = requests.get(url)
        html_content = response.text

        links=[]

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
    
        # Extract links, images, titles, prices, area, and timestamps
        property_elements = soup.find_all('div', class_='dv-item')
    
        for property_element in property_elements:
            # Extract links
            link = property_element.find('a').get('href')
            links.append(link)

            for link in links:

                # Extract image URLs
                image_element = property_element.find('img', class_='imageThumb')
                image_url = image_element.get('data-src') if image_element else ''
        
                # Extract ID
                pattern = r'ID(\d+)'
                match = re.search(pattern, link)
                if match:
                    extracted_id = match.group(1)
                    #print(extracted_id)
                else:
                    print("ID not found in the link.")

                # Extract title of posts
                title_element = property_element.find('h1', id='txtcontenttieudetin')
                if title_element is not None:
                    title = title_element.get_text()
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
                location_element = property_element.find('label', class_='lb-pri-dt')
                if location_element is not None:
                    location = location_element.text.strip()
                else:
                    location = 'N/A'
        
                # Extract the area
                area_element = property_element.find('label', class_='strong2')
                if area_element is not None:
                    area = area_element.text.strip()
                else:
                    area = 'N/A'
        
                # Extract the timestamp
                timestamp_elements = property_element.find('label', id='ContentPlaceHolder1_ct100_lbDate')
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
                direction_elements = property_element.find('label', class_='ContentPlaceHolder1_ct100_lbHuong')
                if direction_elements:
                    text_element = direction_elements.find_next_sibling(string=True)
                    if text_element:
                        direction = text_element.strip()
                    else:
                        direction = 'N/A'
                else:
                    direction = 'N/A'
                
                # Extract the number of floor
                floor_elements = property_element.find('td', class_='col1')
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

                # Extract the "Mat-tien"
                mt_elements = property_element.find('i', class_='fa-arrows-alt')
                if mt_elements:
                    text_element = mt_elements.find_next_sibling(string=True)
                    if text_element:
                        mt = text_element.replace("Mặt tiền:", "").strip()
                    else:
                        mt = 'N/A'
                else:
                    mt = 'N/A'
                
                # Extract the parking slots
                park_elements = property_element.find('i', class_='fa-car')
                if park_elements:
                    text_element = park_elements.find_next_sibling(string=True)
                    if text_element:
                        park = text_element.replace("Chỗ để ôtô", "").strip()
                    else:
                        park = 'N/A'
                else:
                    park = 'N/A'

                # Extract the road width
                road_elements = property_element.find('i', class_='fa-road')
                if road_elements:
                    text_element = road_elements.find_next_sibling(string=True)
                    if text_element:
                        road = text_element.replace("Đường vào: Rộng ", "").strip()
                    else:
                        road = 'N/A'
                else:
                    road = 'N/A'

                # Extract the description
                des_element = property_element.find('label', class_='lb-des')
                if des_element is not None:
                    des = des_element.text.strip()
                else:
                    des = 'N/A'

                # Extract the seller
                seller_element = property_element.find('div', class_='fullname')
                if seller_element is not None:
                    seller = seller_element.text.strip()
                else:
                    seller = 'N/A'

                # Extract the contact of seller
                contact_element = property_element.find('a', class_='call')
                if contact_element:
                    contact = re.search(r'\d{10}', contact_element['viewmobinumber']).group()
                else:
                    contact = "N/A"
                
            property_data = {
                'Data source': 'nhadat24h.net',
                'Agent': 'Uyen Nguyen',
                'Category': sub_menu,
                'ID': extracted_id,
                'Title': title,
                'Post link': link,
                'Price': price,
                'Area': area,
                'Location': location,
                'Timestamp': timestamp,
                # 'Estate type':,
                # 'Certification status':,
                'Direction': direction,
                # 'Rooms':,
                'Bedrooms': bedroom,
                # 'Kitchen':,
                # 'Living room':,
                'Bathrooms': wc,
                'Front width': mt,
                'Floor': floor,
                'Parking slot': park,
                'Description': des,
                'Seller name': seller,
                # 'Seller type':,
                'Phone': contact,
                # 'Images':,
                'Image URL': image_url,
                # 'Email':,
                'Road width': road,
                # 'Sizes':   
            }
            print(property_data)
            data.append(property_data)
print("End scraping")

print('Start downloading images')
# Create a directory to store the downloaded images
os.makedirs('scraped_images5', exist_ok=True)

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

    filename = f'scraped_images5/image_{title}.jpg'  # Modify the filename as needed
    with open(filename, 'wb') as file:
        file.write(image_content)
print("End downloading images")
     
print('Writing CSV file')
# Specify the CSV file path
csv_file = 'scraped_data5.csv'

# Write the data to CSV
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['Data source','Agent','Category','ID','Title','Post link', 'Price','Area','Location','Timestamp','Direction','Bedrooms', 'Bathrooms','Front width', 'Floor', 'Parking slot','Description','Seller name','Phone','Image URL','Road width']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # Write the header row
    writer.writerows(data)  # Write the data rows


print(f'Scraped data and images are saved successfully.')
