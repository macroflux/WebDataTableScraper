# Web Scraper to Google Sheets

This Python script scrapes tabular data from a website, processes it, and uploads it to **Google Sheets** for reporting in **Looker Studio**. It extracts **all tables** dynamically, appends a **timestamp** to the spreadsheet name, and runs on a **scheduled interval**. Useful for data driven, tabular display sites with refreshing data to run localized analysis reports off of, and where there are no data privacy issue considerations.

## Features
- Extracts **all tables** from a web page.
- Saves data to **Google Sheets**.
- Generates a **new spreadsheet** with a timestamp for each run.
- Can be scheduled on **Windows (Task Scheduler)** or **Linux (Cron Jobs)**.

---

## Installation

### 1. Clone the Repository
```sh
 git clone https://github.com/macroflux/web-scraper-google-sheets.git
 cd web-scraper
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```
Ensure the following dependencies are installed:
```sh
pip install requests beautifulsoup4 pandas gspread oauth2client schedule
```

### 3. Set Up Google Sheets API
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Google Sheets API** and **Google Drive API**.
3. Create a **Service Account** and download the JSON credentials file.
4. Share your Google Sheet with the Service Account email (found in the JSON file).

---

## Configuration

Modify the `config.ini` file to set up the **URL** and **Google Sheets credentials**.

### config.ini
```ini
[SETTINGS]
url = the full URL of the public website to scrape

[GOOGLE_SHEETS]
spreadsheet_share = your_email@example.com
spreadsheet_name = Main spreadsheet name - will append timestamp
credentials_file = credentials.json
```

- **url**: The website to scrape.
- **spreadsheet_share**: Your Google account email to access the sheet.
- **spreadsheet_name**: The base name for the generated spreadsheet.
- **credentials_file**: The Google API credentials JSON file.

---

## Running the Scraper
Run the scraper manually with:
```sh
python main.py
```
This will:
- Fetch the webpage.
- Extract all tables.
- Upload them to **Google Sheets**.

---

## Automating the Scraper
You can schedule the scraper to run **daily** or at specific intervals.

### Linux/macOS: Using Cron Jobs
1. Open the crontab editor:
   ```sh
   crontab -e
   ```
2. Add the following line to run the scraper **every day at 8 AM**:
   ```sh
   0 8 * * * /usr/bin/python3 /path/to/main.py
   ```
   **Replace** `/path/to/main.py` with your actual script path.
3. Save and exit. The job will now run automatically!

### Windows: Using Task Scheduler
1. Open **Task Scheduler** and click **Create Basic Task**.
2. Set the trigger to run **daily at 8 AM**.
3. Set the action to **Start a Program** and browse to `python.exe`.
4. Add the **full path** to `main.py` in the "Arguments" field:
   ```sh
   "C:\path\to\main.py"
   ```
5. Click **Finish** to save the task.

---

## Logs & Debugging
Check the logs if anything goes wrong:
```sh
tail -f scraper.log  # Linux/macOS
notepad scraper.log  # Windows
```

---

## Future Improvements
- **Error handling** for missing tables or failed requests.
- **Database storage** instead of Google Sheets.
- **Advanced scheduling** with Airflow.

---

## Contributing
Feel free to fork this repo, submit PRs, or report issues!

---

## License
MIT License. Free to use and modify!

