
from crewai import Task, Crew, Process

from agents import url_discovery_agent

# Starting website
website_url = "https://quotes.toscrape.com/"

# Define the task
discovery_task = Task(
    description=f"""
    Discover internal URLs from this website:

    Website URL: {website_url}

    Instructions:
    1. Use the Discover Website URLs tool.
    2. Find URLs belonging to the same website.
    3. Return the discovered URLs.
    4. Do not invent URLs.
    """,

    expected_output="""
    A clean list of discovered internal website URLs.
    """,

    agent=url_discovery_agent
)

# Create Crew
crew = Crew(
    agents=[url_discovery_agent],
    tasks=[discovery_task],
    process=Process.sequential,
    verbose=True
)

# Execute
print("Starting URL Discovery Agent...")

result = crew.kickoff()

print("\nDISCOVERED WEBSITE URLS:")
print(result)
