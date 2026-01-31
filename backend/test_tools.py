from agent import app_agent
from langchain_core.messages import HumanMessage

inputs = {"messages": [HumanMessage(content="I met Dr. Sharma today and discussed Vaccine A. He was very impressed.")]}
for output in app_agent.stream(inputs):
    for key, value in output.items():
        print(f"Output from node '{key}':")
        print(value)