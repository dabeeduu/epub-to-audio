# epub-to-audio
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/dabeeduu/epub-to-audio)

A command-line tool to convert EPUB e-books into audio files, chapter by chapter, using Microsoft Edge's Text-to-Speech (TTS) service. This script extracts the text from each chapter of an EPUB file and generates a corresponding MP3 audio file.

## Features

*   **EPUB to Audio Conversion**: Converts the text content of EPUB files into spoken audio.
*   **Chapter-by-Chapter**: Creates a separate MP3 file for each chapter, preserving the book's structure.
*   **High-Quality TTS**: Utilizes `edge-tts` for natural-sounding voice synthesis.
*   **Customizable Voice**: Allows you to select from a wide range of Edge TTS voices.
*   **Concurrent Processing**: Processes multiple chapters simultaneously to speed up conversion.
*   **Progress Tracking**: Displays a progress bar to monitor the conversion process.

## Installation

1.  Clone the repository to your local machine:
    ```bash
    git clone https://github.com/dabeeduu/epub-to-audio.git
    ```

2.  Navigate into the cloned directory:
    ```bash
    cd epub-to-audio
    ```

3.  Install the package and its dependencies. It is recommended to do this within a virtual environment.
    ```bash
    pip install .
    ```

## Usage

The script is run from the command line. It will create an `output` directory in your current working directory to store the generated MP3 files.

### Basic Conversion

To convert an EPUB file using the default voice (`en-US-AvaMultilingualNeural`), use the `--file` argument:

```bash
epub-to-audio --file /path/to/your/ebook.epub
```

### Specifying a Different Voice

You can specify a different voice using the `--voice` argument.

```bash
epub-to-audio --file /path/to/your/ebook.epub --voice en-GB-RyanNeural
```

To see a full list of available voices that you can use, run the following `edge-tts` command:

```bash
edge-tts --list-voices
```

## License

This project is licensed under the GNU General Public License v3.0. See the `LICENSE` file for details.