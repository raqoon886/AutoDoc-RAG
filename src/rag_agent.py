#!/usr/bin/env python3
import sys
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Configuration (Must match ingest_data.py)
DB_DIR = "data/vector_db"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.1:8b"
COLLECTION_NAME = "autodoc_rag"

def main():
    print("Initializing AutoDoc-RAG Agent...")

    # 1. Initialize Embeddings (Must match ingestion)
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    # 2. Load Existing Vector DB
    try:
        vector_store = Chroma(
            persist_directory=DB_DIR,
            embedding_function=embeddings,
            collection_name=COLLECTION_NAME
        )
    except Exception as e:
        print(f"Error loading Vector DB: {e}")
        return

    # 3. Setup Retriever
    # search_kwargs={"k": 5}: Retrieve top 5 most relevant chunks
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    # 4. Initialize LLM (Llama 3.1 via Ollama)
    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=0.1, # Low temperature for factual accuracy
        keep_alive="5m"
    )

    # 5. Define Contextual Prompt
    template = """You are an expert middleware developer assistant. 
    Use the following pieces of retrieved context to answer the question. 
    If the context does not contain the answer, say "I don't have enough information in the provided documents to answer that." 
    Keep the answer technical, concise, and accurate.

    Context:
    {context}

    Question: {question}

    Answer:"""
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    # 6. Create QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    # 7. Interactive Loop
    print("\n✅ Agent Ready! Ask questions about your middleware. (Type 'exit' to quit)")
    print("-" * 50)
    
    while True:
        try:
            query = input("\n>> Question: ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break

            print("Thinking...")
            result = qa_chain.invoke({"query": query})
            
            answer = result["result"]
            sources = result["source_documents"]

            print(f"\n>> Answer:\n{answer}\n")
            print("[Referenced Sources]")
            for i, doc in enumerate(sources, 1):
                source_name = doc.metadata.get('source', 'Unknown')
                print(f"{i}. {source_name}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
