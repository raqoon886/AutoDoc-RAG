#!/usr/bin/env python3
"""
LLM-as-a-Judge Evaluation Framework.
Compares API documentation generated with No-RAG vs RAG modes.
"""
import argparse
import json
import os
import re
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Configuration
LLM_MODEL = "llama3.1:8b"
OUTPUT_DIR = "output"

EVALUATION_CRITERIA = [
    "completeness",
    "accuracy", 
    "clarity",
    "structure",
    "context_enrichment"
]


def read_file(path: str) -> str:
    """Read file content."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_scores(response: str) -> dict:
    """Parse LLM response to extract scores with multiple fallback strategies."""
    scores = {}
    
    # Strategy 1: Try to find and parse JSON block
    json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
    if json_match:
        try:
            parsed = json.loads(json_match.group(1))
            if all(c in parsed for c in EVALUATION_CRITERIA):
                return parsed
        except json.JSONDecodeError:
            pass
    
    # Strategy 2: Try to find raw JSON object (without code block)
    json_obj_match = re.search(r'\{[^{}]*"completeness"[^{}]*\}', response, re.DOTALL)
    if json_obj_match:
        try:
            parsed = json.loads(json_obj_match.group(0))
            if all(c in parsed for c in EVALUATION_CRITERIA):
                return parsed
        except json.JSONDecodeError:
            pass
    
    # Strategy 3: Parse scores from text patterns like "Completeness: 8" or "completeness: 8/10"
    for criterion in EVALUATION_CRITERIA:
        patterns = [
            rf'["\']?{criterion}["\']?\s*[:=]\s*(\d+)',  # completeness: 8 or "completeness": 8
            rf'{criterion}\s*[-–:]\s*(\d+)',  # completeness - 8
            rf'{criterion}[^0-9]*(\d+)\s*/\s*10',  # completeness 8/10
            rf'{criterion}[^0-9]*(\d+)\s*(?:points?|pts)?',  # completeness 8 points
        ]
        
        found = False
        for pattern in patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                if 1 <= score <= 10:  # Sanity check
                    scores[criterion] = score
                    found = True
                    break
        
        if not found:
            scores[criterion] = 0
    
    # Extract reasoning - try multiple patterns
    reasoning = ""
    reasoning_patterns = [
        r'"reasoning"\s*:\s*"([^"]+)"',  # JSON style
        r'reasoning[:\s]+(.*?)(?=\n\n|\Z)',  # Plain text
        r'(?:explanation|summary|notes?)[:\s]+(.*?)(?=\n\n|\Z)',  # Alternative labels
    ]
    
    for pattern in reasoning_patterns:
        match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
        if match:
            reasoning = match.group(1).strip()
            break
    
    if not reasoning:
        # Fallback: use last portion of response
        reasoning = response[-500:].strip()
    
    scores["reasoning"] = reasoning
    
    return scores


def evaluate_documentation(source_path: str, no_rag_path: str, rag_path: str):
    """
    Evaluate and compare documentation quality.
    """
    print(f"📖 Reading source: {source_path}")
    source_code = read_file(source_path)
    
    print(f"📄 Reading No-RAG doc: {no_rag_path}")
    no_rag_doc = read_file(no_rag_path)
    
    print(f"📄 Reading RAG doc: {rag_path}")
    rag_doc = read_file(rag_path)
    
    # Initialize LLM
    print(f"🤖 Initializing Judge LLM ({LLM_MODEL})...")
    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=0.1,
        keep_alive="5m"
    )
    
    # Judge Prompt Template
    template = """You are an expert technical documentation reviewer.
Your task is to evaluate the quality of API documentation generated from source code.

**Evaluation Criteria** (score each 1-10):
1. **Completeness & Detail**: Does the doc cover all classes, methods, parameters, and return values with *detailed descriptions*? (Simple summaries should receive low scores)
2. **Accuracy & Insight**: Are the descriptions factually correct and do they provide useful *insights* beyond just reading the code?
3. **Clarity**: Is the documentation easy to understand for developers?
4. **Structure & Professionalism**: Is the Markdown well-organized? Does it look like official library documentation?
5. **Context Enrichment (CRITICAL)**: Does the doc reference external standards, design patterns, or related architectural concepts? **If no external context or references are mentioned, the maximum score for this category is 2.**

---

**Original Source Code** (Ground Truth):
```
{source_code}
```

---

**Documentation to Evaluate**:
{doc_content}

---

Please provide your evaluation in the following JSON format:
```json
{{
  "completeness": <score 1-10>,
  "accuracy": <score 1-10>,
  "clarity": <score 1-10>,
  "structure": <score 1-10>,
  "context_enrichment": <score 1-10>,
  "reasoning": "<brief explanation of scores>"
}}
```
"""
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    
    results = {
        "source_file": os.path.basename(source_path),
        "no_rag": {},
        "rag": {},
        "winner": ""
    }
    
    # Evaluate No-RAG doc
    print("⏳ Evaluating No-RAG documentation...")
    try:
        no_rag_response = chain.invoke({
            "source_code": source_code,
            "doc_content": no_rag_doc
        })
        results["no_rag"] = parse_scores(no_rag_response)
        results["no_rag"]["total"] = sum(
            results["no_rag"].get(c, 0) for c in EVALUATION_CRITERIA
        )
    except Exception as e:
        print(f"❌ Error evaluating No-RAG: {e}")
        results["no_rag"] = {"error": str(e), "total": 0}
    
    # Evaluate RAG doc
    print("⏳ Evaluating RAG documentation...")
    try:
        rag_response = chain.invoke({
            "source_code": source_code,
            "doc_content": rag_doc
        })
        results["rag"] = parse_scores(rag_response)
        results["rag"]["total"] = sum(
            results["rag"].get(c, 0) for c in EVALUATION_CRITERIA
        )
    except Exception as e:
        print(f"❌ Error evaluating RAG: {e}")
        results["rag"] = {"error": str(e), "total": 0}
    
    # Determine winner
    no_rag_total = results["no_rag"].get("total", 0)
    rag_total = results["rag"].get("total", 0)
    
    if rag_total > no_rag_total:
        results["winner"] = "rag"
    elif no_rag_total > rag_total:
        results["winner"] = "no-rag"
    else:
        results["winner"] = "tie"
    
    # Save results
    output_path = os.path.join(OUTPUT_DIR, "evaluation_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Print Summary
    print("\n" + "=" * 50)
    print("📊 EVALUATION RESULTS")
    print("=" * 50)
    print(f"\n{'Criterion':<20} {'No-RAG':>10} {'RAG':>10}")
    print("-" * 42)
    for criterion in EVALUATION_CRITERIA:
        no_rag_score = results["no_rag"].get(criterion, "N/A")
        rag_score = results["rag"].get(criterion, "N/A")
        print(f"{criterion:<20} {str(no_rag_score):>10} {str(rag_score):>10}")
    print("-" * 42)
    print(f"{'TOTAL':<20} {no_rag_total:>10} {rag_total:>10}")
    print(f"\n🏆 Winner: {results['winner'].upper()}")
    print(f"\n💾 Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="LLM-as-a-Judge Evaluation for API Documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
    python src/evaluate_docs.py docs/sample_middleware.cpp
        """
    )
    parser.add_argument("source", help="Path to the original source code file")
    parser.add_argument(
        "--no-rag-dir",
        default="output/no-rag",
        help="Directory containing No-RAG generated docs (default: output/no-rag)"
    )
    parser.add_argument(
        "--rag-dir",
        default="output/rag",
        help="Directory containing RAG generated docs (default: output/rag)"
    )
    
    args = parser.parse_args()
    
    # Derive doc paths from source file name
    base_name = os.path.splitext(os.path.basename(args.source))[0]
    no_rag_path = os.path.join(args.no_rag_dir, f"{base_name}.md")
    rag_path = os.path.join(args.rag_dir, f"{base_name}.md")
    
    # Validate paths
    for path in [args.source, no_rag_path, rag_path]:
        if not os.path.exists(path):
            print(f"❌ File not found: {path}")
            return
    
    evaluate_documentation(args.source, no_rag_path, rag_path)


if __name__ == "__main__":
    main()
