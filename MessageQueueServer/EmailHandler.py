import smtplib
from email.mime.text import MIMEText
import os

class EmailHandler:
    def __init__(self):
        pubEmailInfo = dict({
            "SMTP_SERVER": "smtp.gmail.com",
            "SMTP_ID": os.getenv("HOST_EMAIL"),
            "SMTP_PW": os.getenv("HOST_PASSWD")
        })
        self.smtpServer = pubEmailInfo["SMTP_SERVER"]
        self.smtpId = pubEmailInfo["SMTP_ID"]
        self.smtpPw = pubEmailInfo["SMTP_PW"]

    def send_email(self, receiver, subject, content):
        content = f"\nUpdate your subscribe subject! \n\nSubject : [{subject}] \n{content}"
        message = MIMEText(_text=content, _charset="utf-8")

        message['Subject'] = f"Pub-Sub System update content - {subject}"
        message['From'] = self.smtpId
        message['To'] = receiver

        with smtplib.SMTP(self.smtpServer) as connection:
            connection.starttls()
            connection.login(user=self.smtpId, password=self.smtpPw)
            response = connection.sendmail(self.smtpId, receiver, message.as_string())

            if not response:
                print(f"Successful send email to - {receiver}")
            else:
                print("Error during send email :", response)
