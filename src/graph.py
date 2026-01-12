from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes import (
    intent_classifier, 
    generic_responder, 
    rag_node, 
    lead_capture_node
)

# Define Router Logic
def router(state: AgentState):
    intent = state['intent']
    if intent == "greeting": return "greeting_handler"
    elif intent == "inquiry": return "inquiry_handler"
    else: return "lead_handler"

# Build Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("classifier", intent_classifier)
workflow.add_node("greeting_handler", generic_responder)
workflow.add_node("inquiry_handler", rag_node)
workflow.add_node("lead_handler", lead_capture_node)

# Set Entry Point
workflow.set_entry_point("classifier")

# Add Conditional Edges
workflow.add_conditional_edges(
    "classifier", 
    router,
    {
        "greeting_handler": "greeting_handler",
        "inquiry_handler": "inquiry_handler",
        "lead_handler": "lead_handler"
    }
)

# Add Edges to END
workflow.add_edge("greeting_handler", END)
workflow.add_edge("inquiry_handler", END)
workflow.add_edge("lead_handler", END)

# Compile
app = workflow.compile()