import requests

HN_API_URL = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage={n}"


def fetch_top_stories(n=8):
    """Busca as top n notícias da página principal do Hacker News via Algolia API."""
    try:
        response = requests.get(HN_API_URL.format(n=n), timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"[fetcher] Erro ao buscar notícias do HN: {e}")
        raise

    stories = []
    for hit in data.get("hits", []):
        stories.append({
            "title": hit.get("title", "Sem título"),
            "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            "score": hit.get("points", 0),
        })

    return stories
