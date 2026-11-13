
from crewai import Task, Crew, Process

from agents import content_extraction_agent

url = "https://quotes.toscrape.com/author/Jane-Austen"

extraction_task = Task(
    description=f"""
    Extract website content from this URL:

    {url}

    Instructions:
    1. Use the Extract Website Content tool.
    2. Extract the page title.
    3. Extract the readable website content.
    4. Do not invent information.
    """,

    expected_output="""
    The page title and readable website content.
    """,

    agent=content_extraction_agent
)

crew = Crew(
    agents=[content_extraction_agent],
    tasks=[extraction_task],
    process=Process.sequential,
    verbose=True
)

print("Starting Content Extraction Agent...")

result = crew.kickoff()

print("\nEXTRACTED WEBSITE CONTENT:")
print(result)
