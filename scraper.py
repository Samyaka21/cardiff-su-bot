import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_cardiff_su():
    # Define the "Hubs" that contain the most important info
    urls_to_scrape = [
        "https://www.cardiffstudents.com/",
        "https://www.cardiffstudents.com/activities/societies/",
        "https://www.cardiffstudents.com/advice/",
        "https://www.cardiffstudents.com/activities/sports/",
        "https://www.cardiffstudents.com/about-us/contact/"
    ]
    
    all_data = []
    
    for url in urls_to_scrape:
        print(f"Scraping: {url}...")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove junk like scripts and styles
                for script in soup(["script", "style"]):
                    script.extract()

                text = soup.get_text(separator=' ')
                # Clean up the white space
                clean_text = ' '.join(text.split())
                
                all_data.append({
                    "url": url,
                    "content": clean_text
                })
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    # Save everything to the JSON file
    data_folder = os.path.join(os.path.dirname(__file__), "data")
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        
    with open(os.path.join(data_folder, "raw_su_data.json"), "w", encoding='utf-8') as f:
        json.dump(all_data, f, indent=4)
    
    print(f"Done! Scraped {len(all_data)} pages.")

if __name__ == "__main__":
    scrape_cardiff_su()