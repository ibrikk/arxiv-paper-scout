"""
models.py - Pydantic models for structured LLM outputs

=== WHAT IS PYDANTIC? ===

Pydantic lets us define the EXACT shape of data we want.
Instead of the LLM returning messy text like:

    "The paper is about sensors, written by John, score 8/10"

We get clean Python objects:

    analysis.title      -> "Sensor Paper"
    analysis.authors    -> ["John Smith"]
    analysis.relevance_score -> 8

=== YOUR TASK ===

Fill in the PaperAnalysis and PaperComparison classes below.
Look at the Field() examples to understand the pattern.
"""

from typing import List, Any
from pydantic import BaseModel, Field, field_validator


class PaperAnalysis(BaseModel):
    """
    Structured analysis of a single research paper.

    Each field has:
    - A type (str, int, List[str])
    - A Field() with description (tells the LLM what we want)
    """

    # === EXAMPLE FIELD (already done) ===
    title: str = Field(description="Paper title")

    # === TODO: Add these fields ===

    # authors - should be a List[str]
    # description: "List of author full names, e.g. ['John Smith', 'Jane Doe']"
    # YOUR CODE HERE

    # published - should be a str
    # description: "Publication date"
    # YOUR CODE HERE

    # main_problem - should be a str
    # description: "2-3 sentences describing the main research problem"
    # YOUR CODE HERE

    # method - should be a str
    # description: "2-3 sentences explaining the core method or approach"
    # YOUR CODE HERE

    # key_contribution - should be a str
    # description: "2-3 sentences on the most important contribution"
    # YOUR CODE HERE

    # limitation - should be a str
    # description: "1-2 sentences on limitations or constraints"
    # YOUR CODE HERE

    # target_reader - should be a str
    # description: "1-2 sentences on who benefits most from this paper"
    # YOUR CODE HERE

    # relevance_score - should be an int
    # description: "Relevance to query (1-10)"
    # HINT: Add ge=1, le=10 to Field() to enforce range
    # YOUR CODE HERE

    @field_validator("relevance_score", mode="before")
    @classmethod
    def parse_relevance_score(cls, v: Any) -> int:
        """
        Sometimes the LLM returns "8" instead of 8.
        This validator converts string to int automatically.

        'mode="before"' means this runs BEFORE Pydantic validates the type.
        """
        if isinstance(v, str):
            return int(v)
        return v


class PaperComparison(BaseModel):
    """
    Comparison and ranking of multiple papers.

    === TODO: Add these fields ===

    - best_for_beginner: str - "Best paper title for beginners"
    - best_for_implementation: str - "Best paper for practical use"
    - best_overall: str - "Best overall paper"
    - reading_order: List[str] - "Recommended reading order (titles)"
    - reasoning: str - "3-5 sentences explaining the ranking"
    """

    # YOUR CODE HERE
    pass  # Remove this line when you add fields
