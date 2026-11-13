import re

from crewai import Task, Crew, Process

from agents import research_analyst
from tools import extract_content, discover_urls
from schemas import ResearchData
from data_organizer import save_dataset


# --------------------------------
# Configuration
# --------------------------------

START_URL = "https://quotes.toscrape.com/"
MAX_PAGES = 3
MAX_RETRIES = 2  # retries if the small local model returns bad structured output


# --------------------------------
# Helper: grounding check
# --------------------------------

def is_grounded(summary: str, source_text: str, threshold: float = 0.6) -> bool:
    """
    Rough hallucination check: what fraction of the summary's
    capitalized terms (names, places, events) appear in the source text?
    """
    terms = set(re.findall(r"\b[A-Z][a-zA-Z]{3,}\b", summary))

    if not terms:
        return True

    source_lower = source_text.lower()
    hits = sum(1 for term in terms if term.lower() in source_lower)

    return (hits / len(terms)) >= threshold


# --------------------------------
# Step 1: Discover website URLs
# --------------------------------

def discover_website_pages():

    print("\nSTEP 1: Discovering website URLs...")

    raw_urls = discover_urls.run(START_URL)

    if not raw_urls or raw_urls.startswith("Error"):
        raise ValueError(f"URL discovery failed: {raw_urls}")

    urls = [
        url.strip()
        for url in raw_urls.splitlines()
        if url.strip().startswith(("http://", "https://"))
    ]

    # For our Quotes to Scrape test website,
    # process only author pages.
    if "quotes.toscrape.com" in START_URL:
        urls = [url for url in urls if "/author/" in url]

    urls = list(dict.fromkeys(urls))[:MAX_PAGES]

    print(f"Discovered {len(urls)} pages to process.")

    return urls


# --------------------------------
# Step 2: Extract and summarize
# --------------------------------

def research_website(url):

    print(f"\nProcessing: {url}")

    # Extract website content
    content = extract_content.run(url)

    if not content or content.strip().startswith("Error"):
        print(f"Skipping page because extraction failed: {url}")
        return None

    # Create research task
    research_task = Task(
        description=f"""
        Analyze the following website content.

        Website URL: {url}

        Website Content:
        {content}

        Extract:
        1. Person's name
        2. Birth details
        3. Maximum 5 important facts
        4. Maximum 5 key topics
        5. A summary of maximum 3 sentences

        Rules:
        - Use only the supplied website content.
        - Do not invent information.
        - Write the summary in your own words.
        - Every sentence in the summary must be supported by the Website Content above.
        - Return structured data matching ResearchData.
        """,

        expected_output="Structured research data matching ResearchData.",

        output_pydantic=ResearchData,

        agent=research_analyst
    )

    # Retry loop: small local models sometimes return malformed output
    research_data = None

    for attempt in range(1, MAX_RETRIES + 1):

        crew = Crew(
            agents=[research_analyst],
            tasks=[research_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()

        research_data = result.pydantic

        if research_data is None and result.tasks_output:
            research_data = result.tasks_output[-1].pydantic

        if research_data is not None:
            break

        print(f"Attempt {attempt}/{MAX_RETRIES} failed for: {url}")

    if research_data is None:
        print(f"Could not generate structured output for: {url}")
        return None

    research_dict = research_data.model_dump()

    # Enforce maximum lengths
    research_dict["important_facts"] = research_dict["important_facts"][:5]
    research_dict["key_topics"] = research_dict["key_topics"][:5]

    # Keep the source URL
    research_dict["source_url"] = url

    # Grounding check
    research_dict["grounded"] = is_grounded(research_dict["summary"], content)

    if not research_dict["grounded"]:
        print(f"WARNING: summary may contain ungrounded claims for {url}")

    print(f"Research completed: {url}")

    return research_dict


# --------------------------------
# Step 3: Main execution
# --------------------------------

def main():

    print("=" * 50)
    print("MULTI-AGENT WEB SCRAPER")
    print("=" * 50)

    urls = discover_website_pages()

    if not urls:
        print("No suitable pages found.")
        return

    research_records = []

    print("\nSTEP 2: Extracting and analyzing pages...")

    for url in urls:

        try:
            record = research_website(url)

            if record:
                research_records.append(record)

        except Exception as error:
            print(f"Error processing {url}: {error}")
            continue

    # Save dataset
    if research_records:

        print("\nSTEP 3: Saving research dataset...")

        save_dataset(research_records)

        flagged = [r for r in research_records if not r.get("grounded", True)]

        print("\n" + "=" * 50)
        print("PROJECT COMPLETED SUCCESSFULLY!")
        print("=" * 50)

        print(f"Total pages processed: {len(research_records)}")
        print(f"Flagged as possibly ungrounded: {len(flagged)}")
        print("Generated files:")
        print("- research_dataset.json")
        print("- research_dataset.csv")

    else:
        print("\nNo research records were generated.")


if __name__ == "__main__":
    main()