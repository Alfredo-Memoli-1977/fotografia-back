from fastapi import APIRouter, Query
from typing import Literal
from pydantic import BaseModel
from pathlib import Path
from photos.utils import load_photos, update_photos

router = APIRouter()

DATA_PATH = Path("data/photos.json")

class update_image(BaseModel):
    
        id: int 
        title: str
        description: str
        category: str
        orientation: str
        preview_url: str
        raw_url: str
        price: float
        available: bool
    

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

@router.patch("/photos")
def uploadPhotos(photo:update_image):
    try:
        all_photos:update_image=load_photos()
        aux=[]
        for all_photo in all_photos:
            if all_photo["id"]!=photo.id:
                aux.append(all_photo)
            else:
                new_photo = photo.model_dump()
                new_photo["preview_url"] = all_photo["preview_url"]
                new_photo["raw_url"] = all_photo["raw_url"]
                aux.append(new_photo)
                            
                
        update_photos(aux)
        return {"success": True}
    except  Exception as e:
        return {"success": False, "error": str(e)}
    

