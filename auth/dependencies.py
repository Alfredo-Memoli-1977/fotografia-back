from fastapi import  HTTPException,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.utils import verify_token
from users.utils import load_users

security = HTTPBearer()

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = verify_token(token)
    except:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user_id=payload.get('sub')
    users = load_users()
    user = next((u for u in users if str(u["id"]) == user_id), None)

    if not user or not user.get('is_admin'):
        raise HTTPException(status_code=403, detail="No autorizado")

    return user

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = verify_token(token)
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

    user_id = payload.get("sub")

    users = load_users()
    user = next((u for u in users if str(u["id"]) == user_id), None)

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user