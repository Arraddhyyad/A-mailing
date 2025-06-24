from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

def get_recent_hr_email():
    try:
        creds = Credentials.from_authorized_user_file('token.json')
        service = build('gmail', 'v1', credentials=creds)

        query = 'from:hr@company.com'  
        result = service.users().messages().list(userId='me', q=query, maxResults=1).execute()

        if 'messages' not in result or not result['messages']:
            return {'error': 'No HR emails found.'}

        message_id = result['messages'][0]['id']
        msg = service.users().messages().get(userId='me', id=message_id, format='full').execute()

        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
        snippet = msg.get('snippet', '')

        return {
            'id': message_id,
            'subject': subject,
            'sender': sender,
            'snippet': snippet
        }

    except HttpError as error:
        return {'error': f'An error occurred: {error}'}
    except Exception as e:
        return {'error': f'Unexpected error: {e}'}
