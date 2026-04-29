import json
import os

def semantic_chunker():
    # Load the cleaned data
    if not os.path.exists('data/cleaned_data.json'):
        print("Error: data/cleaned_data.json not found!")
        return

    with open('data/cleaned_data.json', 'r') as f:
        data = json.load(f)

    chunks = []
    # Using a slightly larger chunk for better context
    chunk_size = 1200 
    overlap = 200

    print(f"Processing {len(data)} pages into semantic chunks...")

    for item in data:
        text = item.get('content', '')
        # SAFETY CHECK: If 'url' is missing, use 'Unknown' instead of crashing
        url = item.get('url', 'https://www.cardiffstudents.com/ (Source Unknown)')
        
        if not text:
            continue

        # Split into parts by sentence to avoid cutting in the middle of a word
        parts = text.split('. ')
        
        current_chunk = ""
        for part in parts:
            if len(current_chunk) + len(part) < chunk_size:
                current_chunk += part + ". "
            else:
                chunks.append({
                    "content": current_chunk.strip(), 
                    "url": url
                })
                # Maintain overlap for context continuity
                current_chunk = current_chunk[-overlap:] + part + ". "
        
        # Add the final piece
        if current_chunk:
            chunks.append({
                "content": current_chunk.strip(), 
                "url": url
            })

    # Save the chunks
    with open('data/chunks.json', 'w') as f:
        json.dump(chunks, f, indent=4)
    
    print(f"✅ Success! Created {len(chunks)} high-quality semantic chunks.")

if __name__ == "__main__":
    semantic_chunker()