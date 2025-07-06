import argparse
import asyncio
import os

from epub_utils import extract_text_from_epub
from tts_utils import convert_with_semaphore
from progress import Progress


async def main(file, voice):
    chapters = extract_text_from_epub(file)

    os.makedirs("output", exist_ok=True)

    semaphore = asyncio.Semaphore(5)
    progress = Progress(total=len(chapters))

    tasks = []
    for i, (title, text) in enumerate(chapters.items()):
        safe_title = "".join(
            c for c in title if c.isalnum() or c in (" ", "_", "-")
        ).rstrip()
        file_name = os.path.join("output", f"{i}-{safe_title}.mp3")
        task = convert_with_semaphore(semaphore, text, file_name, progress, voice=voice)
        tasks.append(task)

    await asyncio.gather(*tasks)


def run():
    parser = argparse.ArgumentParser(
        description="Convert EPUB chapters to audio files."
    )
    parser.add_argument("--file", type=str, required=True, help="Path to the EPUB file")
    parser.add_argument(
        "--voice",
        type=str,
        default="en-US-AvaMultilingualNeural",
        help="Edge TTS voice (default: en-US-AvaMultilingualNeural)",
    )

    args = parser.parse_args()

    asyncio.run(main(args.file, args.voice))


if __name__ == "__main__":
    run()
