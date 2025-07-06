from typing import Any
import ebooklib
import edge_tts
import asyncio
import time
from ebooklib import epub
from urllib.parse import urlparse
from bs4 import BeautifulSoup


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


async def convert_text_to_audio(text, output_file, voice="en-GB-RyanNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)


async def convert_with_semaphore(
    semaphore, text, output_file, voice="en-GB-RyanNeural"
):
    async with semaphore:
        start = time.time()
        print(f"start converting: {output_file}")

        await convert_text_to_audio(text, output_file, voice)

        duration = time.time() - start
        print(f"Finished: {output_file} in {duration:.2f} seconds")


async def main():
    epub_path = "carl3.epub"
    chapters = extract_text_from_epub(epub_path)

    semaphore = asyncio.Semaphore(5)

    tasks = []
    for i, (title, text) in enumerate(chapters.items()):
        file_name = f"{i}-{title}.mp3"
        task = convert_with_semaphore(semaphore, text, file_name)
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

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
# 4. add loading bar
