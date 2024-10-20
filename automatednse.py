import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up Chrome options and preferences
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent = your user agent")

download_dir = "downloads"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Set Chrome preferences for downloading files
prefs = {
    "download.default_directory": os.path.abspath(download_dir),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Wait for download completion by checking for .crdownload files
def wait_for_downloads(timeout=30):
    seconds = 0
    while seconds < timeout:
        if not any([filename.endswith(".crdownload") for filename in os.listdir(download_dir)]):
            return
        time.sleep(1)
        seconds += 1
    print("Timeout reached while waiting for downloads to complete.")

# Main part of the script
try:
    driver.get("https://www.nseindia.com/all-reports")  
    time.sleep(10)

    # Locate the reports div and download the files
    report_div = driver.find_element(By.XPATH, "//div[@id='cr_equity_daily_Current']")
    report_divs = report_div.find_elements(By.XPATH, ".//div[contains(@class, 'reportsDownload')]")

    for report in report_divs:
        data_link = report.get_attribute("data-link")
        print(f"Downloading from: {data_link}")
        
        driver.get(data_link)
        wait_for_downloads()  # Wait for the download to complete

finally:
    driver.quit()