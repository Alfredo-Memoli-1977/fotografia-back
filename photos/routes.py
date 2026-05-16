from fastapi import APIRouter, Query
from typing import Literal
import json
from pathlib import Path

router = APIRouter()

DATA_PATH = Path("data/photos.json")

def load_photos():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

@router.get("/photos")
def get_photos(
    category: str | None = Query(default=None),
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    orientation: Literal["landscape", "portrait"] | None = Query(default=None),
    q: str | None = Query(default=None),
):
    result = load_photos()

    if category is not None:
        result = [p for p in result if p["category"] == category]

    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]

    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]

    if orientation is not None:
        result = [p for p in result if p["orientation"] == orientation]

    if q is not None:
        result = [p for p in result if q.strip().lower() in p["description"].lower()]

    return result