import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_with_selenium():
    urls = [
        "https://www.cardiffstudents.com/activities/societies/",
        "https://www.cardiffstudents.com/advice/"
    ]
    
    # Setup Chrome options (Running "headless" means no window pops up)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # This version tells Selenium to find the browser itself
    driver = webdriver.Chrome(options=chrome_options)
    
    all_data = []

    for url in urls:
        print(f"Deep Scanning: {url}...")
        driver.get(url)
        
        # Give the JavaScript 5 seconds to load the societies list
        time.sleep(5) 
        
        # Get the fully rendered HTML
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        text = soup.get_text(separator=' ')
        clean_text = ' '.join(text.split())

        all_data.append({
            "url": url,
            "content": clean_text
        })

    driver.quit()

    data_folder = "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        
    with open(os.path.join(data_folder, "raw_su_data.json"), "w", encoding='utf-8') as f:
        json.dump(all_data, f, indent=4)
    print("Done! Data is now truly complete.")

if __name__ == "__main__":
    scrape_with_selenium()