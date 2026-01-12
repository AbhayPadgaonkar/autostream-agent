from langchain_core.messages import HumanMessage
from src.graph import app

def run_chat():
    print("--- AutoStream AI Agent Started (Modular Version) ---")
    print("Type 'quit' to exit.")
    
    # Initialize blank state
    state_input = {"messages": [], "user_info": {}}
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["quit", "exit"]: 
                break
            
            # Append user message to history
            state_input["messages"].append(HumanMessage(content=user_input))
            
            # Invoke Graph
            result = app.invoke(state_input)
            
            # Update local state variable to maintain memory for next loop
            state_input = result
            
            # Output response
            print(f"Agent: {result['messages'][-1].content}")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    run_chat()