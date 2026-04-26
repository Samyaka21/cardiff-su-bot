import requests
from bs4 import BeautifulSoup
import os

def scrape_su_events():
    url = "https://www.cardiffstudents.com/whatson/"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all event cards (this selector depends on the SU site structure)
        events = soup.find_all('div', class_='event_item') 
        
        event_text = "FRESH EVENTS DATA:\n"
        for event in events:
            event_text += event.get_text(separator=' ', strip=True) + "\n---\n"
        
        # Save to a text file for the assistant to read
        os.makedirs("data", exist_ok=True)
        with open("data/latest_events.txt", "w", encoding="utf-8") as f:
            f.write(event_text)
        return True
    except Exception as e:
        print(f"Scrape failed: {e}")
        return False

if __name__ == "__main__":
    scrape_su_events()