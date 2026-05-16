from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from auth.utils import create_token, check_password
from auth.dependencies import get_current_admin
from users.utils import load_users, save_users

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    password: str




@router.get("")
def get_users(admin = Depends(get_current_admin)):
    
    users = load_users()
    

    if not users:
        return {"message": "No se encontraron usuarios"}

    return [
    {
        "id": usr["id"],
        "name":usr["name"],
        "lastname":usr["lastname"],
        "email": usr["email"],
        "is_admin": usr.get("is_admin", False)
    }
    for usr in users # user acá es cada elemento del objeto no el user de arriba
]
    


@router.post("")
def create_user(user: UserCreate):
    users = load_users()

    user_exists = any(existing_user["email"] == user.email for existing_user in users)

    if user_exists:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    if not check_password(user.password):
        raise HTTPException(status_code=400, detail="Formato de contraseña incorrecto")
    
    hashed_password = pwd_context.hash(user.password)

    new_user = {
        "id": len(users) + 1,
        "name":user.name,
        "lastname":user.lastname,
        "email": user.email,
        "password": hashed_password,
        "is_admin": False
    }

    users.append(new_user)
    save_users(users)
    
   

    token = create_token({
        "sub": str(new_user["id"]),
        "email": new_user["email"]
    })

    return {
        "user": {
            "id": new_user["id"],
            "name":new_user["name"],
            "lastname":new_user["lastname"],
            "email": new_user["email"],
            "is_admin": new_user.get("is_admin", False)
        },
        "token": token
    }
