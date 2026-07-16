from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from auth.utils import create_temp_token, create_token, check_password, verify_temp_token
from auth.dependencies import get_current_admin, get_current_user
from users.utils import load_users, save_users

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    id: int 
    name: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
    is_admin: bool | None = None

class TempToken(BaseModel):
    token: str


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
        "id": users[-1]["id"]+1,
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

@router.patch("")
def update_users(users_update:list[UserUpdate],admin = Depends(get_current_admin)):
    try:
        users = load_users()
        # Elimino el usuario que no exista
        aux=[]
        for user in users:
            flag= False
            
            for user_update in users_update:
                if user["id"]==user_update.id:
                    flag= True
                    break
                

            if flag:
                aux.append(user)
                
        
        users= aux

        # Edito los usuarios existentes
        for user in users_update:
            for usr in users:
                if(usr["id"]==user.id):
                    if(user.name!=None):
                        usr["name"]=user.name
                    if(user.lastname!=None):
                        usr["lastname"]=user.lastname
                    if(user.email!=None):
                        usr["email"]=user.email
                    if(user.is_admin is not None):
                        usr["is_admin"]=user.is_admin
                    # if(user.password!=None):
                    #     usr["password"]=user.name
        
        save_users(users)
        return {"success": True}
    except  Exception as e:
        return {"success": False, "error": str(e)}
    

@router.get("/temporary_token")
def temporary_token(user=Depends(get_current_user)):
    return create_temp_token({
        "sub": str(user["id"]),
        "email": user["email"]
    })

@router.post("/login-with-temp-token")
def login_with_temp_token(data: TempToken):
    payload = verify_temp_token(data.token)

    user_id = payload.get("sub")

    users = load_users()
    user = next((u for u in users if str(u["id"]) == user_id), None)

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    new_token = create_token({
        "sub": str(user["id"]),
        "email": user["email"]
    })

    return {
        "user": {
            "id": user["id"],
            "name": user["name"],
            "lastname": user["lastname"],
            "email": user["email"],
            "is_admin": user.get("is_admin", False)
        },
        "token": new_token
    }