from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up headless browser
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get("https://vacancymail.co.zw/jobs/")
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
job_cards = soup.find_all("a", class_="job-listing", limit=10)

job_data = []
for job in job_cards:
    title = job.text.strip()
    link = "https://vacancymail.co.zw" + job["href"]
    job_data.append({
        "Job Title": title,
        "Job Link": link
    })

driver.quit()

df = pd.DataFrame(job_data)
df.to_csv("scraped_data.csv", index=False)
print("✅ Scraping complete. Jobs found:", len(job_data))