from bs4 import BeautifulSoup


def extract_content(html: str) -> str:
    """
    Extracts meaningful content from HTML by removing nav, footer, scripts, etc.
    """
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.select("nav, footer, script, style"):
        tag.decompose()

    main = soup.find("main") or soup.body
    return main.get_text(separator="\n", strip=True)
