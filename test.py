from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Literal
from google import genai
from dotenv import load_dotenv
import time

# ------------------------
# Setup
# ------------------------
load_dotenv()
client = genai.Client()
app = FastAPI(title="NCLEX MCQ Generator API", version="1.0")

# ------------------------
# Test Plan Rules (RN vs PN)
# ------------------------
RN_RULES = """
### NCLEX-RN Test Plan Rules:
1. Content distribution (approximate percentages):
   - Safe & Effective Care Environment (25–37%)
       • Management of Care (15–21%)
       • Safety & Infection Control (10–16%)
   - Health Promotion & Maintenance (6–12%)
   - Psychosocial Integrity (6–12%)
   - Physiological Integrity (38–62%)
       • Basic Care & Comfort (6–12%)
       • Pharmacological & Parenteral Therapies (13–19%)
       • Reduction of Risk Potential (9–15%)
       • Physiological Adaptation (11–17%)

2. Emphasize **clinical judgment and decision-making**, not just recall.
3. Balance difficulty levels: easy, medium, hard.
4. Pharmacology must appear prominently (≥13% of items).
5. Use realistic scenarios, labs, priorities, delegation/safety decisions.
"""

PN_RULES = """
### NCLEX-PN Test Plan Rules:
1. Content distribution (approximate percentages):
   - Safe & Effective Care Environment (~26–38%)
       • Coordinated Care (16–22%)
       • Safety & Infection Control (10–16%)
   - Health Promotion & Maintenance (7–13%)
   - Psychosocial Integrity (8–14%)
   - Physiological Integrity (~40–60%)
       • Basic Care & Comfort
       • Pharmacological Therapies (11–17%)
       • Reduction of Risk Potential (10–16%)
       • Physiological Adaptation (7–13%)

2. Include **clinical judgment/decision-making**; ~10% can be standalone CJ items.
3. Balance difficulty levels: easy, medium, hard.
4. Use realistic patient scenarios, labs, and plausible distractors.
5. Pharmacology questions should be well represented (≥11%).
"""

# ------------------------
# Prompt Builder
# ------------------------
def build_prompt(exam_type: str):
    if exam_type.upper() == "RN":
        rules = RN_RULES
        exam_label = "NCLEX-RN"
    elif exam_type.upper() == "PN":
        rules = PN_RULES
        exam_label = "NCLEX-PN"
    else:
        raise ValueError("exam_type must be either 'RN' or 'PN'")

    prompt = f"""
You are an expert {exam_label} tutor. 
Your task is to generate **20 practice multiple-choice questions** that mirror the official {exam_label} Test Plan.

{rules}

### Output Requirements:
1. **Question Style**: Multiple-choice (4 options per question, A–D). Some may allow multiple correct answers.
2. **Answers**: Provide the correct option(s).
3. **Explanations**: Explain why the correct answer is correct, and why others are incorrect when relevant.
4. **Format**: JSON only, following this schema:

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
      "answer": "string | [string]",
      "explanation": "string",
      "subtopic": "string",
      "complexity": "string",
      "type": "string"
    }}
  ]
}}
"""
    return prompt

# ------------------------
# Request/Response Models
# ------------------------
class MCQRequest(BaseModel):
    exam_type: Literal["RN", "PN"]

class MCQResponse(BaseModel):
    time_taken: float
    result: str

# ------------------------
# FastAPI Endpoint
# ------------------------

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/generate_mcq", response_model=MCQResponse)
def generate_mcq(request: MCQRequest):
    start_time = time.time()
    prompt = build_prompt(request.exam_type)

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    end_time = time.time()
    return MCQResponse(
        time_taken=round(end_time - start_time, 2),
        result=response.text
    )

