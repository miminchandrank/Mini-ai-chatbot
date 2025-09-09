Professional AI Chatbot - README
📋 Project Overview
A web-based AI chatbot that answers professional questions about productivity, remote work, startups, and business topics. The system first checks a local knowledge base for matching questions, and if no match is found, uses OpenRouter's AI models to generate responses.

🚀 Quick Start
Prerequisites
Python 3.8+

Node.js 14+

npm or yarn

Installation & Setup
Clone the repository

bash
git clone <your-repo-url>
cd professional-ai-chatbot
Backend Setup (Python)

bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
echo "OPENROUTER_API_KEY=your_openrouter_api_key_here" > .env
Frontend Setup (React)

bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
Running the Application
Start the Backend Server

bash
cd backend
python app.py
Server runs on: http://localhost:8000

Start the Frontend Development Server

bash
cd frontend
npm start
Application runs on: http://localhost:3000

Access the Application
Open your browser and go to http://localhost:3000

🛠️ Technologies Used
Backend
FastAPI - Modern, fast web framework for building APIs

Python 3.8+ - Programming language

Uvicorn - ASGI server for running FastAPI

Requests - HTTP library for API calls

python-dotenv - Environment variable management

Pydantic - Data validation and settings management

Frontend
React - JavaScript library for building user interfaces

CSS3 - Styling and responsive design

Fetch API - For making HTTP requests to the backend

AI/ML Services
OpenRouter API - For AI-generated responses when questions aren't in the knowledge base

Custom Knowledge Base - Local JSON file with curated Q&A pairs

📁 Project Structure
text
professional-ai-chatbot/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── knowledge_base.json    # Local Q&A database
│   ├── chat_history.json      # Conversation history
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Styles
│   │   ├── index.js          # React entry point
│   │   └── index.css         # Global styles
│   ├── public/
│   │   └── index.html        # HTML template
│   └── package.json          # Node.js dependencies
└── README.md
🔧 API Endpoints
POST /ask
Purpose: Submit a question to the chatbot

Request Body: {"question": "Your question here"}

Response:

json
{
  "answer": "Response text",
  "matched_question": "Matched question from KB (if applicable)",
  "source": "knowledge_base" or "openrouter"
}
GET /history
Purpose: Retrieve chat history

Response:

json
{
  "history": [
    {
      "question": "User question",
      "answer": "Bot response",
      "matched_question": "Matched question",
      "source": "response source"
    }
  ]
}
🧠 Knowledge Base
The system includes a pre-defined knowledge base with questions about:

Productivity techniques

Remote work best practices

Startup fundamentals

Team management

Work-life balance

Example Q&A:

"How can I improve my productivity?" → Time blocking, Eisenhower Matrix, etc.

"What are the benefits of remote work?" → Flexibility, no commute, etc.

⚙️ Configuration
Environment Variables
Create a .env file in the backend directory:

env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OpenRouter Configuration
The system uses OpenRouter's API with the following settings:

Model: openai/gpt-3.5-turbo (configurable)

Temperature: 0.7 (balanced creativity)

Max Tokens: 200 (concise responses)

System prompt: Professional business assistant

🧪 Testing
Test Knowledge Base Questions
"How can I improve my productivity?"

"What are the benefits of remote work?"

"How do I start a startup?"

Test LLM Questions
"What is the capital of France?"

"Explain quantum computing"

"What are the latest tech trends?"

Verification
Knowledge Base responses: Blue "KB" badge, instant response

LLM responses: Green "AI" badge, slightly slower response

Fallback responses: Handles greetings and edge cases gracefully
