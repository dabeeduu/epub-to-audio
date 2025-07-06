import asyncio
import os

from epub_utils import extract_text_from_epub
from tts_utils import convert_with_semaphore
from progress import Progress


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
        task = convert_with_semaphore(
            semaphore, text, file_name, progress, voice="en-US-AvaMultilingualNeural"
        )
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

# Improvement :
# 1. create front end for GUI (maybe using react)
# 2. choose the voice
# 3. maybe even support pdf ?
# 4. add loading bar
