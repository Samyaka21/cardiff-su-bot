import os
import sys
import glob

# --- 1. THE DYNAMIC PATH SHIELD ---
# Forces the script to use the venv libraries and ignore local conflicts
current_dir = os.getcwd()
venv_pattern = os.path.join(current_dir, 'venv', 'lib', 'python*', 'site-packages')
found_paths = glob.glob(venv_pattern)

# Isolate the environment from the current directory initially
if current_dir in sys.path:
    sys.path.remove(current_dir)

if found_paths:
    sys.path.insert(0, found_paths[0])
    print(f"✅ Shield Active: Pointing to {os.path.basename(os.path.dirname(found_paths[0]))}")

import toml
import chromadb

# Robust Import Strategy
try:
    from mistralai import Mistral
    print("✅ Mistral (Standard) Loaded.")
except ImportError:
    try:
        from mistralai.client import MistralClient as Mistral
        print("✅ Mistral (Legacy) Loaded.")
    except ImportError:
        print("❌ Critical Error: mistralai not found.")
        print("Please run: pip install mistralai")
        sys.exit(1)

# Re-add current directory for database and file access
sys.path.append(current_dir)

# --- 2. CONFIGURATION & DATABASE ---
DB_PATH = "./chroma_db"
COLLECTION_NAME = "cardiff_su"

def load_secrets():
    """Reads your MISTRAL_API_KEY from .streamlit/secrets.toml"""
    secrets_path = os.path.join(".streamlit", "secrets.toml")
    try:
        if not os.path.exists(secrets_path):
            print(f"⚠️ Warning: {secrets_path} not found.")
            return None
        secrets = toml.load(secrets_path)
        # Check for key in top-level or [default] section
        api_key = secrets.get("MISTRAL_API_KEY") or secrets.get("default", {}).get("MISTRAL_API_KEY")
        if not api_key:
            print("❌ MISTRAL_API_KEY missing in secrets.toml")
        return api_key
    except Exception as e:
        print(f"⚠️ Secret Loading Error: {e}")
        return None

def get_context(query):
    """Searches ChromaDB for relevant Cardiff SU information"""
    try:
        db_client = chromadb.PersistentClient(path=DB_PATH)
        collection = db_client.get_collection(name=COLLECTION_NAME)
        
        results = collection.query(
            query_texts=[query],
            n_results=7 
        )
        
        context_text = ""
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                doc = results['documents'][0][i]
                meta = results['metadatas'][0][i] if results['metadatas'] else {}
                url = meta.get('url', 'https://www.cardiffstudents.com/')
                context_text += f"\n[SOURCE: {url}]\n{doc}\n---\n"
            return context_text
        return "No relevant information found in the SU archives."
    except Exception as e:
        return f"Database Error: {str(e)}"

# --- 3. CHAT LOGIC ---
def ask_bot(user_query, mistral_client):
    context = get_context(user_query)
    
    system_instruction = (
        "You are the Cardiff Students' Union AI Assistant. "
        "Use the provided context to answer questions. "
        "Always provide the Source URL from the context in your answer."
    )
    
    try:
        # Compatibility check for newer vs older SDK methods
        if hasattr(mistral_client, 'chat') and hasattr(mistral_client.chat, 'complete'):
            response = mistral_client.chat.complete(
                model="mistral-small-latest",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{user_query}"},
                ],
            )
            return response.choices[0].message.content
        else:
            # Legacy Client method
            from mistralai.models.chat_completion import ChatMessage
            response = mistral_client.chat(
                model="mistral-small-latest",
                messages=[
                    ChatMessage(role="system", content=system_instruction),
                    ChatMessage(role="user", content=f"CONTEXT:\n{context}\n\nQUESTION:\n{user_query}")
                ],
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"Mistral API Error: {str(e)}"

# --- 4. MAIN LOOP ---
if __name__ == "__main__":
    api_key = load_secrets()
    
    if api_key:
        # Initialize the client based on which import worked
        client = Mistral(api_key=api_key)
        
        print("\n" + "═"*45)
        print("🤖 CARDIFF SU SOURCE-AWARE BOT ACTIVE")
        print("═"*45)
        print("Type 'exit' to end the chat.\n")

        while True:
            query = input("Ask a question: ").strip()
            if not query: continue
            if query.lower() in ['exit', 'quit']:
                print("Hwyl fawr! Goodbye!")
                break
            
            print("Searching archives...")
            answer = ask_bot(query, client)
            print(f"\nBot:\n{answer}\n")
            print("─" * 45)