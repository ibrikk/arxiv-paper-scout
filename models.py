"""
Pydantic models for structured LLM outputs.
"""

from typing import List, Any
from pydantic import BaseModel, Field, field_validator


class PaperAnalysis(BaseModel):
    """Structured analysis of a single research paper."""

    title: str = Field(description="Paper title")
    authors: List[str] = Field(
        description="List of author full names, e.g. ['John Smith', 'Jane Doe']"
    )
    published: str = Field(description="Publication date")
    main_problem: str = Field(description="Main research problem addressed")
    method: str = Field(description="Core method or approach used")
    key_contribution: str = Field(description="Most important contribution")
    limitation: str = Field(description="One limitation or constraint")
    target_reader: str = Field(description="Who benefits most from this paper")
    relevance_score: int = Field(ge=1, le=10, description="Relevance to query (1-10)")

    @field_validator("relevance_score", mode="before")
    @classmethod
    def parse_relevance_score(cls, v: Any) -> int:
        """Handle LLM returning '7' instead of 7."""
        if isinstance(v, str):
            return int(v)
        return v


class PaperComparison(BaseModel):
    """Comparison and ranking of multiple papers."""

    best_for_beginner: str = Field(description="Best paper title for beginners")
    best_for_implementation: str = Field(description="Best paper for practical use")
    best_overall: str = Field(description="Best overall paper")
    reading_order: List[str] = Field(description="Recommended reading order (titles)")
    reasoning: str = Field(description="Brief explanation of the ranking")
