from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import json
import re
import os
import requests
from typing import List, Dict
from difflib import get_close_matches

# Load environment variables
load_dotenv()

app = FastAPI(title="Mini AI Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    matched_question: str
    source: str  # "knowledge_base" or "openrouter"


# OpenRouter API configuration
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


# Load knowledge base
def load_knowledge_base(file_path: str) -> Dict[str, str]:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        # Return a default knowledge base if file doesn't exist
        return {
            "How can I improve my productivity?": "To improve productivity, try techniques like time blocking, prioritizing tasks with the Eisenhower Matrix, minimizing distractions, and taking regular breaks using the Pomodoro technique.",
            "What are the benefits of remote work?": "Remote work offers benefits like flexibility, no commute, better work-life balance, and access to a global talent pool. However, it requires discipline and good communication practices.",
            "How do I start a startup?": "Starting a startup involves identifying a problem, validating your idea, creating a business plan, building a minimum viable product (MVP), seeking funding, and iterating based on customer feedback.",
            "What is the best way to manage a remote team?": "Effective remote team management requires clear communication, regular check-ins, trust, the right tools (like Slack, Zoom, Asana), and setting clear expectations and goals.",
            "How can I stay focused while working from home?": "Create a dedicated workspace, establish a routine, set boundaries with family, use time management techniques, and take regular breaks to maintain focus while working from home."
        }


# Load chat history
def load_chat_history(file_path: str) -> List[Dict]:
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Save chat history
def save_chat_history(file_path: str, history: List[Dict]):
    with open(file_path, 'w') as file:
        json.dump(history[-10:], file, indent=2)  # Keep only last 10 messages


# Preprocess text for matching
def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text


# Find best match in knowledge base
def find_best_match(user_question: str, questions: List[str]) -> str:
    user_question_processed = preprocess_text(user_question)
    question_list = [preprocess_text(q) for q in questions]

    matches = get_close_matches(user_question_processed, question_list, n=1, cutoff=0.6)
    return matches[0] if matches else None


# Get answer from knowledge base
def get_knowledge_base_answer(question: str, knowledge_base: Dict[str, str]) -> str:
    for q, a in knowledge_base.items():
        if preprocess_text(q) == preprocess_text(question):
            return a
    return None


# Get answer from OpenRouter API
def get_openrouter_answer(question: str) -> str:
    if not OPENROUTER_API_KEY:
        return get_fallback_response(question)

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",  # Optional but recommended
            "X-Title": "Professional AI Chatbot"  # Optional but recommended
        }

        payload = {
            "model": "openai/gpt-3.5-turbo",  # You can change this to any model supported by OpenRouter
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful professional assistant that answers questions about productivity, remote work, startups, and business topics. Provide concise, professional responses."
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            print(f"OpenRouter API error: {response.status_code} - {response.text}")
            return get_fallback_response(question)

        result = response.json()

        # Extract the generated text from the response
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"].strip()

        return get_fallback_response(question)

    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
        print(f"OpenRouter API error: {e}")
        return get_fallback_response(question)


# Fallback response for when the API fails
def get_fallback_response(question: str) -> str:
    question_lower = question.lower()

    # Simple rule-based responses for common questions
    if any(word in question_lower for word in ["hello", "hi", "hey", "greeting"]):
        return "Hello! I'm your professional AI assistant. How can I help you today?"
    elif any(word in question_lower for word in ["how are you", "how do you do"]):
        return "I'm functioning well, thank you for asking! I'm here to help with your professional questions."
    elif any(word in question_lower for word in ["name", "who are you"]):
        return "I'm a professional AI chatbot designed to answer questions about productivity, remote work, startups, and related topics."
    elif any(word in question_lower for word in ["thank", "thanks", "appreciate"]):
        return "You're welcome! Is there anything else you'd like to know?"
    elif any(word in question_lower for word in ["bye", "goodbye", "see you"]):
        return "Goodbye! Feel free to return if you have more questions."
    else:
        return "I'm not sure how to answer that specific question. Could you try asking about productivity, remote work, or startups?"


# API endpoints
@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    # Load knowledge base
    knowledge_base = load_knowledge_base("knowledge_base.json")

    # Find best match in knowledge base
    best_match = find_best_match(request.question, list(knowledge_base.keys()))

    if best_match:
        # Get the original question format from knowledge base
        original_question = None
        for q in knowledge_base.keys():
            if preprocess_text(q) == best_match:
                original_question = q
                break

        # Get answer from knowledge base
        answer = knowledge_base[original_question]
        response = AnswerResponse(
            answer=answer,
            matched_question=original_question,
            source="knowledge_base"
        )
    else:
        # Get answer from OpenRouter API or fallback
        answer = get_openrouter_answer(request.question)
        response = AnswerResponse(
            answer=answer,
            matched_question="",
            source="openrouter"
        )

    # Save to chat history
    chat_history = load_chat_history("chat_history.json")
    chat_history.append({
        "question": request.question,
        "answer": response.answer,
        "matched_question": response.matched_question,
        "source": response.source
    })
    save_chat_history("chat_history.json", chat_history)

    return response


@app.get("/history")
async def get_chat_history():
    history = load_chat_history("chat_history.json")
    return {"history": history[-10:]}  # Return only last 10 messages


@app.get("/")
async def root():
    return {"message": "Mini AI Chatbot API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)