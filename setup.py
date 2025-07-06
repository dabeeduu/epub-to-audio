from setuptools import setup, find_packages

setup(
    name="epub_to_audio",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "ebooklib",
        "beautifulsoup4",
        "edge-tts",
    ],
    entry_points={
        "console_scripts": [
            "epub-to-audio=epub_to_audio.cli:run",
        ],
    },
)
