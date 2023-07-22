# Web Scraping Project - Vietnamese Real estate market
This Python web scraping project aims to extract property information from the website 'https://nhadat24h.net'. The web scraper retrieves data from different sub-menus, saves the scraped information into a CSV file, and downloads property images to a local directory. The project utilizes popular Python libraries such as requests, BeautifulSoup, and csv to achieve its functionality.

## Project Overview
This project contains a Python script (scraper.py) that performs web scraping to gather property data from 'https://nhadat24h.net'. The data includes information such as property titles, prices, locations, areas, timestamps, directions, number of floors, number of bedrooms, number of bathrooms, links to property pages, and image URLs.

The extracted data is stored in a CSV file (scraped_data.csv) for easy analysis and further processing. Additionally, the script downloads property images and saves them in the 'scraped_images' directory, allowing users to view the properties along with their information.

## Data Extracted
The web scraper extracts the following information for each property:

Category: The category of the property.
Title: The title or name of the property.
Price: The price of the property.
Location: The location of the property.
Area: The area size of the property.
Timestamp: The timestamp of when the property was listed or updated.
Direction: The facing direction of the property (e.g., North, South, etc.).
Floor: The number of floors in the property.
Bedroom: The number of bedrooms in the property.
Bathroom: The number of bathrooms in the property.
Link: The URL link to the property's page on the website.
Image URL: The URL of the property's image.

## Directory Structure
web-scraping-project/<br>
│   README.md<br>
│   main.py<br>
│   timestamp_utils.py<br>
│<br>
└───scraped_images/<br>
│       image_property1.jpg<br>
│       image_property2.jpg<br>
│       ...<br>
│<br>
└───scraped_data.csv<br>

## Used libraries
1. 'requests': This library is used to send HTTP requests to the website and retrieve the HTML content.
2. BeautifulSoup: This library is used for parsing the HTML content and extracting relevant data using various methods like find_all() and find().
3. csv: This library is used to read and write data to the CSV file.
4. os: This library is used to create a directory to store the downloaded images.
5. base64: This library is used to decode base64-encoded images (if applicable).
6. re: This library provides support for regular expressions, which are used to clean and sanitize the property titles.
7. datetime: This library is a built-in Python module that provides classes and functions for working with dates and times. It is used in the convert_relative_to_exact_timestamp function to handle and manipulate datetime objects.

## Contributing
Contributions to this project are welcome. If you find any issues or have suggestions for improvement, feel free to open a pull request or submit an issue.

Note: Please be aware that web scraping may be subject to legal and ethical considerations. Ensure that you have the necessary permissions before scraping data from any website. The authors of this project are not responsible for any misuse of the scraper.
