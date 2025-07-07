from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import shutil
import os
import zipfile

from converter import convert_epub_to_mp3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/convert")
async def convert_epub(
    file: UploadFile = File(...), voice: str = Form("en-US-AvaMultilingualNeural")
):
    temp_epub = f"temp_{uuid.uuid4()}.epub"
    with open(temp_epub, "wb") as f:
        shutil.copyfileobj(file.file, f)

    mp3_files, temp_dir = await convert_epub_to_mp3(temp_epub, voice)

    zip_path = f"{temp_dir}.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for mp3_file in mp3_files:
            zipf.write(mp3_file, os.path.basename(mp3_file))

    os.remove(temp_epub)

    return FileResponse(
        zip_path, media_type="application/zip", filename="audio_files.zip"
    )
