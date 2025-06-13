import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(email_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an email assistant that helps write polite, helpful responses."},
            {"role": "user", "content": email_text}
        ]
    )
    return response.choices[0].message.content.strip()
