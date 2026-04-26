import chromadb
from rank_bm25 import BM25Okapi
import json

def hybrid_query(user_query, n_results=3):
    # 1. Connect to your Day 4 Database
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name="cardiff_su_info")

    # 2. Get Vector Results (Semantic Search)
    results = collection.query(
        query_texts=[user_query],
        n_results=10 # Get a wider pool to re-rank
    )

    # Flatten the results for BM25
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]

    # 3. Apply BM25 Re-ranking (Keyword Search)
    tokenized_corpus = [doc.split(" ") for doc in documents]
    bm25 = BM25Okapi(tokenized_corpus)
    
    tokenized_query = user_query.split(" ")
    # Get scores for the documents based on exact keywords
    bm25_scores = bm25.get_scores(tokenized_query)
    
    # Sort documents by their keyword score
    combined_results = sorted(zip(bm25_scores, documents, metadatas), key=lambda x: x[0], reverse=True)

    return combined_results[:n_results]

if __name__ == "__main__":
    # Test your Day 5 logic!
    query = "What help is available for housing?"
    print(f"Testing Hybrid Search for: '{query}'\n")
    
    top_hits = hybrid_query(query)
    
    for i, (score, text, meta) in enumerate(top_hits):
        print(f"--- Result {i+1} (Source: {meta['source']}) ---")
        print(f"Snippet: {text[:200]}...\n")

    print("--- Day 5 Complete! Hybrid Retrieval logic is active. ---")