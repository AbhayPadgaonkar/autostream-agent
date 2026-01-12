import operator
from typing import Annotated, List, TypedDict, Dict, Any
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    # 'operator.add' ensures new messages are appended to the history, not overwritten
    messages: Annotated[List[BaseMessage], operator.add]
    intent: str
    user_info: Dict[str, Any]  # Stores {name, email, platform}