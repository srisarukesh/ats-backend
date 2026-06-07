from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from parser import extract_text
from scorer import score_resume

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ats-scorer-production.up.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        resume_text = extract_text(temp_path, file.filename)
        result = score_resume(resume_text, job_description)
        return {"success": True, "data": result}
    
    except Exception as e:
        return {"success": False, "error": str(e)}
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/")
def root():
    return {"message": "ATS Scorer API is running!"}