import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.tools import tool
import requests
from tavily import TavilyClient

load_dotenv()

tavily_key = os.getenv("TAVILY_API_KEY")
tavily = TavilyClient(api_key=tavily_key) if tavily_key else None


@tool
def web_search(query: str) -> str:
    """Search the web for recent, reliable, and up-to-date information on a topic. Returns Titles, URLs, and Snippets."""
    if not tavily:
        return "Error: TAVILY_API_KEY is missing in your .env file."

    try:
        result = tavily.search(query=query, max_results=6)
        out = []
        for r in result.get("results", []):
            out.append(
                f"Title : {r.get('title', 'N/A')}\n"
                f"URL : {r.get('url', 'N/A')}\n"
                f"Snippet : {r.get('content', '')[:350]}\n"
            )
        return "\n----\n".join(out) if out else "No search results returned."
    except Exception as e:
        return f"Error executing web search: {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean, main text content from a specified web page URL for deeper analysis."""
    try:
        resp = requests.get(
            url,
            timeout=12,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
            },
        )

        if resp.status_code != 200:
            return f"HTTP Request failed with Status Code: {resp.status_code}"

        soup = BeautifulSoup(resp.text, "html.parser")

        # Strip navigation, script, and footer overhead
        for tag in soup(["script", "style", "nav", "footer", "header", "form", "aside", "svg"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        if not text or len(text) < 100:
            return "URL accessed, but could not extract significant text (site might require JS or block scrapers)."

        return text[:4000]

    except Exception as e:
        return f"Scraping error encountered for {url}: {str(e)}"


if __name__ == "__main__":
    from rich import print
    print("[bold green]Tools file executed directly - Test Mode[/bold green]")