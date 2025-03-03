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

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

tables = soup.find_all("table")

def parse_table(table):
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

def upload_to_gsheets(df, sheet_name):
    worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=df.shape[0]+1, cols=df.shape[1])
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

for table_name, df in parsed_tables.items():
    if not df.empty:
        upload_to_gsheets(df, table_name)

print(f"All tables uploaded to Google Sheets: {SHEET_NAME}")