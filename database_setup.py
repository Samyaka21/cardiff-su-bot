import json
import chromadb
import os

def setup_database():
    # 1. Load ALL chunks
    with open('data/chunks.json', 'r') as f:
        chunks = json.load(f)

    print(f"🚀 Found {len(chunks)} total chunks. Preparing to store all of them...")

    # 2. Setup Chroma
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete the old collection if it exists to start fresh
    try:
        client.delete_collection("cardiff_su")
    except:
        pass
        
    collection = client.create_collection(name="cardiff_su")

    # 3. Add chunks in batches (to avoid memory crashes)
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        
        ids = [f"id_{j}" for j in range(i, i + len(batch))]
        documents = [c['content'] for c in batch]
        metadatas = [{"url": c['url']} for c in batch]

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        print(f"✅ Added chunks {i} to {i + len(batch)}")

    print(f"\n✨ FINAL SUCCESS! Stored {len(chunks)} chunks in ChromaDB.")

if __name__ == "__main__":
    setup_database()