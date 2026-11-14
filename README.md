# Multi-Agent Web Scraper (CrewAI + Ollama)

Discovers pages on a website, extracts their content, summarizes each page with a local LLM, and exports a clean JSON/CSV dataset. 100% free: no paid APIs, and your data never leaves your machine.

## How it works

```
URL discovery + extraction (Python tools)
  -> Research Analyst agent (CrewAI + Llama 3.2 via Ollama)
  -> grounding check
  -> JSON / CSV dataset
```

- **tools.py**: `discover_urls` and `extract_content` (requests + BeautifulSoup)
- **agents.py**: CrewAI agents connected to a local Llama 3.2 model
- **schemas.py**: Pydantic model that forces structured output
- **main.py**: pipeline orchestration, retries and grounding check
- **data_organizer.py**: writes `research_dataset.json` and `research_dataset.csv`

## Hallucination check

Small local models can invent facts. Each record gets a `grounded` flag: the names and terms in the summary are checked against the scraped source text, and suspect records are flagged.

## Setup

```bash
ollama pull llama3.2
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Make sure Ollama is running (`ollama list`).

## Sample output

See `sample_dataset.json` and `sample_dataset.csv`.

## Limitations

- A 3B model can still produce subtle errors; the grounding check is a rough filter
- Static HTML pages only (no JavaScript rendering)
- Not built for large-scale crawling
- Check a site's robots.txt and terms before scraping
