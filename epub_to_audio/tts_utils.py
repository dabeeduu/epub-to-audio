import edge_tts
import time


async def convert_text_to_audio(text, output_file, voice="en-GB-RyanNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)


async def convert_with_semaphore(
    semaphore, text, output_file, progress, voice="en-GB-RyanNeural"
):
    async with semaphore:
        start = time.time()
        print(f"start converting: {output_file}")

        await convert_text_to_audio(text, output_file, voice)

        duration = time.time() - start
        progress.update()
        print(f"\nFinished: {output_file} in {duration:.2f} seconds")
