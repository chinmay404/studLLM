import os
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from .helpers.get_llm import LLM
from .tools.tools import tools_list
from .helpers.load_prompt import load_prompt_from_yaml
from .tools.state_tool import get_user_state_
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage , AnyMessage
from langgraph.prebuilt import create_react_agent
from typing_extensions import TypedDict
import random
from typing import Literal , Annotated
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tool_node , tools_condition , tool_validator , ToolNode



class State(TypedDict):
    graph_state: str
    

class getGraphResponse():
    def __init__(self ):
        self.llm = LLM.get_groq_llm()
        self.llm_with_tools = self.llm.bind_tools(tools_list)
        self.state = State()
        self.graph = self.build_graph()    
    
    def get_nodes(self):
        def assistant(state):
            print(state['graph_state'])
            return {"graph_state": self.llm_with_tools.invoke([HumanMessage(content=state['graph_state'])].content)}
        return [assistant]
    
    def build_graph(self):
        nodes = self.get_nodes()
        builder = StateGraph(State)
        builder.add_node("assistant", nodes[0])
        builder.add_node("tools", ToolNode(tools_list))

        
        
        builder.add_edge(START, "assistant")
        builder.add_conditional_edges("assistant",tools_condition)
        builder.add_edge("tools" , "assistant")
        graph = builder.compile()
        return graph
    
    def get_response(self , query : str):
        return self.llm.invoke([HumanMessage(content=query)] , self.state)
    
    
    
# graph = getGraphResponse()
# while True:
#     query = input("Enter your query: ")
#     response = graph.get_response(query)
#     print(response.content)
#     print("")