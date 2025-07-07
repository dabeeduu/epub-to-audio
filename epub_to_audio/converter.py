import os
import asyncio
import uuid

from epub_utils import extract_text_from_epub
from tts_utils import convert_with_semaphore
from progress import Progress


async def convert_epub_to_mp3(epub_path, voice="en-US-AvaMultilingualNeural"):
    chapters = extract_text_from_epub(epub_path)

    temp_dir = f"temp_output_{uuid.uuid4()}"
    os.makedirs(temp_dir, exist_ok=True)

    semaphore = asyncio.Semaphore(5)
    progress = Progress(total=len(chapters))

    tasks = []
    mp3_files = []

    for i, (title, text) in enumerate(chapters.items()):
        safe_title = "".join(
            c for c in title if c.isalnum() or c in (" ", "_", "-")
        ).rstrip()
        file_name = os.path.join(temp_dir, f"{i}-{safe_title}.mp3")
        task = convert_with_semaphore(semaphore, text, file_name, progress, voice=voice)
        tasks.append(task)
        mp3_files.append(file_name)

    await asyncio.gather(*tasks)

    progress.done()

    return mp3_files, temp_dir
