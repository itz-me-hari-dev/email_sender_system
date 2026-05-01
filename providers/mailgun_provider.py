import requests
import os
from dotenv import load_dotenv

load_dotenv()

class MailgunProvider:
    def __init__(self):
        self.api_key = os.getenv("MAILGUN_API_KEY")
        self.domain = os.getenv("MAILGUN_DOMAIN")

    def send(self, user):
        response = requests.post(
            f"https://api.mailgun.net/v3/{self.domain}/messages",
            auth=("api", self.api_key),
            data={
                "from": f"Mailgun Test <mailgun@{self.domain}>",
                "to": [user["email"]],
                "subject": "Test Email",
                "text": f"Hello {user['name']}, this is a test email."
            }
        )

        if response.status_code != 200:
            raise Exception(f"Mailgun failed: {response.text}")