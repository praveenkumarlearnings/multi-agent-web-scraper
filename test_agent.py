
from pathlib import Path

from crewai import Task, Crew, Process

from agents import research_analyst
from tools import extract_content


# ----------------------------------
# STEP 1: Extract website content
# ----------------------------------

url = "https://quotes.toscrape.com/author/Jane-Austen"

print("\nExtracting website content...")

content = extract_content.run(url)

if not content:
    raise ValueError("Failed to extract website content.")


# ----------------------------------
# STEP 2: Define the research task
# ----------------------------------

research_task = Task(
    description=f"""
    Analyze the following website content carefully.

    Website URL:
    {url}

    Website Content:
    {content}

    Your responsibilities:

    1. Identify the person's name.
    2. Extract important facts.
    3. Identify key topics.
    4. Write a short summary.

    Important:
    - Use only the information provided.
    - Do not invent facts.
    - Keep the report clear and structured.
    """,

    expected_output="""
    A structured research report containing:

    1. Person's Name
    2. Important Facts
    3. Key Topics
    4. Short Summary
    """,

    agent=research_analyst
)


# ----------------------------------
# STEP 3: Create the Crew
# ----------------------------------

crew = Crew(
    agents=[research_analyst],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True
)


# ----------------------------------
# STEP 4: Execute the Crew
# ----------------------------------

print("\nStarting Research Analyst Agent...")

result = crew.kickoff()


# ----------------------------------
# STEP 5: Display final report
# ----------------------------------

report = str(result)

print("\n" + "=" * 60)
print("FINAL RESEARCH REPORT")
print("=" * 60)

print(report)


# ----------------------------------
# STEP 6: Save report to a file
# ----------------------------------

output_file = Path("research_report.txt")

output_file.write_text(
    report,
    encoding="utf-8"
)

print("\n" + "=" * 60)
print("SUCCESS: Research report saved!")
print(f"File location: {output_file.resolve()}")
print("=" * 60)
