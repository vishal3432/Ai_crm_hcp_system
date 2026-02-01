from langchain_core.tools import tool
from database import SessionLocal, Interaction
from typing import Annotated
import datetime

@tool
def log_interaction_tool(
    hcp_name: Annotated[str, "The full name of the Healthcare Professional (Doctor)"],
    product: Annotated[str, "The name of the medicine or product discussed"],
    summary: Annotated[str, "A brief summary of the conversation"]
):
    """Logs a new interaction with a doctor in the CRM database."""
    db = SessionLocal()
    try:
        new_entry = Interaction(hcp_name=hcp_name, product=product, summary=summary)
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return f"Success! Interaction logged for {hcp_name} (ID: {new_entry.id})."
    except Exception as e:
        return f"Error logging interaction: {str(e)}"
    finally:
        db.close()

@tool
def edit_interaction_tool(
    interaction_id: Annotated[int, "The unique ID of the interaction to edit"],
    new_summary: Annotated[str, "The updated summary text"]
):
    """Edits an existing interaction summary using its ID."""
    db = SessionLocal()
    try:
        entry = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if entry:
            entry.summary = new_summary
            db.commit()
            return f"Update successful for Interaction ID {interaction_id}."
        return "Error: Interaction ID not found."
    finally:
        db.close()

@tool
def appointment_scheduler_tool(
    hcp_name: Annotated[str, "Name of the doctor for the appointment"],
    date: Annotated[str, "Scheduled date in YYYY-MM-DD format only"]
):
    """
    Schedules a follow-up appointment. 
    Use this when the user mentions a future date or meeting.
    """
    return f"Appointment confirmed with {hcp_name} for {date}. Added to calendar."

@tool
def hcp_insights_tool(
    hcp_name: Annotated[str, "The doctor's name to search for in history"]
):
    """Retrieves previous interaction history for a specific doctor."""
    db = SessionLocal()
    try:
        history = db.query(Interaction).filter(Interaction.hcp_name.ilike(f"%{hcp_name}%")).all()
        if history:
            return [f"{h.created_at}: {h.summary}" for h in history]
        return f"No previous records found for {hcp_name}."
    finally:
        db.close()

@tool
def sample_inventory_tool(
    product_name: Annotated[str, "Name of the medicine to check stock for"]
):
    """Checks the current stock levels for a specific medicine sample."""
    inventory = {"Vaccine A": 45, "Drug X": 10, "Llama-Cure": 100}
    count = inventory.get(product_name, 0)
    return f"Current stock for {product_name}: {count} units."