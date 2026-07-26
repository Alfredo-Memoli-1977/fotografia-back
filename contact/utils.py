import os
from dotenv import load_dotenv
from email.message import EmailMessage
from .schemas import ContactMsg
import smtplib
from pathlib import Path

load_dotenv()

def send_contact_msg(data:ContactMsg):
    # Para el logo
    

    logo_path = Path(__file__).parent / "assets"/"fotoEmocionalSF.png"
    #Leo el archivo de la plantilla
    template_path=Path(__file__).parent / "email_template.html"
    html= template_path.read_text(encoding="utf-8")
    html = html.replace("{{name}}", data.name)
    html = html.replace("{{email}}", data.email)
    html = html.replace("{{subject}}", data.subject)
    html = html.replace("{{message}}", data.message)
    html = html.replace("{{logo_cid}}", "logo")

    msg = EmailMessage()
    sFrom = os.getenv("MAIL_USERNAME")
    sPassword = os.getenv("MAIL_PASSWORD")
    sTo = os.getenv("MAIL_TO")
    sSMTPServer = os.getenv("MAIL_HOST")
    nPuerto = int(os.getenv("MAIL_PORT"))

    sAsunto = data.subject
    sCuerpo = html

    msg["From"] = sFrom
    msg["To"]=sTo
    msg["Subject"] = sAsunto
    
    msg.set_content("Tu cliente de correo no soporta HTML.")
    msg.add_alternative(sCuerpo, subtype="html")

    with open(logo_path, "rb") as logo_file:
        logo_data = logo_file.read()

    msg.get_payload()[1].add_related(
        logo_data,
        maintype="image",
        subtype="png",
        cid="<logo>",
    )

    email = smtplib.SMTP(sSMTPServer, nPuerto)

    try:
        email.starttls()
        email.login(sFrom, sPassword)
        email.send_message(msg)
        return {"success": True}

    except Exception:
        return {"success": False}

    finally:
        email.quit()

    '''html = template_path.read_text(encoding="utf-8")

html = html.replace("{{name}}", data.name)
html = html.replace("{{message}}", data.message)'''