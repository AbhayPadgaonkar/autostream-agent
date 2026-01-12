# AutoStream Social-to-Lead Agent

This project is a Conversational AI Agent designed for **AutoStream**, a SaaS video editing platform. Built as part of the ServiceHive Machine Learning Internship assignment, this agent acts as a first-line support and sales representative.

It is capable of answering pricing queries using RAG (Retrieval Augmented Generation), detecting high-intent leads, and intelligently collecting user details to trigger backend workflows.

## 🚀 Features
* **Intent Recognition:** Distinguishes between casual greetings, product inquiries, and high-intent leads.
* **RAG-Powered Knowledge:** Retrieves accurate pricing and policy data from a local knowledge base.
* **Lead Qualification:** intelligently asks for missing details (Name, Email, Platform) before processing a lead.
* **Tool Execution:** triggers a mock CRM update only when all necessary data is collected.

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Orchestration:** LangGraph (Stateful Agentic Workflow)
* **LLM:** Google Gemini 1.5 Flash
* **Environment:** Dotenv for secure key management

---

## 🏃 How to Run Locally

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd autostream_agent
    ```

2.  **Set up Environment Variables**
    Create a `.env` file in the root directory and add your API key:
    ```
    GOOGLE_API_KEY=your_google_api_key_here
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Agent**
    ```bash
    python main.py
    ```

---

## 🏗️ Architecture Explanation

**Why LangGraph?**
I chose **LangGraph** over standard LangChain chains or AutoGen because the problem statement requires a **stateful, cyclic workflow**. A linear chain is insufficient for lead capture, where the agent might need to loop back multiple times to ask for missing information (e.g., if the user provides their name but forgets their email).

LangGraph allows us to treat the conversation as a graph where nodes represent actions (Classification, RAG, Lead Processing) and edges represent the flow. This architecture provides distinct advantages:
1.  **Cyclic State Management:** If the `Lead Handler` node detects missing slots (e.g., missing email), it updates the state and loops back to the user, maintaining context without resetting the conversation flow.
2.  **Explicit Control:** We can define strict "Conditional Edges" (routers) that prevent the agent from hallucinating tool calls. The agent *cannot* reach the tool execution node unless the intent classifier explicitly routes it there.
3.  **Memory Persistence:** The `AgentState` dictionary persists conversation history and extracted user data (`user_info`) across turns, ensuring the agent "remembers" the user's name even after answering a pricing question.

## 📱 WhatsApp Deployment Strategy

To integrate this agent with WhatsApp, I would use the **Meta Cloud API** (or a provider like Twilio) combined with a webhook server.

**Implementation Steps:**
1.  **Webhook Endpoint:** I would wrap the LangGraph entry point (`app.invoke`) inside a **FastAPI** or **Flask** route (e.g., `POST /webhook`).
2.  **Session Management:** WhatsApp identifies users by phone number (`WaId`). I would use this `WaId` as the unique `thread_id` in LangGraph's checkpointer. This ensures that concurrent users have isolated conversation states.
3.  **Payload Handling:**
    * **Receive:** The FastAPI server receives the JSON payload from Meta, extracts the user's text message, and passes it to the graph.
    * **Process:** The Agent processes the text (classifying intent, running RAG, etc.).
    * **Respond:** The final text output from the Agent is sent back to the user via a POST request to the `https://graph.facebook.com/v17.0/{phone_number_id}/messages` endpoint.
