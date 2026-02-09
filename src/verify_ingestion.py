#!/usr/bin/env python3
"""
Verification Script for AutoDoc-RAG VectorDB.
Checks if documents from specific sources have been successfully ingested.
"""
import argparse
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# Configuration (Must match ingest scripts)
DB_DIR = "data/vector_db"
EMBEDDING_MODEL = "nomic-embed-text"
COLLECTION_NAME = "autodoc_rag"

def main():
    print(f"🔍 Connecting to VectorDB at '{DB_DIR}'...")
    
    # 1. Initialize Embeddings & DB
    try:
        embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        vector_store = Chroma(
            persist_directory=DB_DIR,
            embedding_function=embeddings,
            collection_name=COLLECTION_NAME
        )
    except Exception as e:
        print(f"❌ Error loading Vector DB: {e}")
        return

    # 2. Get Collection Statistics
    # Note: Chroma's public API for getting all metadata is limited in LangChain wrapper.
    # We will use the underlying collection object.
    collection = vector_store._collection
    count = collection.count()
    print(f"📊 Total Chunk Count: {count}")

    if count == 0:
        print("⚠️  The database is empty.")
        return

    # 3. Verify Specific Sources by Querying Metadata
    # We'll sample metadata to look for source URLs
    print("\n🧐 Analyzing Sources (Sampling top 100 chunks)...")
    
    # Peek at the first 100 items to see sources
    data = collection.peek(limit=100)
    metadatas = data.get('metadatas', [])
    
    detected_sources = set()
    for meta in metadatas:
        if meta and 'source' in meta:
            detected_sources.add(meta['source'])
    
    print("\n✅ Detected Sources in Sample:")
    for src in sorted(detected_sources):
        print(f"  - {src}")

    # 4. Interactive Search Check
    print("\n🧪 Running Test Retrieval...")
    test_queries = [
        "What is arc42?",
        "How to use mermaid.js?",
        "D-Bus message bus system",
        "Protobuf style guide",
        "Systemd service unit"
    ]
    
    for query in test_queries:
        results = vector_store.similarity_search(query, k=1)
        if results:
            top_doc = results[0]
            source = top_doc.metadata.get('source', 'Unknown')
            print(f"  Query: '{query}' -> Found in: {source}")
        else:
            print(f"  Query: '{query}' -> ❌ No results found")

if __name__ == "__main__":
    main()
