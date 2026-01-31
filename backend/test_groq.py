import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
llm = ChatGroq(model_name="llama-3.3-70b-versatile")

try:
    response = llm.invoke("Hello, are you working?")
    print("Success! AI Response:", response.content)
except Exception as e:
    print("Error aa gaya bhai:", e)