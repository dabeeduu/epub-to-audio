from typing import Any
import ebooklib
from ebooklib import epub
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def extract_toc(toc: list[Any], title_map: dict):
    for item in toc:
        if isinstance(item, epub.Link):
            href_no_fragment = urlparse(item.href).path
            title_map[href_no_fragment] = item.title


def clean_text(text):
    text = text.replace("\xa0", " ")
    text = text.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    return text


def extract_text_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    chapters = {}

    toc = book.toc
    title_map = {}

    extract_toc(toc, title_map)

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")

        header = soup.find(["h1", "h2"])
        if header:
            header.decompose()

        title = title_map.get(item.get_name(), item.get_name())

        for tag in soup.find_all(["p", "div"]):
            if tag.get_text(strip=True) == title:
                tag.decompose()

        paragraphs = []
        for p in soup.find_all("p"):
            text = p.get_text()
            if text.strip():
                paragraphs.append(text)

        if not paragraphs:
            continue

        paragraph_string = "\n\n".join(paragraphs)
        cleaned_paragraph = clean_text(paragraph_string)

        chapters[title] = f"{title}\n\n{cleaned_paragraph}"

    return chapters
