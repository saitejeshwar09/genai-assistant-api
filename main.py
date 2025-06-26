from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils.parser import parse_document
from utils.summarizer import generate_summary
from utils.qa import answer_question
from utils.challenge import generate_questions, evaluate_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

doc_text = ""
doc_paragraphs = []

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    global doc_text, doc_paragraphs
    doc_text, doc_paragraphs = parse_document(file.file, file.content_type)
    summary = generate_summary(doc_text)
    return {"summary": summary}

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    if not doc_paragraphs:
        return JSONResponse(status_code=400, content={"error": "No document uploaded yet."})
    answer, ref = answer_question(question, doc_paragraphs)
    return {"answer": answer, "reference": ref}

@app.get("/challenge/")
def get_challenge():
    if not doc_paragraphs:
        return JSONResponse(status_code=400, content={"error": "No document uploaded yet."})
    return {"questions": generate_questions(doc_paragraphs)}

@app.post("/evaluate/")
def check_answer(user_answer: str = Form(...), correct_answer: str = Form(...)):
    result, feedback = evaluate_answer(user_answer, correct_answer)
    return {"correct": result, "feedback": feedback}
