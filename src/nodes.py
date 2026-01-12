import json
from langchain_core.messages import SystemMessage, AIMessage
from src.state import AgentState
from src.config import llm
from src.utils import retrieve_knowledge, mock_lead_capture

def intent_classifier(state: AgentState):
    """Classifies user intent: greeting, inquiry, or lead."""
    messages = state['messages']
    
    prompt = """
    You are an intent classifier for AutoStream (a video editing SaaS).
    Classify the user's message into exactly one of these three categories:
    1. "greeting" (Casual hellos)
    2. "inquiry" (Questions about pricing, features, policies)
    3. "lead" (High intent, wants to buy, try, or sign up)
    
    Output ONLY the category name.
    """
    
    response = llm.invoke([SystemMessage(content=prompt)] + messages[-1:])
    intent = response.content.strip().lower()
    
    # Normalization logic
    if "lead" in intent: intent = "lead"
    elif "inquiry" in intent or "pricing" in intent: intent = "inquiry"
    else: intent = "greeting"
    
    return {"intent": intent}

def generic_responder(state: AgentState):
    """Handles casual greetings."""
    return {"messages": [AIMessage(content="Hi there! I'm the AutoStream assistant. How can I help you edit your videos today?")]}

def rag_node(state: AgentState):
    """RAG: Retrieves pricing/policy info to answer questions."""
    messages = state['messages']
    context = retrieve_knowledge()
    
    prompt = f"""
    You are a helpful assistant for AutoStream. 
    Use the following CONTEXT to answer the user's question accurately.
    
    CONTEXT:
    {context}
    
    If the answer is not in the context, politely say you don't know.
    """
    
    response = llm.invoke([SystemMessage(content=prompt)] + messages)
    return {"messages": [response]}

def lead_capture_node(state: AgentState):
    """
    Extracts slots (Name, Email, Platform). 
    If complete -> Calls Tool. 
    If incomplete -> Asks User.
    """
    messages = state['messages']
    current_info = state.get("user_info", {}) or {}
    
    # 1. Extraction Step
    extraction_prompt = f"""
    Analyze the conversation history. Extract the following user details if present:
    - Name
    - Email
    - Platform (e.g., YouTube, Instagram)
    
    Return a JSON object with keys: "name", "email", "platform". 
    If a value is missing, set it to null.
    
    Current known info: {json.dumps(current_info)}
    """
    
    extraction_response = llm.invoke([SystemMessage(content=extraction_prompt)] + messages)
    
    try:
        # Simple cleanup to ensure JSON parsing
        content = extraction_response.content.replace("```json", "").replace("```", "")
        extracted_data = json.loads(content)
        
        # Update current info with newly found data
        for k, v in extracted_data.items():
            if v: current_info[k] = v
    except Exception:
        pass 

    # 2. Validation Step
    missing = []
    if not current_info.get("name"): missing.append("Name")
    if not current_info.get("email"): missing.append("Email")
    if not current_info.get("platform"): missing.append("Creator Platform")

    if not missing:
        # Success: Run Tool
        mock_lead_capture(current_info['name'], current_info['email'], current_info['platform'])
        return {
            "messages": [AIMessage(content="Thanks! I've secured your spot. Our team will reach out shortly.")],
            "user_info": current_info
        }
    else:
        # Failure: Ask for missing details
        ask_msg = f"That sounds great! To set you up, I just need your {', '.join(missing)}."
        return {
            "messages": [AIMessage(content=ask_msg)], 
            "user_info": current_info
        }