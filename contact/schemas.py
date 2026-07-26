from pydantic import BaseModel, EmailStr

class ContactMsg(BaseModel):
    name:str
    email:EmailStr
    subject:str
    message:str