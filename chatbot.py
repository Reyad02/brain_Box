from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

prompt = """You are an expert NCLEX (National Council Licensure Examination) tutor.
- Your role is to help nursing students prepare for the NCLEX exam.
- If the user asks a question unrelated to NCLEX, politely respond that you can only assist with NCLEX-related queries.
- Always explain your answers clearly, as if teaching a student.
questions: {question}
"""


def chatbot_ans(question):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt.format(question=question)
    )
    return response.text
    
# res = chatbot_ans(question="What are the key differences between Type 1 and Type 2 diabetes?")
res = chatbot_ans(question="Who is CR7?")
print(res)