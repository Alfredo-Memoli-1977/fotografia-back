from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from auth.utils import create_token, verify_password
from users.utils import load_users
from auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str



@router.post("/login")
def login(data: LoginRequest):
    users = load_users()

    user = next((u for u in users if u["email"] == data.email), None)

    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    token = create_token({
        "sub": str(user["id"]),
        "email": user["email"]
    })

    return {
        "user": {
            "id": user["id"],
            "name":user["name"],
            "lastname":user["lastname"],
            "email": user["email"],
            "is_admin": user.get("is_admin", False)
        },
        "token": token
    }

@router.get("/check")
def check(user = Depends(get_current_user)):
    return user