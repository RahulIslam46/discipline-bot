import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY") or os.getenv("GRoQO_API_KEY")

if not api_key:
       raise RuntimeError("Missing GROQ_API_KEY in environment or .env")

client = Groq(api_key=api_key)
response = client.chat.completions.create(
       model="llama-3.3-70b-versatile",
       messages=[
              {"role": "user", "content": "You are a helpful assistant that provides information"}
       ],
)
print(response.choices[0].message.content)