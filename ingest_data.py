import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

# Main page URL with yearly links
url = "https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/"

# Send a request to fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all <a> tags (links) on the page
links = soup.find_all('a', href=True)

# Filter out the links that point to the yearly data pages (e.g., '2024', '2025' pages)
year_links = []
for link in links:
    href = link['href']
    # Check if the link contains 'year' (you may adjust this as needed)
    if 'https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/ae-attendances-and-emergency-admissions-' in href:
        year_links.append(href)

# Print out the found year links
print(year_links)
print(len(year_links))


# Step 3: Iterate over each CSV link to visit the new page and scrape monthly CSVs
all_csvs = []
for csv_link in year_links:
    print(f"Visiting: {csv_link}")
    response = requests.get(csv_link)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 4: Find all CSV links on the new page
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Look for .csv links that do not contain 'weekly'
        if href.endswith('.csv') and 'weekly' not in href.lower():
            # If the link is relative, prepend the base URL
            if not href.startswith('http'):
                href = 'https://www.england.nhs.uk' + href
            all_csvs.append(href)

# Debugging: Print all CSV links found on subsequent pages
print("All CSV Links Found:", all_csvs)

# Step 5: Download each CSV file from the collected list
# Create a folder to store CSVs
os.makedirs("csv_downloads", exist_ok=True)

for csv_link in all_csvs:
    print(f"Downloading: {csv_link}")
    csv_response = requests.get(csv_link)
    csv_filename = os.path.join("csv_downloads", csv_link.split('/')[-1])  # Save to csv_downloads folder
    with open(csv_filename, 'wb') as file:
        file.write(csv_response.content)
    print(f"Downloaded: {csv_filename}")