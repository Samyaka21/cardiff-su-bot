import chromadb
import json
import os

def setup_database():
    # 1. Initialize the Chroma Client
    # This creates a folder called 'chroma_db' to store your data persistently
    client = chromadb.PersistentClient(path="./chroma_db")

    # 2. Create a Collection (think of this like a Table in a database)
    # We'll call it "cardiff_su_info"
    collection = client.get_or_create_collection(name="cardiff_su_info")

    # 3. Load your chunks from Day 3
    if not os.path.exists('data/chunked_su_data.json'):
        print("Error: chunked_su_data.json not found! Run Day 3 first.")
        return

    with open('data/chunked_su_data.json', 'r', encoding='utf-8') as f:
        chunks = json.load(f)

    print(f"Adding {len(chunks)} chunks to ChromaDB...")

    # 4. Prepare data for ChromaDB
    # Chroma needs lists of IDs, Documents (text), and Metadata
    documents = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        documents.append(chunk['content'])
        metadatas.append({
            "source": chunk['source_url'],
            "category": chunk['category']
        })
        ids.append(f"id_{i}")

    # 5. Upsert (Update or Insert) the data
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print("\n--- Day 4 Complete! ---")
    print(f"Successfully stored {collection.count()} items in the Vector Database.")
    print("Database folder created at: ./chroma_db")

if __name__ == "__main__":
    setup_database()