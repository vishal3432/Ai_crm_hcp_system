import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from tools import log_interaction_tool, edit_interaction_tool, appointment_scheduler_tool, hcp_insights_tool, sample_inventory_tool

load_dotenv()

# Tool setup
tools = [log_interaction_tool, edit_interaction_tool, appointment_scheduler_tool, hcp_insights_tool, sample_inventory_tool]
tool_node = ToolNode(tools)

# LLM setup (Llama 3.3 for 2026 performance)
llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.1-8b-instant", 
    groq_api_key=os.getenv("GROQ_API_KEY")
).bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "Conversation history"]

def call_model(state: AgentState):
    response = llm.invoke(state['messages'])
    return {"messages": [response]}

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