"""
Prompt templates for the LLM.
"""


def paper_analysis_prompt(
    topic: str, title: str, authors: str, published: str, content: str
) -> str:
    return f"""Analyze this arXiv paper for someone researching: {topic}

PAPER METADATA:
- Title: {title}
- Authors: {authors}
- Published: {published}

PAPER CONTENT (truncated):
{content}

Return a JSON object with EXACTLY these fields:
{{
    "title": "paper title",
    "authors": ["author 1", "author 2"],
    "published": "publication date",
    "main_problem": "2-3 sentences describing the main research problem",
    "method": "2-3 sentences explaining the core method or approach",
    "key_contribution": "2-3 sentences on the most important contribution",
    "limitation": "1-2 sentences on limitations or constraints",
    "target_reader": "1-2 sentences on who benefits most from this paper",
    "relevance_score": 7
}}

RULES:
- Use ONLY these field names, no extras
- relevance_score must be an integer from 1 to 10
- Write detailed responses (2-3 sentences per field, not just phrases)
- Be specific, cite details from the paper

Respond in JSON format."""


def comparison_prompt(topic: str, analyses_json: str) -> str:
    return f"""Compare these papers for someone researching: {topic}

PAPER ANALYSES:
{analyses_json}

Return a JSON object with EXACTLY these fields:
{{
    "best_for_beginner": "title of best paper for beginners",
    "best_for_implementation": "title of best paper for practical use",
    "best_overall": "title of best overall paper",
    "reading_order": ["first paper title", "second paper title"],
    "reasoning": "3-5 sentences explaining why this ranking makes sense, comparing the papers' strengths and weaknesses"
}}

RULES:
- Use ONLY these field names, no extras
- Write detailed reasoning (3-5 sentences, not just one)

Respond in JSON format."""
