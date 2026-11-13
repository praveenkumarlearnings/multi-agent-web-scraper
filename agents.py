
from crewai import Agent, LLM

# Connect CrewAI to the local Ollama server
llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434",
    temperature=0.1,
)

# Research Analyst Agent
research_analyst = Agent(
    role="Research Analyst",
    goal="Analyze website content and identify important information.",
    backstory=(
        "You are an experienced research analyst. "
        "You read website content carefully and "
        "create accurate summaries."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


from tools import discover_urls

# URL Discovery Specialist Agent
url_discovery_agent = Agent(
    role="URL Discovery Specialist",

    goal=(
        "Discover relevant internal URLs from a given website "
        "and return a clean list of URLs."
    ),

    backstory=(
        "You are an expert web research specialist. "
        "You identify useful pages within a website "
        "and avoid irrelevant external links."
    ),

    tools=[discover_urls],
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


from tools import extract_content

# Content Extraction Specialist Agent
content_extraction_agent = Agent(
    role="Content Extraction Specialist",

    goal=(
        "Extract relevant website content from URLs "
        "and provide clean, readable information."
    ),

    backstory=(
        "You are an expert web content extraction specialist. "
        "You collect website titles and useful text while "
        "avoiding irrelevant information."
    ),

    tools=[extract_content],
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# Agent 4: Data Organizer
data_organizer_agent = Agent(
    role="Research Data Organizer",

    goal=(
        "Convert research summaries into clean, "
        "consistent and structured JSON records."
    ),

    backstory=(
        "You are an expert data organizer. "
        "You transform research information into "
        "structured datasets while preserving source URLs "
        "and avoiding duplicate records."
    ),

    llm=llm,
    verbose=True,
    allow_delegation=False,
)
