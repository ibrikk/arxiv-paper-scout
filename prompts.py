"""
prompts.py - Prompt templates for the LLM

=== WHY SEPARATE PROMPTS? ===

1. Easy to iterate and improve
2. Clear what context the LLM sees
3. Can A/B test different prompts

=== PROMPT ENGINEERING TIPS ===

1. Be explicit about the output format
2. Give examples when possible
3. Use "RULES" or "INSTRUCTIONS" sections
4. For JSON: show the exact schema you want

=== YOUR TASK ===

Complete the two prompt functions below.
"""


def paper_analysis_prompt(
    topic: str, title: str, authors: str, published: str, content: str
) -> str:
    """
    Build a prompt to analyze a single paper.

    Args:
        topic: What the user is researching (e.g., "Android sensor spoofing")
        title: Paper title
        authors: Comma-separated author names
        published: Publication date
        content: Paper abstract/content (truncated)

    Returns:
        A prompt string that will make the LLM return structured JSON
    """

    # === TODO: Complete this prompt ===
    #
    # Your prompt should:
    # 1. Tell the LLM the user's research topic
    # 2. Provide the paper metadata (title, authors, published)
    # 3. Provide the paper content
    # 4. Show the EXACT JSON schema you want back
    # 5. Include "Respond in JSON format." (required by Groq)
    #
    # HINT: Use an f-string with {topic}, {title}, {authors}, {published}, {content}

    return f"""Analyze this arXiv paper for someone researching: {topic}

PAPER METADATA:
- Title: {title}
- Authors: {authors}
- Published: {published}

PAPER CONTENT (truncated):
{content}

# TODO: Add the JSON schema and rules here
# Look at the PaperAnalysis model for the fields you need

Respond in JSON format."""


def comparison_prompt(topic: str, analyses_json: str) -> str:
    """
    Build a prompt to compare multiple papers.

    Args:
        topic: What the user is researching
        analyses_json: JSON string of all paper analyses

    Returns:
        A prompt string that will make the LLM return comparison JSON
    """

    # === TODO: Complete this prompt ===

    return f"""Compare these papers for someone researching: {topic}

PAPER ANALYSES:
{analyses_json}

# TODO: Add the JSON schema and rules here
# Look at the PaperComparison model for the fields you need

Respond in JSON format."""
