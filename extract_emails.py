from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

def get_recent_hr_emails():
    try:
        creds = Credentials.from_authorized_user_file('token.json')
        service = build('gmail', 'v1', credentials=creds)

        five_days_ago = (datetime.utcnow() - timedelta(days=5)).strftime('%Y/%m/%d')

        query = f'from:hr@company.com after:{five_days_ago}'

        result = service.users().messages().list(userId='me', q=query, maxResults=50).execute()

        if 'messages' not in result or not result['messages']:
            return {'error': 'No HR emails found in the last 5 days.'}

        emails = []
        for message in result['messages']:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()

            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '(No Date)')
            snippet = msg.get('snippet', '')

            emails.append({
                'id': message['id'],
                'subject': subject,
                'sender': sender,
                'date': date,
                'snippet': snippet
            })

        return emails

    except HttpError as error:
        return {'error': f'An error occurred: {error}'}
    except Exception as e:
        return {'error': f'Unexpected error: {e}'}
