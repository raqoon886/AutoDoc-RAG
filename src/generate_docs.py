#!/usr/bin/env python3
"""
API Documentation Generator.
Supports two modes:
  - no-rag: Generate docs using only the source file content (LLM baseline).
  - rag: Generate docs using source file + relevant context from VectorDB.
"""
import argparse
import os
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Configuration
LLM_MODEL = "llama3.1:8b"
EMBEDDING_MODEL = "nomic-embed-text"
DB_DIR = "data/vector_db"
COLLECTION_NAME = "autodoc_rag"
OUTPUT_BASE_DIR = "output"


def get_rag_context(file_content: str, file_name: str, k: int = 5) -> str:
    """
    Retrieves relevant context from VectorDB based on the file content.
    """
    print(f"🔍 Searching VectorDB for related context (top {k})...")
    
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vector_store = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )
    
    # Use key portions of the file as query (first ~1000 chars for efficiency)
    query = f"API documentation context for: {file_name}\n{file_content[:2000]}"
    
    results = vector_store.similarity_search(query, k=k)
    
    if not results:
        print("   No relevant context found.")
        return ""
    
    context_parts = []
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get('source', 'Unknown')
        context_parts.append(f"[Source {i}: {source}]\n{doc.page_content}")
    
    context = "\n\n---\n\n".join(context_parts)
    print(f"   Found {len(results)} relevant documents.")
    return context


def generate_documentation(file_path: str, mode: str):
    """
    Generates API documentation for a single file.
    
    Args:
        file_path: Path to the source code file.
        mode: 'no-rag' or 'rag'.
    """
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    print(f"📖 Reading file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()

    file_name = os.path.basename(file_path)
    base_name = os.path.splitext(file_name)[0]

    # Initialize LLM
    print(f"🤖 Initializing LLM ({LLM_MODEL})...")
    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=0.1,
        keep_alive="5m"
    )

    # Prepare context based on mode
    rag_context = ""
    if mode == "rag":
        rag_context = get_rag_context(file_content, file_name, k=5)
    
    # Define Prompt based on mode
    if mode == "no-rag":
        # Minimal baseline prompt - pure LLM capability test
        template = """Analyze the following source code file: "{file_name}" and provide a summary of its contents.

Describe the main components and functions briefly.

**Source Code**:
```
{file_content}
```

**Summary**:
"""
    else:
        # RAG mode: Aggressive context utilization
        template = """You are an expert technical writer and software engineer.
Your task is to generate comprehensive API documentation for the following source code file: "{file_name}"

**IMPORTANT: You have access to valuable reference materials from a knowledge base.**
**You MUST actively incorporate this context into your documentation:**
- Use terminology and naming conventions from the reference materials
- Reference related architecture patterns or design decisions
- Cite relevant coding standards (e.g., C++ Core Guidelines) when applicable
- Even if the context seems only partially related, find ways to enrich the documentation with it

**Reference Context** (from VectorDB - USE THIS ACTIVELY):
{rag_context}

---

Please analyze the code below and produce a structured Markdown document.
The documentation should include:
1. **Module Overview**: Summarize what this file/module does. Connect it to architectural concepts from the reference context.
2. **Classes/Structs**: For each class or struct:
    - Description (enriched with insights from references)
    - Member Variables (if public/protected)
    - Methods (Signature + Description + Parameters + Return Value)
3. **Functions**: For global functions:
    - Signature
    - Description
    - Parameters
    - Return Value
4. **Usage Example**: A code snippet showing how to use the key components.
5. **Related References**: List any relevant standards, guidelines, or architecture documents from the context. This section is REQUIRED if any reference context was provided.

**Important**:
- Use GitHub Flavored Markdown.
- Ensure the tone is professional and clear.
- Prioritize incorporating reference context to create richer, more informative documentation.
- Do not make up information, but DO actively use the provided context.

---
**Source Code**:
```
{file_content}
```

**Markdown Output**:
"""

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()

    print(f"⏳ Generating documentation (Mode: {mode})... (This may take a while)")
    try:
        invoke_args = {
            "file_name": file_name,
            "file_content": file_content
        }
        if mode == "rag":
            invoke_args["rag_context"] = rag_context
        
        doc_content = chain.invoke(invoke_args)
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        return

    # Save Output to mode-specific folder
    output_dir = os.path.join(OUTPUT_BASE_DIR, mode)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{base_name}.md")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(doc_content)
    
    print(f"✅ Documentation saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate API Documentation from Source Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Without RAG (pure LLM):
    python src/generate_docs.py target.cpp --mode no-rag

    # With RAG (LLM + VectorDB context):
    python src/generate_docs.py target.cpp --mode rag
        """
    )
    parser.add_argument("file", help="Path to the source code file")
    parser.add_argument(
        "--mode",
        choices=["no-rag", "rag"],
        default="no-rag",
        help="Generation mode: 'no-rag' (LLM only) or 'rag' (LLM + VectorDB context). Default: no-rag"
    )
    
    args = parser.parse_args()
    
    generate_documentation(args.file, args.mode)


if __name__ == "__main__":
    main()
