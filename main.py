from typing import Any
import ebooklib
import edge_tts
import asyncio
import time
from ebooklib import epub
from urllib.parse import urlparse
from bs4 import BeautifulSoup


async def convert_text_to_audio(text, output_file, voice="en-GB-RyanNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)


def extract_toc(toc: list[Any], title_map: dict):
    for item in toc:
        if isinstance(item, epub.Link):
            href_no_fragment = urlparse(item.href).path
            title_map[href_no_fragment] = item.title


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

        text = soup.get_text().strip()
        if not text:
            continue

        text = f"{title}\n\n{text}"

        chapters[title] = text

    return chapters


def main():
    epub_path = "carl3.epub"

    start_time = time.time()

    chapters = extract_text_from_epub(epub_path)

    for i, (title, body) in enumerate(chapters.items()):
        print(f"--- {title} ---")
        print(body[:500])
        print()
        if i == 10:
            break

    output_audio = "sample_audio.mp3"
    key_list = list(chapters.keys())
    asyncio.run(
        convert_text_to_audio(
            chapters[key_list[10]][:500], output_audio, "en-US-AvaNeural"
        )
    )
    # asyncio.run(convert_text_to_audio(chapters[10][:500], output_audio))
    print(f"Done! Audio saved to {output_audio}")
    #
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    #
    # print(f"Extracted {len(chapters)} chapters in {elapsed_time:.2f} seconds.\n")


if __name__ == "__main__":
    main()

# The idea :
# 1. get epub file
# 2. split based on chapter
# 3. put into a list
# 4. asynchronously parse it to mp3
#
# Improvement :
# 1. create front end for GUI (maybe using react)
# 2. choose the voice
# 3. maybe even support pdf ?
