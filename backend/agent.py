import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from typing import TypedDict

load_dotenv()

class AgentState(TypedDict):
    user_input: str
    extracted_data: dict

# Model: Gemma-2-9b-it (Fastest on Groq)
llm = ChatGroq(temperature=0, model_name="gemma2-9b-it", groq_api_key=os.getenv("GROQ_API_KEY"))

def extract_info(state: AgentState):
    prompt = f"Extract Doctor Name and Medicine from this text: {state['user_input']}. Return only JSON."
    response = llm.invoke(prompt)
    return {"extracted_data": {"raw": response.content}}

workflow = StateGraph(AgentState)
workflow.add_node("extract", extract_info)
workflow.set_entry_point("extract")
workflow.add_edge("extract", END)

app_agent = workflow.compile()