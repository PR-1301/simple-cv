import smtplib
from PIL import Image
from io import BytesIO
from email.message import EmailMessage

username = "itsallgoodman2026@gmail.com"
password = "mire wnzj bddj fjfb"
receiver = "deviramaswamy@gmail.com"

def send_email(image_path):

    email_message = EmailMessage()
    email_message["Subject"] = "Object detected!"
    email_message.set_content("Hey, Someone or something entered!")

    with open(image_path, "rb") as file:
        content = file.read()
    image_data = BytesIO(content)
    img = Image.open(image_data)
    image_format = img.format
    email_message.add_attachment(content, maintype="image", subtype=image_format)

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    # initiates the convo btw python and gmail
    gmail.ehlo()
    # Upgrades the connection to a secure encrypted connection (TLS).transport layer security
    gmail.starttls()
    gmail.login(username, password)
    gmail.sendmail(username, receiver, email_message.as_string())
    gmail.quit()

if __name__ == "__main__":
    send_email(image_path='images/complete.png')


