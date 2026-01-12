import json
import os

# Define the path to the data file relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'knowledge_base.json')

def retrieve_knowledge() -> str:
    """Reads the JSON knowledge base."""
    try:
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
        return json.dumps(data, indent=2)
    except FileNotFoundError:
        return "Error: Knowledge base file not found."

def mock_lead_capture(name: str, email: str, platform: str):
    """Simulates sending lead data to a backend CRM."""
    print(f"\n[SYSTEM TOOL] Lead captured successfully: {name}, {email}, {platform}\n")
    return "Lead processed."