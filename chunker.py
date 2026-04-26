import json
import os

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    # We use overlap so sentences aren't cut off awkwardly in the middle
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

def process_chunking():
    if not os.path.exists('data/cleaned_su_data.json'):
        print("Error: cleaned_su_data.json not found! Run Day 2 first.")
        return

    with open('data/cleaned_su_data.json', 'r', encoding='utf-8') as f:
        cleaned_data = json.load(f)

    chunked_library = []

    print("Starting Day 3: Chunking text into 500-character segments...")

    for entry in cleaned_data:
        text_content = entry['content']
        # Create the chunks
        text_chunks = chunk_text(text_content)
        
        for i, chunk in enumerate(text_chunks):
            # Save each chunk with its specific metadata for 'Source-Awareness'
            chunked_library.append({
                "chunk_id": f"{entry['category']}_{i}",
                "category": entry['category'],
                "source_url": entry['source_url'],
                "content": chunk,
                "date_chunked": "2026-04-18"
            })

    # Save the final chunked data
    with open('data/chunked_su_data.json', 'w', encoding='utf-8') as f:
        json.dump(chunked_library, f, indent=4)

    print(f"\n--- Day 3 Complete! ---")
    print(f"Created {len(chunked_library)} total chunks.")
    print("Saved to: data/chunked_su_data.json")

if __name__ == "__main__":
    process_chunking()