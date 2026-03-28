"""
main.py - arxiv-paper-scout main pipeline

=== WHAT WE'RE BUILDING ===

A tool that:
1. Takes a research topic from the user
2. Fetches relevant papers from arXiv
3. Analyzes each paper with an LLM
4. Compares the papers and recommends reading order
5. Saves everything to JSON

=== KEY CONCEPTS ===

1. LangChain LLM abstraction - swap providers easily
2. Structured outputs - get Python objects, not messy text
3. Retrieval (RAG) - fetch real documents to augment LLM
4. Chaining - compose multiple LLM calls

=== YOUR TASK ===

Fill in the TODO sections. Each one teaches a concept.
"""

import json
import os
from typing import List

from dotenv import load_dotenv
from langchain_community.retrievers import ArxivRetriever
from langchain_groq import ChatGroq

from models import PaperAnalysis, PaperComparison
from prompts import paper_analysis_prompt, comparison_prompt


# === CONFIGURATION ===
MAX_PAPERS = 3
MAX_CONTENT_CHARS = 6000
DEFAULT_TOPIC = "retrieval augmented generation"


def check_environment() -> bool:
    """
    Verify API key is configured.
    Always check this first - saves debugging time!
    """
    load_dotenv()

    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in .env file")
        print("   Get a free key at: https://console.groq.com/keys")
        return False

    print("✅ API key found")
    return True


def get_llm():
    """
    Create a LangChain LLM instance.

    === WHY LANGCHAIN? ===

    Without LangChain, switching from Groq to OpenAI means rewriting code.
    With LangChain, you just change this one function:

        # Groq (free, fast)
        return ChatGroq(model="llama-3.3-70b-versatile")

        # OpenAI (paid, very reliable)
        return ChatOpenAI(model="gpt-4o-mini")

        # Anthropic (paid, great for long docs)
        return ChatAnthropic(model="claude-3-sonnet")

    Same interface, different providers!
    """

    # === TODO: Create and return a ChatGroq instance ===
    #
    # Use these parameters:
    #   model="llama-3.3-70b-versatile"
    #   api_key=os.getenv("GROQ_API_KEY"),
    #   temperature=0  (makes output deterministic/reproducible)
    #
    # YOUR CODE HERE
    pass


def retrieve_papers(query: str) -> List:
    """
    Fetch papers from arXiv.

    === THIS IS THE "R" IN RAG ===

    RAG = Retrieval Augmented Generation

    Problem: LLMs have knowledge cutoffs and hallucinate
    Solution: Retrieve real documents and include them in the prompt

    LangChain has retrievers for:
    - arXiv (academic papers)
    - Wikipedia
    - Web search (Google, Bing)
    - Vector databases (Pinecone, Chroma)
    - SQL databases
    - And many more!
    """
    print(f"📚 Searching arXiv for: {query}")

    # === TODO: Create an ArxivRetriever and fetch papers ===
    #
    # 1. Create retriever:
    #    retriever = ArxivRetriever(
    #        load_max_docs=MAX_PAPERS,
    #        get_full_documents=False,  # Just abstracts, faster
    #    )
    #
    # 2. Fetch papers:
    #    docs = retriever.invoke(query)
    #
    # 3. Print count and return:
    #    print(f"   Found {len(docs)} papers")
    #    return docs
    #
    # YOUR CODE HERE
    pass


def analyze_paper(llm, topic: str, doc) -> PaperAnalysis:
    """
    Analyze a single paper with structured output.

    === KEY CONCEPT: with_structured_output() ===

    Normal LLM call:
        response = llm.invoke("Analyze this paper...")
        # Returns: "The paper discusses various aspects of..."
        # You have to parse this yourself! 😫

    Structured output:
        structured_llm = llm.with_structured_output(PaperAnalysis)
        analysis = structured_llm.invoke("Analyze this paper...")
        # Returns: PaperAnalysis object
        # analysis.title, analysis.authors, etc. 🎉

    The magic: LangChain tells the LLM to return JSON matching your Pydantic model!
    """
    metadata = doc.metadata or {}

    # Handle authors - arXiv returns various formats
    authors_raw = metadata.get("Authors", "Unknown")
    if isinstance(authors_raw, list):
        authors = ", ".join(authors_raw)
    else:
        authors = str(authors_raw)

    # === TODO: Build the prompt and get structured output ===
    #
    # 1. Build the prompt using paper_analysis_prompt():
    #    prompt = paper_analysis_prompt(
    #        topic=topic,
    #        title=metadata.get("Title", "Unknown"),
    #        authors=authors,
    #        published=metadata.get("Published", "Unknown"),
    #        content=doc.page_content[:MAX_CONTENT_CHARS],
    #    )
    #
    # 2. Create structured LLM (use json_mode for Groq compatibility):
    #    structured_llm = llm.with_structured_output(PaperAnalysis, method="json_mode")
    #
    # 3. Invoke and return:
    #    return structured_llm.invoke(prompt)
    #
    # YOUR CODE HERE
    pass


def compare_papers(llm, topic: str, analyses: List[PaperAnalysis]) -> PaperComparison:
    """
    Compare all papers and recommend reading order.

    === THIS IS "CHAINING" ===

    We take the OUTPUT of step 1 (individual analyses)
    and use it as INPUT to step 2 (comparison).

    Pipeline:
        Papers → [Analyze] → Analyses → [Compare] → Comparison

    Each step uses the same LLM with different prompts/schemas.
    """

    # Convert analyses to JSON string for the prompt
    analyses_json = json.dumps([a.model_dump() for a in analyses], indent=2)

    # === TODO: Build prompt and get structured output ===
    #
    # Same pattern as analyze_paper(), but use:
    # - comparison_prompt(topic, analyses_json)
    # - PaperComparison model
    #
    # YOUR CODE HERE
    pass


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
    """
    Main pipeline.

    === THE FULL FLOW ===

    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │ User Query  │ ──▶ │  Retrieve   │ ──▶ │  Analyze    │ ──▶ │  Compare    │
    │             │     │  (arXiv)    │     │  (LLM × 3)  │     │  (LLM × 1)  │
    └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
    """

    # Step 0: Check environment
    if not check_environment():
        return

    # Step 1: Get user input
    print("\n" + "=" * 50)
    print("   📚 arxiv-paper-scout")
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

    # Step 4: Analyze each paper
    print("\n--- ANALYSIS ---")
    analyses: List[PaperAnalysis] = []

    for i, doc in enumerate(docs, 1):
        title = (doc.metadata or {}).get("Title", f"Paper {i}")[:60]
        print(f"🔍 [{i}/{len(docs)}] Analyzing: {title}...")

        analysis = analyze_paper(llm, topic, doc)
        analyses.append(analysis)

        # Show preview
        print(f"   → {analysis.key_contribution[:80]}...")
        print(f"   → Relevance: {analysis.relevance_score}/10")

    # Step 5: Compare papers
    print("\n--- COMPARISON ---")
    print("🤔 Comparing papers and ranking...")

    comparison = compare_papers(llm, topic, analyses)

    # Display results
    print(f"\n📊 Results:")
    print(f"   Best for beginners: {comparison.best_for_beginner}")
    print(f"   Best for implementation: {comparison.best_for_implementation}")
    print(f"   Best overall: {comparison.best_overall}")

    print(f"\n📖 Recommended reading order:")
    for i, title in enumerate(comparison.reading_order, 1):
        print(f"   {i}. {title}")

    print(f"\n💡 Why: {comparison.reasoning}")

    # Step 6: Save results
    print()
    save_results(topic, analyses, comparison)


if __name__ == "__main__":
    main()
