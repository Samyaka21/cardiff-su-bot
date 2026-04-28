import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_su():
    # The hubs we know work with simple scraping
    urls = [
        "https://www.cardiffstudents.com/whatson/",
        "https://www.cardiffstudents.com/about/contact/"
    ]
    
    all_data = []
    for url in urls:
        print(f"Scraping: {url}...")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get clean text
        content = soup.get_text(separator=' ', strip=True)
        all_data.append({
            "url": url,
            "content": content
        })

    # Save data
    os.makedirs('data', exist_ok=True)
    with open('data/raw_su_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4)
    print("Done!")

if __name__ == "__main__":
    scrape_su()