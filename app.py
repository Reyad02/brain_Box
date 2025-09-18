from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Write 20 practice questions on the topic NCLEX -RN pharmacology with answers",
)

print(response.text)