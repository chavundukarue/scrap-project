from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_jobs():
    url = "https://vacancymail.co.zw/jobs/"

    # Set up headless Chrome browser
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(5)  # Let the page load fully

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    jobs = []
    job_cards = soup.select('div.job-listing-description')[:10]  # Updated selector

    for job in job_cards:
        title = job.select_one('h3.job-listing-title')
        title = title.get_text(strip=True) if title else 'N/A'

        company = job.select_one('h4.job-listing-company')
        company = company.get_text(strip=True) if company else 'N/A'

        description = job.select_one('p.job-listing-text')
        description = description.get_text(strip=True) if description else 'N/A'

        # Location and expiry date are not present in this snippet
        location = 'N/A'
        expiry = 'N/A'

        jobs.append({
            'Job Title': title,
            'Company': company,
            'Location': location,
            'Expiry Date': expiry,
            'Description': description
        })

    # Create DataFrame and save to CSV
    df = pd.DataFrame(jobs)
    df.to_csv('scraped_data.csv', index=False)

    print("Scraping complete. Data saved to scraped_data.csv")

if __name__ == "__main__":
    scrape_jobs()
