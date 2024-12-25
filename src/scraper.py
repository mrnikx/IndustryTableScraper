import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from config import URL as url
# Sending a request to the webpage

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("Error fetching the webpage")
    exit()

# Parsing the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Finding the table
table = soup.find("table")
if not table:
    print("No table found on the webpage")
    exit()

# Extracting table headers
headers = []
for th in table.find_all("th"):
    headers.append(th.text.strip())

# Define headers manually if none are found
if not headers:
    headers = ["کارخانه", "مدیر","موبایل","تلفن", "آدرس", "شهر", "فعالیت"]

# Extracting table rows
rows = []
for tr in table.find_all("tr")[1:]:  # Skip the header row
    cells = tr.find_all("td")
    if len(cells) == len(headers):  # Ensure the number of cells matches the headers
        row = [cell.text.strip() for cell in cells]
        rows.append(row)

# Creating a DataFrame
if rows:
    df = pd.DataFrame(rows, columns=headers)
    
    # Removing unwanted columns ("Mobile" and "Phone" if they exist)
    columns_to_remove = ["موبایل", "تلفن"]
    for col in columns_to_remove:
        if col in df.columns:
            df.drop(columns=col, inplace=True)

    # Ensure the "data" directory exists
    os.makedirs("data", exist_ok=True)

    # Save the DataFrame to an Excel file in the "data" directory
    output_path = os.path.join("data", "extracted_data_filtered.xlsx")
    df.to_excel(output_path, index=False)
    print(f"Data successfully extracted and saved to {output_path}.")
else:
    print("No data found or the table is empty.")
