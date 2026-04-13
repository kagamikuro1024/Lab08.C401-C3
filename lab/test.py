from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('OPENAI_API_KEY')
if not key:
    print('ERROR: OPENAI_API_KEY not set in .env')
    exit(1)

client = OpenAI(api_key=key)
response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{'role': 'user', 'content': 'Hello'}],
    max_tokens=10
)
print('✓ API connection successful')
print(f'  Response: {response.choices[0].message.content}')
