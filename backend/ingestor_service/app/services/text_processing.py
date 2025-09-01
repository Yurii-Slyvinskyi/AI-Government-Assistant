import re


def split_text(text: str, max_chunk_size: int = 1000) -> list[str]:
    """
    Splits the input text into chunks of up to max_chunk_size characters.

    First splits by paragraphs, then groups them into chunks. If a paragraph
    is too long, it is further split by sentences. Returns a list of text chunks.
    """
    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 <= max_chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            if len(para) > max_chunk_size:
                sentences = re.split(r"(?<=[.!?])\s+", para)
                temp = ""
                for s in sentences:
                    if len(temp) + len(s) + 1 <= max_chunk_size:
                        temp += s + " "
                    else:
                        chunks.append(temp.strip())
                        temp = s + " "
                if temp:
                    chunks.append(temp.strip())
                current_chunk = ""
            else:
                current_chunk = para + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
