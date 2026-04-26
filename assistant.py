import os
import json
import chromadb
from sentence_transformers import SentenceTransformer

# 1. Setup ChromaDB and Embedding Model
# Using absolute paths ensures the cloud server finds the database every time
base_dir = os.path.dirname(__file__)
db_path = os.path.join(base_dir, "chroma_db")
client = chromadb.PersistentClient(path=db_path)
collection = client.get_or_create_collection(name="cardiff_su_data")
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_fresh_events():
    """Reads the manual JSON file for specific time-sensitive event details."""
    try:
        json_path = os.path.join(base_dir, "event_data.json")
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return []

def search_database(query, n_results=3):
    """Searches both the static database and the hourly scraped text file."""
    try:
        query_embedding = model.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        context = ""
        # Look for the file updated by the hourly GitHub Action
        latest_file = os.path.join(base_dir, "data", "latest_events.txt")
        if os.path.exists(latest_file):
            with open(latest_file, "r", encoding="utf-8") as f:
                # Add the freshly scraped web data to the context
                context += "\n--- LIVE HOURLY WEB UPDATES ---\n" + f.read()[:2000]

        # Add the long-term database knowledge
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            source = results['metadatas'][0][i].get('source', 'https://www.cardiffstudents.com/')
            context += f"\nSource: {source}\nContent: {doc}\n"
        return context
    except Exception as e:
        return f"Database search error: {e}"

def generate_source_aware_prompt(user_question):
    """Combines all data sources and enforces link-sharing rules."""
    
    # A. Search the Vector Database + Hourly Text File
    db_context = search_database(user_question)
    
    # B. Get JSON Events
    fresh_events_list = get_fresh_events()
    event_context = ""
    
    keywords = ["event", "on", "happening", "today", "tonight", "party", "yolo", "link", "ticket"]
    if any(word in user_question.lower() for word in keywords):
        event_context = "\n--- JSON UPCOMING EVENTS (USE THESE LINKS) ---\n"
        for event in fresh_events_list:
            event_context += (
                f"- EVENT: {event.get('title')}\n"
                f"  DATE: {event.get('date')}\n"
                f"  URL/LINK: {event.get('link', 'https://www.cardiffstudents.com/whatson/')}\n"
                f"  DETAILS: {event.get('description', '')}\n\n"
            )

    # C. System Instructions
    system_rules = """
    You are the official Cardiff Students' Union Assistant. 
    Your goal is to be helpful, accurate, and provide direct links.

    RULES:
    1. If a 'URL' or 'Link' is provided in the context below, you MUST include it in your answer as a clickable Markdown link like this: [Event Name](URL).
    2. Use the 'JSON UPCOMING EVENTS' section for specific event times and links.
    3. Use the 'LIVE HOURLY WEB UPDATES' for general news happening right now.
    4. If you don't know the answer, point them to https://www.cardiffstudents.com/about/contact/.
    5. Always end with 'Source Link:' and the most relevant URL found.
    """

    # Final Prompt
    full_prompt = f"""
    {system_rules}

    {event_context}

    {db_context}

    USER QUESTION: {user_question}
    
    ANSWER:
    """
    return full_prompt