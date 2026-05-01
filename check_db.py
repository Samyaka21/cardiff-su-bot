import chromadb
import os

DB_PATH = "./chroma_db"

if os.path.exists(DB_PATH):
    client = chromadb.PersistentClient(path=DB_PATH)
    collections = client.list_collections()
    print("Your available collections are:")
    for col in collections:
        print(f" - {col.name}")
else:
    print(f"❌ Folder '{DB_PATH}' not found in: {os.getcwd()}")