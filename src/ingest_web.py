#!/usr/bin/env python3
"""
Web URL Data Ingestion Script for AutoDoc-RAG.
Recursively crawls a URL and ingests all linked pages into ChromaDB.

Usage:
    python src/ingest_web.py <URL> [--max-depth=2]
    
Example:
    python src/ingest_web.py https://docs.example.com/api --max-depth=3
"""
import argparse
import re
from typing import List
from bs4 import BeautifulSoup

from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Configuration (Must match ingest_data.py)
DB_DIR = "data/vector_db"
EMBEDDING_MODEL = "nomic-embed-text"
OLLAMA_BASE_URL = "http://localhost:11434"
COLLECTION_NAME = "autodoc_rag"


def bs4_extractor(html: str) -> str:
    """Extract text content from HTML using BeautifulSoup."""
    soup = BeautifulSoup(html, "lxml")
    
    # Remove script and style elements
    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.decompose()
    
    # Get text
    text = soup.get_text(separator="\n", strip=True)
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text


def load_web_documents(url: str, max_depth: int = 2) -> List[Document]:
    """
    Recursively load documents from a URL.
    
    Args:
        url: The root URL to start crawling from.
        max_depth: Maximum depth of links to follow (default: 2).
        
    Returns:
        List of Document objects containing the web page content.
    """
    print(f"🌐 Starting recursive crawl from: {url}")
    print(f"   Max depth: {max_depth}")
    
    loader = RecursiveUrlLoader(
        url=url,
        max_depth=max_depth,
        extractor=bs4_extractor,
        prevent_outside=True,  # Stay within the same domain
        timeout=30,
        check_response_status=True,
    )
    
    documents = loader.load()
    print(f"   Loaded {len(documents)} pages.")
    
    return documents


def main():
    parser = argparse.ArgumentParser(
        description="Ingest web documentation into VectorDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python src/ingest_web.py https://docs.example.com/api
    python src/ingest_web.py https://docs.example.com/api --max-depth=3
        """
    )
    parser.add_argument("url", help="Root URL to start crawling from")
    parser.add_argument(
        "--max-depth", 
        type=int, 
        default=2, 
        help="Maximum depth of links to follow (default: 2)"
    )
    
    args = parser.parse_args()
    
    # 1. Load Web Documents
    web_docs = load_web_documents(args.url, args.max_depth)
    
    if not web_docs:
        print("❌ No documents found from the URL.")
        return
    
    # 2. Split Documents
    print(f"✂️  Splitting {len(web_docs)} documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = text_splitter.split_documents(web_docs)
    print(f"   Split into {len(chunks)} chunks.")
    
    if not chunks:
        print("❌ No chunks to index.")
        return
    
    # 3. Initialize Embeddings
    print(f"🔢 Initializing embeddings with model '{EMBEDDING_MODEL}'...")
    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    
    # 4. Save to ChromaDB (Append to existing collection)
    print(f"💾 Indexing {len(chunks)} chunks to ChromaDB at {DB_DIR}...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR,
        collection_name=COLLECTION_NAME
    )
    
    print("✅ Web ingestion complete!")
    print(f"   Source: {args.url}")
    print(f"   Pages crawled: {len(web_docs)}")
    print(f"   Chunks indexed: {len(chunks)}")


if __name__ == "__main__":
    main()
