from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "users.json"
                 
def load_users():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
    

def save_users(users):
    with open(DATA_PATH, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)