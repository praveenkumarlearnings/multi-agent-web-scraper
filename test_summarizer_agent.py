
from crewai import Task, Crew, Process
import json

from agents import research_analyst
from tools import extract_content
from schemas import ResearchData


# STEP 1: Extract website content

url = "https://quotes.toscrape.com/author/Jane-Austen"

print("Extracting website content...")

content = extract_content.run(url)

if not content or content.startswith("Error"):
    raise ValueError("Content extraction failed.")


# STEP 2: Define summarization task

summarization_task = Task(
    description=f"""
    Analyze the following website content.

    Website URL:
    {url}

    Website Content:
    {content}

    Extract:
    1. Person's name
    2. Birth details
    3. Maximum 5 important facts
    4. Maximum 5 key topics
    5. A short summary of maximum 3 sentences

    Rules:
    - Use only the supplied website content.
    - Do not invent information.
    - Write the summary in your own words.
    - Do not copy the entire website content.
    - Return structured data matching the required schema.
    """,

    expected_output="Structured research data matching ResearchData.",

    output_pydantic=ResearchData,

    agent=research_analyst
)


# STEP 3: Create Crew

crew = Crew(
    agents=[research_analyst],
    tasks=[summarization_task],
    process=Process.sequential,
    verbose=True
)


# STEP 4: Execute Crew

print("\nStarting Research Summarizer Agent...")

result = crew.kickoff()


# STEP 5: Get validated structured output

print("\nValidating research output...")

research_data = result.pydantic

if research_data is None:
    raise ValueError("Structured output was not generated.")

# Convert Pydantic object to dictionary
research_dict = research_data.model_dump()

# Enforce maximum lengths as a safety check
research_dict["important_facts"] = research_dict["important_facts"][:5]
research_dict["key_topics"] = research_dict["key_topics"][:5]


# STEP 6: Display result

print("\nSTRUCTURED RESEARCH OUTPUT:")

print(json.dumps(
    research_dict,
    indent=4,
    ensure_ascii=False
))


# STEP 7: Save JSON file

with open(
    "research_dataset.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        [research_dict],
        file,
        indent=4,
        ensure_ascii=False
    )

print("\nResearch data saved successfully!")
print("File: research_dataset.json")
