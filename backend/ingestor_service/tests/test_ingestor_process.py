import pytest
import requests
from unittest.mock import MagicMock, patch

from ..app.parser.fetcher import fetch_url
from ..app.parser.extractor import extract_content
from ..app.parser.normalizer import normalize_text
from ..app.services.text_processing import split_text
from ..app.services.send_chanks import send_chunks_to_embedding


def test_fetch_url_success():
    mock_response = MagicMock()
    mock_response.text = "<html><body>Main Content</body></html>"
    mock_response.raise_for_status = MagicMock()

    with patch.object(requests, "get", return_value=mock_response) as mock_get:
        html = fetch_url("http://example.com")
        assert "Main Content" in html
        mock_get.assert_called_once_with("http://example.com", headers={"User-Agent": "Mozilla/5.0"})


def test_extract_content_removes_nav_footer_script():
    html = """
        <html>
            <body>
                <nav>Navigation</nav>
                <main>Main Content</main>
                <footer>Footer</footer>
                <script>console.log("x")</script>
            </body>
        </html>
        """
    content = extract_content(html)
    assert content == "Main Content"


def test_normalize_text():
    text = "This  is  \n\n\n some text   "
    normalized = normalize_text(text)
    assert normalized == "This is some text"


def test_split_text_simple():
    text = "Para1\n\nPara2\n\nPara3"
    chunks = split_text(text, max_chunk_size=10)
    assert isinstance(chunks, list)
    assert all(isinstance(c, str) for c in chunks)


@pytest.mark.asyncio
async def test_send_chunks_to_embedding():
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "ok"}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", return_value=mock_response):
        result = await send_chunks_to_embedding("http://example.com", ["chunk1", "chunk2"])

        assert result == {"status": "ok"}
        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_called_once()
