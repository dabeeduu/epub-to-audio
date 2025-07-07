# epub-to-audio

[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/dabeeduu/epub-to-audio)

A fullstack application and CLI toolset to convert EPUB e-books into high-quality audio files — chapter by chapter — using Microsoft Edge's Text-to-Speech (TTS) service. Upload your EPUB, choose your preferred voice, and **download** ready-to-listen audio to enjoy anywhere.


##  Features

- **EPUB to Audio Conversion**: Seamlessly convert EPUB text content into spoken audio.
- **Chapter-by-Chapter Output**: Generates separate MP3 files for each chapter, preserving the book’s structure.
- **High-Quality Voices**: Uses `edge-tts` for natural, expressive voice synthesis.
- **Customizable Voice Selection**: Choose from a wide variety of voices and accents supported by Edge TTS.
- **Concurrent Processing**: Converts multiple chapters in parallel for faster results.
- **Modern Web UI**: Built with React (TypeScript + Tailwind CSS), featuring drag-and-drop EPUB upload and progress tracking.
- **Fast, Robust Backend**: Powered by FastAPI for high performance.
- **Downloadable Audio**: Easily download generated MP3 files chapter by chapter.


##  Installation

### Fullstack (Frontend + Backend)

> ⚠️ **Important:** The `make run-all` and `start.sh` scripts **do not install dependencies**. You must install them manually before running.

#### Install dependencies
Clone the repository:

```bash
git clone https://github.com/dabeeduu/epub-to-audio.git
cd epub_to_audio
make build-and-run-all
```



#### Start the application

From the project root:

```bash
make run-all
```

or

```bash
./start.sh 
```

This will:

- Start the FastAPI backend (default: `http://0.0.0.0:8000`)
- Start the React frontend (default: `http://localhost:3000`)

---

### CLI Tools Only

Clone the repository:

```bash
git clone https://github.com/dabeeduu/epub-to-audio.git
```

Navigate to the project directory:

```bash
cd epub-to-audio
```

Install the package (preferably in a virtual environment):

```bash
pip install .
```


## Usage (CLI)

The CLI creates an `output` directory in your current working directory, storing the generated MP3 files.

### Basic Conversion

```bash
epub-to-audio --file /path/to/your/ebook.epub
```

Uses the default voice: `en-US-AvaMultilingualNeural`.



### Use a Different Voice

```bash
epub-to-audio --file /path/to/your/ebook.epub --voice en-GB-RyanNeural
```

List all available voices:

```bash
edge-tts --list-voices
```

## Frontend

The web interface supports:

- Drag-and-drop EPUB upload
- **Downloadable audio files** after conversion
-  Progress bar during conversion (planned)
- Voice selection (planned)


## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).


## Acknowledgements

- [edge-tts](https://github.com/rany2/edge-tts) for the TTS engine.
- FastAPI and React communities for the modern, robust stack.


## Contributing

Contributions are welcome! Please open issues or submit pull requests.

