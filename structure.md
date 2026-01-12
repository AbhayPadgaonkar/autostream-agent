autostream_agent/
├── data/
│   └── knowledge_base.json    # Pricing and policy data
├── src/
│   ├── __init__.py
│   ├── config.py              # LLM setup and API keys
│   ├── state.py               # Type definitions for State
│   ├── utils.py               # RAG loader and Mock Tool
│   ├── nodes.py               # The core logic functions (Classifier, RAG, etc.)
│   └── graph.py               # LangGraph workflow construction
├── main.py                    # Entry point to run the agent
├── requirements.txt
└── README.md