#!/usr/bin/env python
import sys
import warnings
from dotenv import load_dotenv
from mem0 import MemoryClient
import os
from crew import Studllm

load_dotenv()


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

client = MemoryClient(api_key=os.getenv('MEM0_API_KEY'))

def run(user_message: str, user_id: str):
    """
    Run the crew.
    """
    inputs = {
        'user_message': user_message,
        'user_state': "Landed in germany",
        'memory' : client.search(user_message, version="v2"),
        'context': client.get_all(version="v2", page=1, page_size=50),
    }
    print(inputs)
    Studllm().crew().kickoff(inputs=inputs)
print(run("Hello", "0"))

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         Studllm().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")


