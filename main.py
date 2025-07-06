from typing import Any
import ebooklib
import edge_tts
import asyncio
import time
import os
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

        paragraphs = []
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if text:
                paragraphs.append(text)

        if not paragraphs:
            continue

        chapters[title] = f"{title}\n\n{'\n\n'.join(paragraphs)}"

    return chapters


async def convert_text_to_audio(text, output_file, voice="en-GB-RyanNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)


class Progress:
    def __init__(self, total):
        self.total = total
        self.done = 0


async def convert_with_semaphore(
    semaphore, text, output_file, progress, voice="en-GB-RyanNeural"
):
    async with semaphore:
        start = time.time()
        print(f"start converting: {output_file}")

        await convert_text_to_audio(text, output_file, voice)

        duration = time.time() - start
        progress.done += 1
        print(f"Finished: {output_file} in {duration:.2f} seconds")


async def main():
    epub_path = "midnight.epub"
    chapters = extract_text_from_epub(epub_path)

    os.makedirs("output", exist_ok=True)

    semaphore = asyncio.Semaphore(5)
    progress = Progress(total=len(chapters))

    tasks = []
    for i, (title, text) in enumerate(chapters.items()):
        safe_title = "".join(
            c for c in title if c.isalnum() or c in (" ", "_", "-")
        ).rstrip()
        file_name = os.path.join("output", f"{i}-{safe_title}.mp3")
        task = convert_with_semaphore(semaphore, text, file_name, progress)
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
