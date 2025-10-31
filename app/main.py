import json
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.llm import HybridLLM

app = FastAPI(title="Hybrid Tavily + SerpAPI LLM")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the LLM
llm = HybridLLM()

@app.get("/")
def root():
    return {"message": "Backend running: Tavily + SerpAPI hybrid model"}

@app.post("/query")
async def query_endpoint(request: Request):
    body = await request.json()
    question = body.get("question", "")
    if not question:
        return {"error": "No question provided"}
    response = llm.get_solution(question)
    return response

@app.post("/feedback")
async def feedback_endpoint(request: Request):
    body = await request.json()
    feedback_rating = body.get("rating", "")
    feedback_comment = body.get("comment", "")
    question = body.get("question", "")

    if not feedback_rating:
        return {"error": "Feedback rating is required"}

    # Load existing feedback
    try:
        with open("feedback_store.json", "r") as f:
            feedback_list = json.load(f)
    except FileNotFoundError:
        feedback_list = []

    # Append new feedback
    feedback_list.append({
        "question": question,
        "rating": feedback_rating,
        "comment": feedback_comment,
        "timestamp": datetime.now().isoformat()
    })

    # Save back to file
    with open("feedback_store.json", "w") as f:
        json.dump(feedback_list, f, indent=4)

    return {"message": "Feedback submitted successfully"}
