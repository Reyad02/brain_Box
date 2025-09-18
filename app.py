from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

prompt = """You are an expert {topic} tutor. 
Your task is to generate **20 practice multiple-choice questions** that test nursing pharmacology knowledge.  

### Requirements:
1. **Question Style**: Multiple-choice (4 options per question, labeled A–D).
2. **Answers**: Provide the correct option (e.g., "B").
3. **Explanations**: Each answer must include a clear, concise explanation of why the chosen option is correct and why the others are incorrect if relevant.
4. **Output Format**: JSON only (no extra text outside the JSON).
5. **JSON Schema**:
{{
  "questions": [
    {{
      "id": 1,
      "question": "string",
      "options": {{
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
      }},
      "answer": "string",
      "explanation": "string",
      "subtopic": "string",  # short, concise category name (e.g., 'Antirheumatics', 'Diuretics')
      "complexity": "string" # e.g., easy, medium, hard
    }}
  ]
}}
"""


def generate_MCQ_ans(topic):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt.format(topic=topic)
    )
    return response.text
    
res = generate_MCQ_ans(topic="NCLEX-RN")
print(res)