#!/usr/bin/env python3
import os
import glob
from typing import List

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Configuration
DOCS_DIR = "docs"
DB_DIR = "data/vector_db"
EMBEDDING_MODEL = "nomic-embed-text"
OLLAMA_BASE_URL = "http://localhost:11434"

def load_text_documents(source_dir: str) -> List[Document]:
    """Load Markdown and PDF documents."""
    documents = []
    
    # Load Markdown
    print(f"Loading Markdown files from {source_dir}...")
    md_loader = DirectoryLoader(
        source_dir,
        glob="**/*.md",
        loader_cls=TextLoader,
        recursive=True,
        show_progress=True
    )
    documents.extend(md_loader.load())

    # Load PDFs
    print(f"Loading PDF files from {source_dir}...")
    pdf_loader = DirectoryLoader(
        source_dir,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        recursive=True,
        show_progress=True
    )
    documents.extend(pdf_loader.load())
    
    return documents

def load_code_documents(source_dir: str) -> List[Document]:
    """Load C/C++ source code."""
    print(f"Loading C/C++ files from {source_dir}...")
    loader = GenericLoader.from_filesystem(
        source_dir,
        glob="**/*",
        suffixes=[".c", ".cpp", ".h", ".hpp", ".cc"],
        parser=LanguageParser(language=Language.CPP, parser_threshold=500),
        show_progress=True
    )
    return loader.load()

def main():
    # 1. Load Documents
    text_docs = load_text_documents(DOCS_DIR)
    code_docs = load_code_documents(DOCS_DIR)
    
    if not text_docs and not code_docs:
        print("No documents found in docs/ directory.")
        return

    print(f"Loaded {len(text_docs)} text documents and {len(code_docs)} code documents.")

    # 2. Split Documents
    all_chunks = []

    # Split Text
    if text_docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        text_chunks = text_splitter.split_documents(text_docs)
        print(f"Split text documents into {len(text_chunks)} chunks.")
        all_chunks.extend(text_chunks)

    # Split Code
    if code_docs:
        code_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.CPP,
            chunk_size=1000,
            chunk_overlap=200
        )
        code_chunks = code_splitter.split_documents(code_docs)
        print(f"Split code documents into {len(code_chunks)} chunks.")
        all_chunks.extend(code_chunks)

    if not all_chunks:
        print("No chunks to index.")
        return

    # 3. Initialize Embeddings
    print(f"Initializing embeddings with model '{EMBEDDING_MODEL}'...")
    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL
    )

    # 4. Save to ChromaDB
    print(f"Indexing {len(all_chunks)} chunks to ChromaDB at {DB_DIR}...")
    # Using persist_directory to create a persistent instance
    vector_store = Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        persist_directory=DB_DIR,
        collection_name="autodoc_rag"
    )
    
    print("Ingestion complete!")

if __name__ == "__main__":
    main()
