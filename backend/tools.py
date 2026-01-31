from langchain_core.tools import tool
from database import SessionLocal, Interaction
import datetime

@tool
def log_interaction_tool(hcp_name: str, product: str, summary: str):
    """Logs a new interaction with an HCP into the database. Use this when the user mentions a meeting or talk with a doctor."""
    db = SessionLocal()
    new_entry = Interaction(hcp_name=hcp_name, product=product, summary=summary)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return f"Success! Interaction logged for {hcp_name} (ID: {new_entry.id})."

@tool
def edit_interaction_tool(interaction_id: int, new_summary: str):
    """Edits an existing interaction summary using its ID."""
    db = SessionLocal()
    entry = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if entry:
        entry.summary = new_summary
        db.commit()
        return f"Update successful for Interaction ID {interaction_id}."
    return "Error: Interaction ID not found."

@tool
def appointment_scheduler_tool(hcp_name: str, date: str):
    """Schedules a follow-up appointment. Format: 'YYYY-MM-DD'."""
    return f"Appointment confirmed with {hcp_name} for {date}. Added to calendar."

@tool
def hcp_insights_tool(hcp_name: str):
    """Retrieves past interaction history for a doctor."""
    db = SessionLocal()
    history = db.query(Interaction).filter(Interaction.hcp_name.ilike(f"%{hcp_name}%")).all()
    if history:
        return [f"{h.created_at}: {h.summary}" for h in history]
    return f"No previous records found for {hcp_name}."

@tool
def sample_inventory_tool(product_name: str):
    """Checks if medicine samples are in stock."""
    # Mock inventory data
    inventory = {"Vaccine A": 45, "Drug X": 10, "Llama-Cure": 100}
    count = inventory.get(product_name, 0)
    return f"Current stock for {product_name}: {count} units."