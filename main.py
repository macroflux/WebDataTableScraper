"""
Web Scraper for extracting tabular data from a webpage
and uploading it to Google Sheets for reporting

Author: Chris Cole
Date: 2024-03-01
"""

import configparser
import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

config = configparser.ConfigParser()
config.read("config.ini")

URL = config["SETTINGS"]["url"]
SPREADSHEET_SHARE = config["GOOGLE_SHEETS"]["spreadsheet_share"]
SPREADSHEET_NAME = config["GOOGLE_SHEETS"]["spreadsheet_name"]
CREDENTIALS_FILE = config["GOOGLE_SHEETS"]["credentials_file"]

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
SHEET_NAME = f"{SPREADSHEET_NAME}_{timestamp}"

response = requests.get(URL, timeout=60)
soup = BeautifulSoup(response.content, "html.parser")

tables = soup.find_all("table")

def parse_table(table):
    """
    Extracts data from an HTML table and converts it into a Pandas DataFrame.

    Args:
        table (bs4.element.Tag): The HTML table element to be parsed.

    Returns:
        pandas.DataFrame: A DataFrame containing the extracted table data.
    """
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cells:
            rows.append(cells)
    return pd.DataFrame(rows, columns=headers) if headers else pd.DataFrame(rows)

parsed_tables = {f"Table_{i+1}": parse_table(table) for i, table in enumerate(tables)}

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

spreadsheet = client.create(SHEET_NAME)
spreadsheet.share(SPREADSHEET_SHARE, perm_type="user", role="writer")

def upload_to_gsheets(dataframe, sheet_name):
    """
    Uploads a Pandas DataFrame to a Google Sheets worksheet.

    Args:
        dataframe (pandas.DataFrame): The DataFrame containing data to be uploaded.
        sheet_name (str): The name of the worksheet where the data will be stored.

    Returns:
        None
    """
    worksheet = spreadsheet.add_worksheet(
        title=sheet_name,
        rows=dataframe.shape[0] + 1,
        cols=dataframe.shape[1]
    )
    worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())

for table_name, df in parsed_tables.items():
    if not df.empty:
        upload_to_gsheets(df, table_name)

print(f"All tables uploaded to Google Sheets: {SHEET_NAME}")
