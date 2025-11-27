# tools/arxiv_tools.py
import feedparser
from typing import List, Dict


def fetch_latest_papers(category: str, max_results: int = 20) -> List[Dict]:
    """
    Fetch latest papers for a given arXiv category using RSS feed.
    Example category: 'cs.AI', 'cs.CV', etc.
    """
    url = f"https://export.arxiv.org/rss/{category}"
    feed = feedparser.parse(url)

    papers = []
    for entry in feed.entries[:max_results]:
        papers.append(
            {
                "id": entry.id,
                "title": entry.title,
                "summary": entry.summary,
                "link": entry.link,
                "authors": [a.name for a in entry.authors],
                "published": entry.published,
                "category": category,
            }
        )
    return papers

