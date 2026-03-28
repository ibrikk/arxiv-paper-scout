"""
arxiv-paper-scout: AI-powered research paper analyzer

WHAT THIS DEMO TEACHES:
1. LangChain LLM abstraction - swap providers easily
2. Structured outputs - get Python objects, not messy text
3. Retrieval (RAG) - fetch real documents to augment LLM knowledge
4. Chaining - compose multiple LLM calls into a pipeline

FLOW:
    User query → Retrieve papers → Analyze each → Compare all → Save results
"""

import json
import os
from typing import List

from dotenv import load_dotenv
from langchain_community.retrievers import ArxivRetriever
from langchain_groq import ChatGroq

from models import PaperAnalysis, PaperComparison
from prompts import paper_analysis_prompt, comparison_prompt

# --- CONFIGURATION ---
MAX_PAPERS = 3
MAX_CONTENT_CHARS = 5000
DEFAULT_TOPIC = "retrieval augmented generation"


def check_environment():
    """Verify API key is configured."""
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in .env file")
        print("   Get a free key at: https://console.groq.com/keys")
        return False
    return True


def get_llm():
    """
    Create LangChain LLM instance.

    WHY LANGCHAIN?
    - Change one line to switch from Groq → OpenAI → Anthropic
    - Same interface regardless of provider
    - Built-in structured output support
    """
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,  # Deterministic outputs for reproducibility
    )


def retrieve_papers(query: str, max_papers: int = MAX_PAPERS) -> List:
    """Fetch papers from arXiv."""
    print(f"📚 Searching arXiv for: {query} (requesting {max_papers})")

    retriever = ArxivRetriever(
        load_max_docs=max_papers,
        get_full_documents=False,
    )

    docs = retriever.invoke(query)
    print(f"   Found {len(docs)} papers (requested {max_papers})")
    return docs


def analyze_paper(llm, topic: str, doc) -> PaperAnalysis:
    """Analyze a single paper with structured output."""
    metadata = doc.metadata or {}

    authors_raw = metadata.get("Authors", "Unknown")
    if isinstance(authors_raw, list):
        authors = ", ".join(authors_raw)
    else:
        authors = str(authors_raw)

    prompt = paper_analysis_prompt(
        topic=topic,
        title=metadata.get("Title", "Unknown"),
        authors=authors,
        published=metadata.get("Published", "Unknown"),
        content=doc.page_content[:MAX_CONTENT_CHARS],
    )

    # Use json_mode so Pydantic handles validation (not Groq's tool schema)
    structured_llm = llm.with_structured_output(PaperAnalysis, method="json_mode")
    return structured_llm.invoke(prompt)


def compare_papers(llm, topic: str, analyses: List[PaperAnalysis]) -> PaperComparison:
    """Compare all papers and recommend reading order."""
    analyses_json = json.dumps([a.model_dump() for a in analyses], indent=2)
    prompt = comparison_prompt(topic, analyses_json)

    # Use json_mode so Pydantic handles validation (not Groq's tool schema)
    structured_llm = llm.with_structured_output(PaperComparison, method="json_mode")
    return structured_llm.invoke(prompt)


def save_results(
    topic: str, analyses: List[PaperAnalysis], comparison: PaperComparison
):
    """Save all results to JSON file."""
    output = {
        "topic": topic,
        "papers": [a.model_dump() for a in analyses],
        "comparison": comparison.model_dump(),
    }

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("💾 Saved results to output.json")


def main():
    """Main pipeline."""

    # Step 0: Check setup
    if not check_environment():
        return

    # Step 1: Get user query
    print("\n" + "=" * 50)
    print("   arxiv-paper-scout")
    print("=" * 50)

    topic = input(f"\nEnter research topic [{DEFAULT_TOPIC}]: ").strip()
    topic = topic or DEFAULT_TOPIC

    # Step 2: Retrieve papers (the "R" in RAG)
    print("\n--- RETRIEVAL ---")
    docs = retrieve_papers(topic)

    if not docs:
        print("❌ No papers found. Try a different topic.")
        return

    # Step 3: Initialize LLM
    llm = get_llm()

    # Step 4: Analyze each paper (structured output)
    print("\n--- ANALYSIS ---")
    analyses: List[PaperAnalysis] = []

    for i, doc in enumerate(docs, 1):
        title = (doc.metadata or {}).get("Title", f"Paper {i}")[:60]
        print(f"🔍 [{i}/{len(docs)}] Analyzing: {title}...")

        analysis = analyze_paper(llm, topic, doc)
        analyses.append(analysis)

        # Show a preview
        print(f"   → {analysis.key_contribution[:80]}...")
        print(f"   → Relevance: {analysis.relevance_score}/10")

    # Step 5: Compare papers (chaining)
    print("\n--- COMPARISON ---")
    print("🤔 Comparing papers and ranking...")
    comparison = compare_papers(llm, topic, analyses)

    print(f"\n📊 Results:")
    print(f"   Best for beginners: {comparison.best_for_beginner}")
    print(f"   Best for implementation: {comparison.best_for_implementation}")
    print(f"   Best overall: {comparison.best_overall}")
    print(f"\n📖 Recommended reading order:")
    for i, title in enumerate(comparison.reading_order, 1):
        print(f"   {i}. {title}")

    # Step 6: Save results
    print()
    save_results(topic, analyses, comparison)


if __name__ == "__main__":
    main()
