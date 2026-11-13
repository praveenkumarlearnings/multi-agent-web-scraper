
from pydantic import BaseModel, Field


class ResearchData(BaseModel):
    person_name: str = Field(description="Name of the person")

    birth_details: str = Field(
        description="Birth date and location"
    )

    important_facts: list[str] = Field(
        description="Maximum 5 important facts"
    )

    key_topics: list[str] = Field(
        description="Maximum 5 key topics"
    )

    summary: str = Field(
        description="Short summary of maximum 3 sentences"
    )
