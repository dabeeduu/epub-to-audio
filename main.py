import edge_tts
import asyncio


async def convert_text_to_audio(text, output_file, voice="en-GB-RyanNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)


def main():
    sample_text = "It’s about 5 years that I’m using Neovim as my daily text editor especially when it comes to software development. On the other hand, I do lots of Python programming during the last 4 years and so to develop more comfortably, I had to configure my text editor as well. In this post, I’m going to explain my daily setup for Python software development."

    output_audio = "sample_audio.mp3"

    asyncio.run(convert_text_to_audio(sample_text, output_audio, "en-US-AvaNeural"))
    print(f"Done! Audio saved to {output_audio}")


if __name__ == "__main__":
    main()
