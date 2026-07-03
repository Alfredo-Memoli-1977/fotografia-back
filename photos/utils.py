from pathlib import Path
import json
import shutil
from fastapi import UploadFile

# Rutas
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "photos.json"
DATA_PREVIEW=BASE_DIR/"images"/"preview"
DATA_RAW=BASE_DIR/"images"/"raw"

def load_photos():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
    
def update_photos(photos):
    with open(DATA_PATH, "w", encoding="utf-8") as file:
        json.dump(photos, file, indent=4, ensure_ascii=False)

def upload_new_photos(photos:list[UploadFile]):
    for photo in photos:
        if photo.filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            with open(DATA_PREVIEW/photo.filename, "wb") as file:
                shutil.copyfileobj(photo.file, file)
        elif photo.filename.lower().endswith((".raw", ".cr3", ".cr2", ".nef", ".arw", ".dng")):
            with open(DATA_RAW/photo.filename, "wb") as file:
                shutil.copyfileobj(photo.file, file)