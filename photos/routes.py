from fastapi import APIRouter, File, Query, UploadFile
from typing import Literal
from pydantic import BaseModel
from pathlib import Path
from photos.utils import load_photos, update_photos, upload_new_photos

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
def update_Photos(photo:update_image):
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
    
@router.post("/photos")
def upload_photos(photos:list[UploadFile]=File(...)):
    all_photos=load_photos()
    aux_photos=[]
    duplicates=[]
    new_id=0
    for all_photo in all_photos:
        for photo in photos:
            if photo.filename.lower().rsplit(".", 1)[0] == all_photo["title"].lower():
                # return {"success": False, "error": "Foto duplicada"}
                duplicates.append(photo.filename)

        if(new_id<all_photo["id"]):
            new_id=all_photo["id"]

    for photo in photos:
        if photo.filename in duplicates:
            continue

        aux_photos.append(photo)

    

        
    try:
        for photo in aux_photos:
            filename = photo.filename.lower()
            raw_filename=""
            for raw_photos in aux_photos:
                if raw_photos.filename.lower()!=filename and raw_photos.filename.lower().rsplit(".", 1)[0]==filename.rsplit(".", 1)[0]:
                    raw_filename=raw_photos.filename


            if filename.endswith((".jpg", ".jpeg", ".png", ".webp")):
                
                new_id+=1
                new_photo = {
                    "id": new_id,
                    "title": photo.filename.rsplit(".", 1)[0],
                    "description": "",
                    "category": "",
                    "orientation": "landscape",
                    "preview_url": f"/images/preview/{photo.filename}",
                    "raw_url": f"/images/raw/{raw_filename}",
                    "price": 0,
                    "available": False
                }
                all_photos.append(new_photo)
           
        update_photos(all_photos)
        
        upload_new_photos(aux_photos)
        if duplicates:
            return {
                "success": False,
                "error": f"Fotos duplicadas: {len(duplicates)}. Subidas: {len(photos)-len(duplicates)}",
                "duplicates": duplicates,
            }
        return {"success": True}
    except  Exception as e:
        return {"success": False, "error": str(e)}

