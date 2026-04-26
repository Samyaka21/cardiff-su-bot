import json
import os
import re

def clean_text(text):
    # 1. Remove excessive whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # 2. Common "Junk" phrases found in SU headers/footers
    # We can add more to this list as we find them
    junk_phrases = [
        "Login", "Register", "Toggle navigation", "Search", 
        "Cardiff University Students' Union", "All rights reserved",
        "Follow us on social media", "Cookies Policy", "Privacy Policy"
    ]
    
    for phrase in junk_phrases:
        text = text.replace(phrase, "")
    
    return text.strip()

def process_cleaning():
    # Ensure directories exist
    if not os.path.exists('data/raw_su_data.json'):
        print("Error: raw_su_data.json not found! Did you run Day 1?")
        return

    # Load the raw data from Day 1
    with open('data/raw_su_data.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    cleaned_data = []

    print("Starting Day 2: Cleaning HTML content...")

    for entry in raw_data:
        print(f"Cleaning {entry['category']}...")
        
        raw_text = entry['content']
        # Clean the content 
        clean_content = clean_text(raw_text)
        
        # Keep the metadata! This is crucial for being 'Source-Aware' 
        cleaned_data.append({
            "category": entry['category'],
            "source_url": entry['source_url'],
            "content": clean_content,
            "date_cleaned": "2026-04-17"
        })

    # Save to a new file for Day 3
    with open('data/cleaned_su_data.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=4)

    print("\n--- Day 2 Complete! ---")
    print("Cleaned data saved to: data/cleaned_su_data.json")

if __name__ == "__main__":
    process_cleaning()