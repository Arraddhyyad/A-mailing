from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def get_recent_email():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('gmail', 'v1', credentials=creds)

    result = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
    message_id = result['messages'][0]['id']
    msg = service.users().messages().get(userId='me', id=message_id, format='full').execute()

    headers = msg['payload']['headers']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
    snippet = msg['snippet']

    return {
        'id': message_id,
        'subject': subject,
        'sender': sender,
        'snippet': snippet
    }
