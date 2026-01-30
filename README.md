Bhai, Phase 0 shuru karte hain! Is phase ka main maqsad hai ek mazboot foundation taiyar karna taaki tera code organized rahe aur GitHub par professional dikhe.

Yahan hum "Zero Human Code" policy follow kar rahe hain, isliye main tujhe saare folder structures aur setup commands de raha hoon.

## 1. Project Folder Structure
Sabse pehle apne computer par ek naya folder banao (e.g., ai-crm-hcp-system) aur uske andar ye structure follow karo:

Plaintext
ai-crm-hcp-system/
├── backend/            # FastAPI, LangGraph, and Tools
├── frontend/           # React, Redux, and Inter Font
├── .gitignore          # To hide secrets and node_modules
└── README.md           # Professional project documentation
## 2. The .gitignore File (Security First)
Pharma aur AI projects mein API keys (Groq) aur Database credentials leak nahi honi chahiye. Is code ko copy karke .gitignore file mein daal do:

Plaintext
# Python
__pycache__/
*.py[cod]
.env
venv/

# Node (Frontend)
node_modules/
build/
.env.local

# Databases
*.sqlite
*.db

# OS
.DS_Store
## 3. Initial README.md (Project Bio)
GitHub par jab koi aaye toh use pata chale ki ye kitna cool project hai. Ye content copy-paste kar lo:

Markdown
# AI-First CRM: HCP Module (LogInteraction)

An intelligent Customer Relationship Management system for Life Sciences, powered by LangGraph and Groq (Gemma-2-9b-it).

## 🚀 Key Features
- **Hybrid Logging:** Log HCP interactions via structured forms or a conversational AI agent.
- **AI Agent:** Built with **LangGraph** for multi-step reasoning and tool calling.
- **Tools:** Includes LogInteraction, EditInteraction, and Appointment Auto-Scheduler.

## 🛠 Tech Stack
- **Frontend:** React, Redux, Google Inter Font.
- **Backend:** Python (FastAPI), LangGraph, SQLAlchemy.
- **LLM:** Gemma-2-9b-it via Groq.

## 📁 Repository Structure
- `/backend`: FastAPI server and LangGraph agent logic.
- `/frontend`: React UI with Redux state management. 
