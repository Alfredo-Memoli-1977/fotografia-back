from fastapi import APIRouter
from .schemas import ContactMsg
from contact.utils import send_contact_msg 


router = APIRouter(prefix="/contact", tags=["Contact"])



@router.post("")
def send_msg(data:ContactMsg):
    return send_contact_msg(data)

