import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated, Sequence
# SystemMessage import karna zaroori hai
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage 
from tools import log_interaction_tool, edit_interaction_tool, appointment_scheduler_tool, hcp_insights_tool, sample_inventory_tool
from datetime import datetime

load_dotenv()

# Tool setup
tools = [log_interaction_tool, edit_interaction_tool, appointment_scheduler_tool, hcp_insights_tool, sample_inventory_tool]
tool_node = ToolNode(tools)

# LLM setup
llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.1-8b-instant", 
    groq_api_key=os.getenv("GROQ_API_KEY")
).bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "Conversation history"]

# --- YAHAN SE CHANGES HAIN ---

def call_model(state: AgentState):
    # 1. Aaj ki sahi date nikalna
    today = datetime.now()
    current_date = today.strftime("%A, %B %d, %Y") # Example: Sunday, February 01, 2026
    
    # 2. AI ko context dena (Grounding)
    system_prompt = SystemMessage(content=f"""
    You are an AI CRM Agent for Healthcare Professionals (HCPs).
    Your primary goal is to help sales reps log visits, schedule appointments, and manage inventory.
    
    IMPORTANT CONTEXT:
    - Today's date is {current_date}.
    - When the user mentions relative dates like 'tomorrow', 'next week', or 'next Thursday', 
      calculate the exact YYYY-MM-DD date based on {current_date}.
    - If a tool call fails, double-check your date calculations.
    """)
    
    # 3. System prompt ko messages ke shuruat mein joḍna
    messages_with_context = [system_prompt] + list(state['messages'])
    
    # 4. LLM call
    response = llm.invoke(messages_with_context)
    return {"messages": [response]}

# --- CHANGES KHATAM ---

def should_continue(state: AgentState):
    last_msg = state['messages'][-1]
    if last_msg.tool_calls:
        return "tools"
    return END

# Workflow Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app_agent = workflow.compile()