
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
from crewai.tools import tool


@tool("Discover Website URLs")
def discover_urls(base_url: str) -> str:
    """
    Discover unique links belonging to the same domain.
    """

    try:
        response = requests.get(
            base_url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        base_domain = urlparse(base_url).hostname
        discovered_urls = set()

        for link in soup.find_all("a", href=True):
            href = link["href"]

            absolute_url = urljoin(base_url, href)
            absolute_url, _ = urldefrag(absolute_url)

            parsed_url = urlparse(absolute_url)

            if (
                parsed_url.scheme in ("http", "https")
                and parsed_url.hostname == base_domain
                and absolute_url != base_url
            ):
                discovered_urls.add(absolute_url)

        if not discovered_urls:
            return "No matching URLs found."

        return "\n".join(sorted(discovered_urls)[:20])

    except requests.RequestException as error:
        return f"Error discovering URLs: {error}"

@tool("Extract Website Content")
def extract_content(url: str) -> str:
    """
    Extract the title and readable text content
    from a given website URL.
    """

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract page title
        title = (
            soup.title.get_text(strip=True)
            if soup.title
            else "No title found"
        )

        # Remove unnecessary HTML elements
        for element in soup(
            ["script", "style", "nav", "footer", "header"]
        ):
            element.decompose()

        # Extract readable text
        content = soup.get_text(
            separator=" ",
            strip=True
        )

        # Limit content size
        content = content[:5000]

        return f"""
        Page Title: {title}

        Website Content:
        {content}
        """

    except requests.RequestException as error:
        return f"Error extracting content: {error}"
