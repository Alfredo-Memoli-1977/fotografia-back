from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "photos.json"

def load_photos():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
    
def update_photos(photos):
    with open(DATA_PATH, "w", encoding="utf-8") as file:
        json.dump(photos, file, indent=4, ensure_ascii=False)