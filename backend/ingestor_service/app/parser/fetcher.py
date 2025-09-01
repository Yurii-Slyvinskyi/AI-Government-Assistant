import requests


def fetch_url(url: str) -> str:
    """
    Fetches raw HTML content from the given URL using requests.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text
