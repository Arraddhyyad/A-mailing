from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
import base64

def send_reply(reply_text, to, subject):
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(reply_text)
    message['to'] = to
    message['subject'] = "Re: " + subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw_message}

    service.users().messages().send(userId='me', body=body).execute()
    print(f"Reply sent to {to}")
