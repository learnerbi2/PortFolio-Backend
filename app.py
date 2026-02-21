from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import os

# ✅ Force load from current directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)
CORS(app)

# add keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# add my system prompt here
SYSTEM_PROMPT = """You are an AI assistant on Rohit Bamne's portfolio website.
You help visitors learn about Rohit's skills, projects, education, and experience.
Keep responses short, friendly, and professional.

Here are Rohit's details:

NAME: Rohit Bamne
LOCATION: Noida-ready (Based in Bhopal, MP)
CONTACT: bamnerohit29@gmail.com | +91-7879390759
GITHUB: github.com/learnerbi2
LINKEDIN: linkedin.com/in/rohit-bamne

EDUCATION:
- B.E. in Computer Science & Engineering (2022–2026) at SISTec-E, Bhopal | CGPA: 6.5+
- Class XII from Paradise Higher Secondary School, Amla, MP | 88.2%

TECHNICAL SKILLS:
- Programming: Java (DSA), JavaScript (ES6+), Python, SQL
- Web Development: MERN Stack (MongoDB, Express.js, React.js, Node.js), Next.js, HTML5, CSS3
- Core Concepts: OOPS, Scalable Architecture, Modular Design, Performance Optimization
- Databases: SQL, MongoDB
- Tools: Git, GitHub, VS Code, Postman
- Testing: Manual Testing, Basic Unit Testing

PROJECTS:
1. C.V.D. Risk Assessment Platform (Python, Flask, SQL, MERN Stack)
   - Scalable web app for real-time health risk assessment
   - Built RESTful APIs with SQL queries optimized to reduce response time by 30%
   - Implemented authentication and responsive React.js frontend
   - Achieved 99% uptime through manual testing and validation

2. Spotify Web Clone (HTML, CSS, JavaScript)
   - Responsive UI with reusable components
   - Clean code practices with performance optimization

CERTIFICATIONS & ACHIEVEMENTS:
- Python Essentials 1 & 2 (60+ hours)
- DSA Workshop at MANIT Bhopal (30+ problems solved)
- Top 10 Team – Smart India Hackathon (Women Safety App)
- Selected Participant – VITB-JHU Health Hack 2025 (Global Collaboration)

CORE COMPETENCIES:
Analytical Thinking, Problem Solving, Rapid Learning, Cross-functional Collaboration,
Attention to Detail, High-Performance Systems Mindset

INSTRUCTIONS:
- Answer questions about Rohit's skills, projects, experience, and education
- If asked something unrelated to Rohit or his portfolio, politely redirect
- Keep answers concise and professional
- Encourage visitors to reach out via email or LinkedIn for opportunities
"""


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Flask is working!"})

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Server is running"})

# add api endpoint for chat
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    payload = {
        "model": "arcee-ai/trinity-large-preview:free",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            *messages
        ],
        "max_tokens": 500
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Portfolio Chatbot"
    }

    # try:
    #     response = requests.post(OPENROUTER_URL, json=payload, headers=headers)
    #     response.raise_for_status()
    #     reply = response.json()["choices"][0]["message"]["content"]
    #     print(f"User: {messages[-1]['content']}")
    #     print(f"AI: {reply}")
    #     return jsonify({"reply": reply})
    
    # except requests.exceptions.HTTPError as e:
    #     return jsonify({"error": str(e)}), response.status_code
    # except Exception as e:
    #     return jsonify({"error": "Something went wrong"}), 500
    try:
            response = requests.post(OPENROUTER_URL, json=payload, headers=headers)
            response.raise_for_status()
            reply = response.json()["choices"][0]["message"]["content"]
            print(f"User: {messages[-1]['content']}")
            print(f"AI: {reply}")
            return jsonify({"reply": reply})
        
    except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")
            return jsonify({"error": "Failed to get response from AI"}), 500
    except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "Something went wrong"}), 500    
    
if __name__ == "__main__":
    app.run(port=5000, debug=True)