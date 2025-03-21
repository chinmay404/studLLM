import os
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from helpers.get_llm import LLM
from tools.tools import tools_list
from helpers.load_prompt import load_prompt_from_yaml
from tools.state_tool import get_user_state_
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from typing_extensions import TypedDict
import random
from typing import Literal
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END



llm = LLM.get_groq_llm()



class State(TypedDict):
    graph_state: str
    
    
def node_1(state):
    print("---Node 1---")
    return {"graph_state": state['graph_state'] +" I am"}

def node_2(state):
    print("---Node 2---")
    return {"graph_state": state['graph_state'] +" happy!"}

def node_3(state):
    print("---Node 3---")
    return {"graph_state": state['graph_state'] +" sad!"}





def decide_mood(state) -> Literal["node_2", "node_3"]:
    user_input = state['graph_state'] 
    if random.random() < 0.5:
        return "node_2"
    return "node_3"




builder = StateGraph(State)


# Adding Nodes
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)


# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1" , decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)


#Add
graph = builder.compile()


# display(Image(graph.get_graph().draw_mermaid_png()))

op = graph.invoke({"graph_state": "Hi Im Chinmay"})


print("Final State:",op)
