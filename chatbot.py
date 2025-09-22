from google import genai
from dotenv import load_dotenv
import uuid
import os
import json

load_dotenv()

HISTORY_FILE = "chat_histories.json"

client = genai.Client()

if os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, "r") as f:
            chat_histories = json.load(f)
    except json.JSONDecodeError:
        chat_histories = {}
else:
    chat_histories = {}

def save_history():
    """Write chat_histories dict to JSON file"""
    with open(HISTORY_FILE, "w") as f:
        json.dump(chat_histories, f, indent=2)
    
prompt_template = """You are an expert NCLEX (National Council Licensure Examination) tutor.
- Your role is to help nursing students prepare for the NCLEX exam.
- If the user asks a question unrelated to NCLEX, politely respond that you can only assist with NCLEX-related queries.
- Always explain your answers clearly, as if teaching a student.
- Make sure the naswer is accurate and very short and concise. not more than 50 words

Conversation so far:
{history}

User question: {question}
"""

def get_or_create_session(session_id=None):
    """Return existing session_id or create a new one if it doesn't exist"""
    if session_id and session_id in chat_histories:
        return session_id
    new_session_id = str(uuid.uuid4())
    chat_histories[new_session_id] = []
    save_history()

    return new_session_id

def chatbot_ans(question, session_id=None, max_history=10):
    session_id = get_or_create_session(session_id)
    
    history_msgs = chat_histories.get(session_id, [])[-max_history:]
    history_str = ""
    for msg in history_msgs:
        history_str += f"User: {msg['user_message']}\nAssistant: {msg['assistant_message']}\n"
    
    final_prompt = prompt_template.format(history=history_str, question=question)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=final_prompt
    )
    
    chat_histories[session_id].append({
        "user_message": question,
        "assistant_message": response.text,
    })
    
    save_history()

    return response.text, session_id

# res, session_id = chatbot_ans("Who is CR7?")
# res, session_id = chatbot_ans("What are the key differences between Type 1 and Type 2 diabetes?", session_id="b7290b16-ee45-4c7e-b368-56063fa5e213")
res, session_id = chatbot_ans("is Bangladesh win last match?", session_id="b7290b16-ee45-4c7e-b368-56063fa5e213")

# res, session_id = chatbot_ans("Who is LM10?")