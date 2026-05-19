from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage

llm = OllamaLLM(model="llama3.2:1b")

# Simple chain - give it a task
response = llm.invoke("""
You are a research assistant. I need you to:
1. Find information about exoplanets
2. Summarize the key points
3. Suggest next steps for research

Please complete these tasks step by step.
""")

print(response)