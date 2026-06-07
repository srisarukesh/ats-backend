from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def score_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are an ATS (Applicant Tracking System) expert.

Analyze this resume against the job description and return a JSON response with exactly this structure:
{{
  "ats_score": <number 0-100>,
  "matched_keywords": [<list of keywords found in both resume and JD>],
  "missing_keywords": [<list of important keywords from JD missing in resume>],
  "section_analysis": {{
    "experience": "<feedback>",
    "skills": "<feedback>",
    "education": "<feedback>"
  }},
  "improvements": [<list of 3-5 specific improvement suggestions>]
}}

Return ONLY the JSON, no extra text.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    text = response.choices[0].message.content.strip()

    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    return json.loads(text.strip())