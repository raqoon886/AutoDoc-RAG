#!/usr/bin/env python3
"""
BLEU Score Evaluation Script.
Compares generated documentation against official Ground Truth using BLEU and other metrics.
"""
import argparse
import os
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize
import nltk
import json

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)


def load_document(filepath: str) -> str:
    """Load and return document content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def preprocess_text(text: str) -> list:
    """Tokenize and lowercase text for comparison."""
    return word_tokenize(text.lower())


def calculate_bleu(reference: str, candidate: str) -> dict:
    """Calculate BLEU scores (1-4 gram) between reference and candidate."""
    ref_tokens = preprocess_text(reference)
    cand_tokens = preprocess_text(candidate)
    
    # Use smoothing to handle zero counts
    smoothing = SmoothingFunction().method1
    
    # Individual n-gram scores
    bleu_1 = sentence_bleu([ref_tokens], cand_tokens, weights=(1, 0, 0, 0), smoothing_function=smoothing)
    bleu_2 = sentence_bleu([ref_tokens], cand_tokens, weights=(0.5, 0.5, 0, 0), smoothing_function=smoothing)
    bleu_3 = sentence_bleu([ref_tokens], cand_tokens, weights=(0.33, 0.33, 0.33, 0), smoothing_function=smoothing)
    bleu_4 = sentence_bleu([ref_tokens], cand_tokens, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=smoothing)
    
    return {
        "bleu_1": round(bleu_1 * 100, 2),
        "bleu_2": round(bleu_2 * 100, 2),
        "bleu_3": round(bleu_3 * 100, 2),
        "bleu_4": round(bleu_4 * 100, 2),
    }


def calculate_token_overlap(reference: str, candidate: str) -> dict:
    """Calculate token-level overlap metrics."""
    ref_tokens = set(preprocess_text(reference))
    cand_tokens = set(preprocess_text(candidate))
    
    intersection = ref_tokens & cand_tokens
    
    precision = len(intersection) / len(cand_tokens) if cand_tokens else 0
    recall = len(intersection) / len(ref_tokens) if ref_tokens else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "precision": round(precision * 100, 2),
        "recall": round(recall * 100, 2),
        "f1": round(f1 * 100, 2),
        "overlap_tokens": len(intersection),
    }


def main():
    parser = argparse.ArgumentParser(description="Compare generated docs with Ground Truth using BLEU score")
    parser.add_argument("ground_truth", help="Path to the Ground Truth (official) documentation")
    parser.add_argument("--no-rag", dest="no_rag", help="Path to No-RAG generated documentation")
    parser.add_argument("--rag", help="Path to RAG generated documentation")
    parser.add_argument("--output", "-o", default="output/bleu_results.json", help="Output file path for results")
    
    args = parser.parse_args()
    
    # Load Ground Truth
    print(f"📖 Loading Ground Truth: {args.ground_truth}")
    ground_truth = load_document(args.ground_truth)
    
    results = {}
    
    # Evaluate No-RAG
    if args.no_rag and os.path.exists(args.no_rag):
        print(f"📄 Loading No-RAG doc: {args.no_rag}")
        no_rag_doc = load_document(args.no_rag)
        
        bleu_scores = calculate_bleu(ground_truth, no_rag_doc)
        overlap = calculate_token_overlap(ground_truth, no_rag_doc)
        
        results["no_rag"] = {
            "bleu": bleu_scores,
            "overlap": overlap,
        }
    
    # Evaluate RAG
    if args.rag and os.path.exists(args.rag):
        print(f"📄 Loading RAG doc: {args.rag}")
        rag_doc = load_document(args.rag)
        
        bleu_scores = calculate_bleu(ground_truth, rag_doc)
        overlap = calculate_token_overlap(ground_truth, rag_doc)
        
        results["rag"] = {
            "bleu": bleu_scores,
            "overlap": overlap,
        }
    
    # Print Results
    print("\n" + "=" * 60)
    print("📊 BLEU SCORE COMPARISON")
    print("=" * 60)
    
    print(f"\n{'Metric':<20} {'No-RAG':>12} {'RAG':>12} {'Δ':>10}")
    print("-" * 54)
    
    metrics = ["bleu_1", "bleu_2", "bleu_3", "bleu_4"]
    for metric in metrics:
        no_rag_val = results.get("no_rag", {}).get("bleu", {}).get(metric, 0)
        rag_val = results.get("rag", {}).get("bleu", {}).get(metric, 0)
        delta = rag_val - no_rag_val
        delta_str = f"+{delta:.2f}" if delta >= 0 else f"{delta:.2f}"
        print(f"{metric.upper():<20} {no_rag_val:>11.2f}% {rag_val:>11.2f}% {delta_str:>10}")
    
    print("-" * 54)
    print("\n📊 TOKEN OVERLAP (vs Ground Truth)")
    print("-" * 54)
    
    overlap_metrics = ["precision", "recall", "f1"]
    for metric in overlap_metrics:
        no_rag_val = results.get("no_rag", {}).get("overlap", {}).get(metric, 0)
        rag_val = results.get("rag", {}).get("overlap", {}).get(metric, 0)
        delta = rag_val - no_rag_val
        delta_str = f"+{delta:.2f}" if delta >= 0 else f"{delta:.2f}"
        print(f"{metric.capitalize():<20} {no_rag_val:>11.2f}% {rag_val:>11.2f}% {delta_str:>10}")
    
    # Determine winner
    no_rag_bleu4 = results.get("no_rag", {}).get("bleu", {}).get("bleu_4", 0)
    rag_bleu4 = results.get("rag", {}).get("bleu", {}).get("bleu_4", 0)
    
    print("\n" + "=" * 60)
    if rag_bleu4 > no_rag_bleu4:
        print(f"🏆 Winner (BLEU-4): RAG ({rag_bleu4:.2f}% vs {no_rag_bleu4:.2f}%)")
    elif no_rag_bleu4 > rag_bleu4:
        print(f"🏆 Winner (BLEU-4): No-RAG ({no_rag_bleu4:.2f}% vs {rag_bleu4:.2f}%)")
    else:
        print(f"🏆 Winner (BLEU-4): TIE ({no_rag_bleu4:.2f}%)")
    print("=" * 60)
    
    # Save results
    output_path = args.output
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to: {output_path}")


if __name__ == "__main__":
    main()
