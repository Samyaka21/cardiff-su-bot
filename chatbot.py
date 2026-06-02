import os
import sys
import glob
import toml
import chromadb

# --- 1. THE DYNAMIC PATH SHIELD (For Mac venv support) ---
current_dir = os.getcwd()
venv_pattern = os.path.join(current_dir, 'venv', 'lib', 'python*', 'site-packages')
found_paths = glob.glob(venv_pattern)

if found_paths:
    sys.path.insert(0, found_paths[0])

# --- 2. ROBUST MISTRAL IMPORT (Pinned to 0.4.2 compatibility) ---
try:
    from mistralai.client import MistralClient as Mistral
except ImportError:
    # Fallback for different versioning structures
    try:
        from mistralai import Mistral
    except ImportError:
        raise ImportError("Mistral library not found. Please run: pip install mistralai==0.4.2")

# --- 3. CONFIGURATION ---
DB_PATH = "./chroma_db"
COLLECTION_NAME = "cardiff_su"

def load_secrets():
    """Reads your MISTRAL_API_KEY from .streamlit/secrets.toml"""
    secrets_path = os.path.join(".streamlit", "secrets.toml")
    try:
        if not os.path.exists(secrets_path):
            return os.environ.get("MISTRAL_API_KEY")
        secrets = toml.load(secrets_path)
        # Check both standard and default table locations
        return secrets.get("MISTRAL_API_KEY") or secrets.get("default", {}).get("MISTRAL_API_KEY")
    except Exception:
        return None

def ask_chatbot(user_query):
    """
    Function called by app.py. 
    Retrieves context from ChromaDB and generates a response with links.
    """
    api_key = load_secrets()
    if not api_key:
        return "⚠️ Error: Mistral API Key not found in .streamlit/secrets.toml."

    try:
        # Connect to your local vector database
        db_client = chromadb.PersistentClient(path=DB_PATH)
        collection = db_client.get_collection(name=COLLECTION_NAME)
        
        # Search for the top 3 most relevant chunks
        results = collection.query(query_texts=[user_query], n_results=3)
        
        context_text = ""
        unique_sources = []
        
        # Extract text content and metadata (links)
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                doc_content = results['documents'][0][i]
                context_text += f"\n{doc_content}\n---\n"
                
                # Grab the URL from the metadata if it exists
                if results['metadatas'] and results['metadatas'][0][i]:
                    meta = results['metadatas'][0][i]
                    url = meta.get("url") or meta.get("source") or "https://www.cardiffstudents.com/"
                    if url not in unique_sources:
                        unique_sources.append(url)
        else:
            context_text = "No specific Cardiff SU information found for this query."

        # Initialize the Mistral Client
        client = Mistral(api_key=api_key)
        system_instruction = (
            "You are the Cardiff Students' Union AI Assistant. "
            "Use the provided context to answer questions accurately. "
            "If the answer is not in the context, politely state you don't know. "
            "DO NOT append any source links, URLs, or phrases like '(Source Unknown)' "
            "at the end of your answer, as the system will handle formatting links automatically."
        )
        

        # Generate the AI response
        response = client.chat(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"CONTEXT:\n{context_text}\n\nQUESTION:\n{user_query}"},
            ],
        )
        
        ai_answer = response.choices[0].message.content

        # Append source links at the bottom in Markdown format
        if unique_sources:
            links_formatted = "\n\n**Sources & Further Reading:**\n"
            for link in unique_sources:
                links_formatted += f"- [{link}]({link})\n"
            final_output = ai_answer + links_formatted
            return final_output.replace("(Source Unknown)", "")
        
        # If there are no sources, still clean the AI answer just in case
        return ai_answer.replace("(Source Unknown)", "")
           
        

    except Exception as e:
        return f"❌ An error occurred: {str(e)}"