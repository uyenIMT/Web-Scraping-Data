import requests
from bs4 import BeautifulSoup
import csv
import re
from urllib.parse import unquote
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
data = []
csv_file = 'scraped_data17.csv'

# Write the header row to the CSV file
with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
    fieldnames = ['Data source','Agent','Category','ID','Title','Post link', 'Price','Area','Location','Timestamp','Estate type','Certification status','Direction','Rooms','Bedrooms','Kitchen','Living room','Bathrooms','Front width','Floor', 'Parking slot','Description','Seller name','Seller type','Phone','Images','Image URL','Email','Road width','Sizes']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # Write the header row

sub_menu_data = {}

for sub_menu in sub_menus:
    links_for_sub_menu = []
    timestamps_for_sub_menu = []
    for i in range (1,11):
        url = f'{website}{sub_menu}/page{i}'
        # print(url)
        response = requests.get(url)
        html_content = response.text
        
        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
    
        # Extract links, images, titles, prices, area, and timestamps
        property_elements = soup.find_all('div', class_='dv-item')
    
        for soup in property_elements:
            # Extract links
            link = soup.find('a').get('href')
            links_for_sub_menu.append(link)
            # print(link)
    
            # Extract the timestamp
            icon_element = soup.find('i', class_='fa-clock-o')
            if icon_element:
                timestamp = icon_element.find_parent('p').text.strip()
                exact_timestamp = convert_relative_to_exact_timestamp(timestamp).strftime("%d/%m/%Y, %H:%M:%S")
                timestamps_for_sub_menu.append(exact_timestamp)
                # print(exact_timestamp)
            else:
                timestamps_for_sub_menu.append(' ')

    # Store the sub-menu, links, and timestamps within the property data
    property_data = {
        'Category': sub_menu,
        'Post link': links_for_sub_menu,
        'Timestamp': timestamps_for_sub_menu
    }

    # Append the property data to the list
    data.append(property_data)

for property_data in data:
    sub_menu = property_data['Category']
    links = property_data['Post link']
    timestamps = property_data['Timestamp']
    for link, timestamp in zip(links, timestamps):
        url = f'{website}{link}'
        try:
            response = requests.get(url)
        # Check the response status code to see if the request was successful
            if response.status_code == 200:
            # Process the response content as needed
            # Your processing code here
                print(f"Successfully fetched data from {url} at timestamp {timestamp}")
            else:
                print(f"Request to {url} returned status code {response.status_code} at timestamp {timestamp}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect to {url} at timestamp {timestamp}. Exception: {e}")
        # response = requests.get(url)
        html_content = response.text

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract links, images, titles, prices, area, and timestamps
        property_elements = soup.find_all('div', class_='ct-in-all')

        # Extract image URLs
        image_element = soup.find('img', class_='imageThumb')
        image_url = image_element.get('data-src') if image_element else ''

        # Extract ID
        pattern = r'ID(\d+)'
        match = re.search(pattern, url)
        if match:
            extracted_id = match.group(1)
            # print(extracted_id)
        else:
            extracted_id = ' '
            print("ID not found in the link.")

        # Extract title of posts
        title_element = soup.find('h1', id='txtcontenttieudetin')
        if title_element is not None:
            title = title_element.text.strip()
        else:
            title = ' '

        # Extract the price
        price_element = soup.find('label', class_='lb-pri-dt')
        if price_element:
            price_text = price_element.get_text()

            # Use regular expression to extract the numeric part and the unit
            price_match = re.search(r'(\d+)\s*(\S+)\s*-', price_text)
            
            if price_match:
                price_amount = price_match.group(1)
                price_unit = price_match.group(2)
                price = f"{price_amount} {price_unit}"
            else:
                price = ' '
        else:
            price = ' '

        # Extract the location
        location_element = soup.find('label', id='ContentPlaceHolder1_ctl00_lbTinhThanh')
        if location_element is not None:
            location = location_element.text.strip()
        else:
            location = ' '

        # Extract the area
        area_element = soup.find('label', class_='lb-pri-dt')  
        if area_element:
            # Find the area amount within the strong2 class
            area_amount_element = area_element.find('label', class_='strong2')
            if area_amount_element:
                area_amount = area_amount_element.get_text().strip()

                # Find the area unit (text before the area amount)
                area_unit_element = area_element.contents[4].strip()

                area = f"{area_amount} {area_unit_element}"
            else:
                area = ' '
        else:
            area = ' '
                
        # Extract the direction
        direction_element = soup.find('label', id='ContentPlaceHolder1_ctl00_lbHuong')
        if direction_element is not None:
            direction = direction_element.text.strip()
        else:
            direction = ' '


        # Extract the number of floor
        floor_element = soup.find('td', string='Số tầng')
        if floor_element:
            floor = floor_element.find_next('td').get_text(strip=True)
        else:
            floor = ' '

                            
        # Extract the number of bedroom
        br_element = soup.find('td', string='Phòng Ngủ')
        if br_element:
            br = br_element.find_next('td').get_text(strip=True)
        else:
            br = ' '

        # Extract the number of wc
        wc_element = soup.find('td', string='Phòng WC')
        if wc_element:
            wc = wc_element.find_next('td').get_text(strip=True) 
        else:
            wc = ' '

        # Extract the front width
        fw_element = soup.find('td', string='Mặt tiền')
        if fw_element:
            fw = fw_element.find_next('td').get_text(strip=True)
        else:
            fw = ' '

        # Extract the parking slots
        park_element = soup.find('td', string='Chỗ để xe')
        if park_element:
            park = park_element.find_next('td').get_text(strip=True)
        else:
            park = ' '

        # Extract the road width
        rw_element = soup.find('td', string='Đường vào')
        if rw_element:
            rw = rw_element.find_next('td').get_text(strip=True)
        else:
            rw = ' '

        # Extract the description
        des_element = soup.find('div', class_='dv-txt-mt')
        if des_element is not None:
            des = des_element.text.strip()
            des = re.sub(r'<br\s?/?>', ' ', des)
            des = re.sub(r'%\d+[a-zA-Z/]+%3e', ' ', des)  # Remove encoded entities like %3cbr/%3e
            des = re.sub(r'%\d{2}', ' ', des)  # Remove encoded entities like %29
            des = re.sub(r'%\d{1}a', ' ', des)
            des = re.sub(r'[^\w\s,.]+', ' ', des) # Remove special characters
            des = des.replace('\n', ' ')
        else:
            des = ' '

        # Extract the seller
        seller_element = soup.find('label', class_='fullname')
        if seller_element is not None:
            seller = seller_element.text.strip()
        else:
            seller = ' '

        # Extract the phone number of seller
        phone_element = soup.find('a', class_='call')
        if phone_element:
            phone_number = phone_element['href'].split(':')[-1]
            # print(phone_number)
        else:
            phone_number = ' '

        # Extract the estate type
        estate_type = soup.find('label', id='ContentPlaceHolder1_ctl00_lbLoaiBDS')
        if estate_type is not None:
            estate_type = estate_type.get_text()
        else:
            estate_type = ' '

        # Extract the seller type
        icon_element = soup.find('i', class_='fas fa-user')
        if icon_element:
            seller_type = icon_element.find_parent('label').text.strip()
        else:
            seller_type = ' '

        # Extract the Certification status
        cs_element = soup.find('div', class_= 'dv-time-dt')
        if cs_element:
            cs_strong_element = cs_element.find('strong')
            if cs_strong_element:
                cs = cs_strong_element.get_text(strip=True)
            else:
                cs = ' '
        else:
            cs = ' '

        property_data = {
            'Data source': 'nhadat24h.net',
            'Agent': 'Uyen Nguyen',
            'Category': sub_menu,
            'ID': extracted_id,
            'Title': title,
            'Price': price,
            'Location': location,
            'Area': area,
            'Timestamp': timestamp,
            'Direction': direction,
            'Floor': floor,
            'Bedrooms': br,
            'Bathrooms': wc,
            'Parking slot': park,
            'Road width': rw,
            'Front width': fw,
            'Post link': f'{website}{link}',
            'Image URL': f'{website}{image_url}',
            'Description': des,
            'Seller name': seller,
            'Phone': phone_number,
            'Estate type': estate_type,
            'Certification status': cs,
            'Rooms': None,
            'Kitchen': None,
            'Living room': None,
            'Seller type': seller_type,
            'Images': None,
            'Email': None,
            'Sizes': None
        }
        # print(property_data)
        if property_data not in data:
            data.append(property_data)

            with open(csv_file, 'a', newline='', encoding='utf-8-sig') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow(property_data)

print("End scraping")
