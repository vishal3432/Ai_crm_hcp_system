from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.messages import HumanMessage
from agent import app_agent
from database import SessionLocal, Interaction

app = FastAPI(title="AI CRM HCP API")

# 1. CORS Setup (Taaki React app isse baat kar sake)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development ke liye sab allowed hai
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Data Models (Request/Response structure)
class ChatRequest(BaseModel):
    message: str

class InteractionResponse(BaseModel):
    id: int
    hcp_name: str
    summary: str
    product: str

# 3. API Endpoints

@app.get("/")
def home():
    return {"status": "AI CRM Backend is Live!"}

@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    try:
        # User input ko agent ke format mein convert karna
        inputs = {"messages": [HumanMessage(content=request.message)]}
        
        # Agent ko run karna
        result = app_agent.invoke(inputs)
        
        # Jawab nikalna
        final_answer = result["messages"][-1].content
        return {"response": final_answer}
    except Exception as e:
        # Ye line terminal mein asli error print karegi
        print(f"ASLI ERROR YE HAI: {str(e)}") 
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/interactions", response_model=List[InteractionResponse])
def get_all_interactions():
    """Database se saari interactions fetch karta hai."""
    db = SessionLocal()
    interactions = db.query(Interaction).order_by(Interaction.id.desc()).all()
    return interactions

# main.py mein endpoints ke pass add karo
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(request: LoginRequest):
    # Abhi ke liye simple hardcoded check
    if request.username == "admin" and request.password == "admin123":
        return {"status": "success", "token": "fake-jwt-token"}
    raise HTTPException(status_code=401, detail="Invalid Credentials")