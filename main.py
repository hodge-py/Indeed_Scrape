from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up headless Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

service = Service('path/to/chromedriver')  # 🔧 Replace with actual path
driver = webdriver.Chrome(service=service, options=options)

# Go to the Indeed search page
url = 'https://www.indeed.com/jobs?q=software+developer&l=remote'
driver.get(url)
wait = WebDriverWait(driver, 10)

# Wait for listings to load
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'job_seen_beacon')))
jobs = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')

descriptions = []

for job in jobs:
    try:
        # Click the job to reveal its description pane
        job.click()
        time.sleep(2)  # Give time for sidebar to load

        # Locate the job description container (you may need to adjust this class)
        desc_element = wait.until(EC.presence_of_element_located(
            (By.ID, 'jobDescriptionText')))
        descriptions.append(desc_element.text)
    except Exception as e:
        print(f"Could not extract one job: {e}")
        continue

# Save to a txt file
with open('job_descriptions.txt', 'w', encoding='utf-8') as f:
    for i, desc in enumerate(descriptions, 1):
        f.write(f"--- Job {i} ---\n{desc}\n\n")

driver.quit()
