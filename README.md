TMU Assistant Chatbot

TMU Assistant Chatbot is an AI-powered university information and assistance system developed for Teerthanker Mahaveer University (TMU). The project helps students, applicants, and visitors access university-related information through an intelligent conversational interface.

The chatbot provides information related to:

Courses and programs
Admissions and eligibility
Fees and scholarships
Placements and career opportunities
Hostel and campus facilities

Unlike traditional rule-based systems, the chatbot uses Artificial Intelligence and Large Language Models (LLMs) to generate contextual and human-like responses.

Features
AI-powered conversational chatbot
Ollama + Gemma LLM integration
Intelligent context retrieval system
Flask backend with API communication
JSON-based knowledge base
Responsive modern UI
Dark mode support
Dynamic message rendering
Technologies Used
Frontend
HTML
CSS
JavaScript
Backend
Python
Flask
AI & Data
Ollama
Gemma LLM
JSON
Project Structure
TMU-Assistant-Chatbot/
│
├── app.py
├── ai_helper.py
├── requirements.txt
│
├── data/
│   └── tmu_data.json
│
├── templates/
│   └── index.html
│
├── templates/
│   ├── index.html
│
└── README.md
System Workflow

User Query
→ Flask Backend
→ Context Retrieval
→ JSON Knowledge Base
→ Ollama + Gemma AI Model
→ AI Response Generation
→ Frontend Display

Installation
Clone Repository
git clone <repository-link>
cd TMU-Assistant-Chatbot
Install Dependencies
pip install flask requests
Install and Run Ollama
ollama pull gemma:2b
ollama serve
Run Project
python app.py

Open in browser:

http://127.0.0.1:5000
Future Enhancements
Voice assistant integration
Multilingual support
Database integration
Mobile application version
Advanced AI models
Developed By

Mohammad Uvesh
Vaishali

Faculty of Engineering & Computing Sciences
Teerthanker Mahaveer University, Moradabad
