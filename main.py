import ebooklib
import edge_tts
import asyncio
import time
from ebooklib import epub
from bs4 import BeautifulSoup


async def convert_text_to_audio(text, output_file, voice="en-GB-RyanNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)


def extract_text_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")
        text = soup.get_text()
        if text.strip():
            chapters.append(text)
    return chapters


def main():
    epub_path = "carl3.epub"

    start_time = time.time()

    chapters = extract_text_from_epub(epub_path)

    for i, chapter_text in enumerate(chapters, 1):
        print(f"--- Chapter {i} ---")
        print(chapter_text[:500])
        print()
        # only get the 11 chapter
        if i == 11:
            break

    output_audio = "sample_audio.mp3"

    # asyncio.run(convert_text_to_audio(chapters[10], output_audio, "en-US-AvaNeural"))
    asyncio.run(convert_text_to_audio(chapters[10][:500], output_audio))
    print(f"Done! Audio saved to {output_audio}")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Extracted {len(chapters)} chapters in {elapsed_time:.2f} seconds.\n")


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
