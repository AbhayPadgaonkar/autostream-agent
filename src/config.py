import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load .env variables
load_dotenv()

# Initialize the LLM once here to be imported elsewhere
# Using Gemini 1.5 Flash as allowed by requirements
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)