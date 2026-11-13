
from crewai import Agent, Task, Crew, Process

from agents import llm
from tools import discover_urls


# STEP 1: Create URL Discovery Agent
url_agent = Agent(
    role="Website URL Discovery Specialist",

    goal="Find relevant internal pages from a given website.",

    backstory="""
    You are an expert web research assistant.
    You identify useful internal website URLs
    and ignore irrelevant external links.
    """,

    tools=[discover_urls],
    llm=llm,
    verbose=True,
    allow_delegation=False
)


# STEP 2: Create a Task
discovery_task = Task(
    description="""
    Discover internal pages from this website:

    https://quotes.toscrape.com/

    Instructions:
    1. Use the discover_urls tool.
    2. Identify useful author profile pages.
    3. Return only valid URLs.
    4. Return one URL per line.
    5. Do not include explanations or markdown.
    6. Return a maximum of 5 URLs.
    """,

    expected_output="A list of valid internal author page URLs, one per line.",

    agent=url_agent
)


# STEP 3: Create Crew
discovery_crew = Crew(
    agents=[url_agent],
    tasks=[discovery_task],
    process=Process.sequential,
    verbose=True
)


# STEP 4: Execute
if __name__ == "__main__":

    print("\nStarting URL Discovery Agent...\n")

    result = discovery_crew.kickoff()

    print("\nDISCOVERED URLS:")
    print(result.raw)
