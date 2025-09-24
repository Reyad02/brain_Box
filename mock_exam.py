from google import genai
from dotenv import load_dotenv
import re
import json
import math
import time  

load_dotenv()
client = genai.Client()

prompt_template = """You are an expert NCLEX (National Council Licensure Examination) tutor. 
Your task is to generate **{num} practice multiple-choice questions** that test nursing pharmacology knowledge.  

### Requirements:
1. **Question Style**: Multiple-choice (4 options per question, labeled A–D).
2. **Answers**: Provide the correct option (e.g., "B").
3. **Explanations**: Each answer must include a clear, concise explanation of why the chosen option is correct and why the others are incorrect if relevant.
4. **Output Format**: JSON only (no extra text outside the JSON).
5. **JSON Schema**:
{{
  "questions": [
    {{
      "question": "string",
      "options": {{
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
      }}
    }}
  ],
  "answers": [
    {{
      "correct_option": "A",
      "explanation": "string",
      "subtopic": "string"
    }}
  ]
}}
"""

def extract_json(text):
    """Extract JSON block from the model response using regex."""
    match = re.search(r"```json(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def generate_chunk(num_questions):
    prompt = prompt_template.format(num=num_questions)
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
    )
    json_text = extract_json(response.text)
    data = json.loads(json_text)
    return data.get("questions", []), data.get("answers", [])

def generate_full_exam(total_questions=85, chunk_size=10, file_name="nclex_exam.json"):
    chunks = math.ceil(total_questions / chunk_size)
    questions_list = []
    answers_list = []

    for i in range(chunks):
        start_time = time.time()  

        num = min(chunk_size, total_questions - len(questions_list))
        questions, answers = generate_chunk(num)

        start_id = len(questions_list) + 1
        for idx, q in enumerate(questions):
            q["id"] = start_id + idx
        for idx, a in enumerate(answers):
            a["id"] = start_id + idx

        questions_list.extend(questions)
        answers_list.extend(answers)

        with open(file_name, "w") as f:
            json.dump({"questions": questions_list, "answers": answers_list}, f, indent=2)
        
        end_time = time.time()  
        print(f"Chunk {i+1} saved. Total questions so far: {len(questions_list)}. Time taken: {end_time - start_time:.2f} seconds")

    return questions_list, answers_list

questions, answers = generate_full_exam()
print("Final Total Questions:", len(questions))
print("Final Total Answers:", len(answers))

