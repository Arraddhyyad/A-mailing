from extract_emails import get_recent_email
from generate_reply import generate_reply
from send_reply import send_reply

email = get_recent_email()
print(f"\n From: {email['sender']}")
print(f" Subject: {email['subject']}")
print(f" Snippet: {email['snippet']}")

reply = generate_reply(email["snippet"])

print(f"\n Generated Reply:\n{reply}")

send_reply(reply, email['sender'], email['subject'])
