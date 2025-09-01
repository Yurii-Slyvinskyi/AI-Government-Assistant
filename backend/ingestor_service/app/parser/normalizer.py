import re


def normalize_text(text: str) -> str:
    """
    Remove spaces, new lines. Clean, continuous text.
    """
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()
