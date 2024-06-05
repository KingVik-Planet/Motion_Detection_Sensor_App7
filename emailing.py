import smtplib
from email.message import EmailMessage
import imghdr
from key import password, sender, receiver

password = password
sender = sender
receiver = receiver
def send_email(image_path):
    print("Send_email started")
    email_message = EmailMessage()
    email_message["Subject"] = "Object in Range, Motion Detected!"
    email_message.set_content("Hey There are some movement and Object are in Range,"
                              "This Movement was detected by the app!")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype = "image", subtype = imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, receiver, email_message.as_string())
    gmail.quit()
    print("send email ended")


if __name__ == "__main__":
    send_email(image_path="images/20.png")