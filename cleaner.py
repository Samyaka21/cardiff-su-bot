import json
import os
from bs4 import BeautifulSoup

def clean_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    
    # Get text and clean up whitespace
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return '\n'.join(chunk for chunk in chunks if chunk)

def process_cleaning():
    print("Starting Data Cleaning...")
    
    data_path = os.path.join('data', 'raw_su_data.json')
    
    if not os.path.exists(data_path):
        print("Error: raw_su_data.json not found!")
        return

    with open(data_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    cleaned_data = []
    for entry in raw_data:
        # Check if it's the new format (url) or old format (category)
        source_label = entry.get('url', entry.get('category', 'Unknown Source'))
        
        print(f"Cleaning content from: {source_label}...")
        
        text = clean_text(entry['content'])
        cleaned_data.append({
            "source": source_label,
            "content": text
        })

    # Save the cleaned data
    with open(os.path.join('data', 'cleaned_data.json'), 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=4)
    
    print(f"Successfully cleaned {len(cleaned_data)} pages!")

if __name__ == "__main__":
    process_cleaning()