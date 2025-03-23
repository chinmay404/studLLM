import os
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from .helpers.get_llm import LLM
from .tools.tools import tools_list
from .helpers.load_prompt import load_prompt_from_yaml
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage
from langgraph.prebuilt import create_react_agent
from typing_extensions import TypedDict
import random
from typing import Literal, Annotated
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tool_node, tools_condition, tool_validator, ToolNode
from langgraph.checkpoint.memory import MemorySaver
from .helpers.load_prompt import load_prompt_from_yaml
from DB_ops.main import MongoCRUD

db = MongoCRUD()

class State(MessagesState):
    pass


class getGraphResponse():
    def __init__(self):
        self.llm = LLM.get_groq_llm()
        self.memory = MemorySaver()
        self.llm_with_tools = self.llm.bind_tools(tools_list)
        self.state = State()
        self.graph = self.build_graph()
        self.sys_msg = load_prompt_from_yaml("REACT_LANGGRAPH_PROMPT")

    def get_nodes(self):
        def assistant(state: MessagesState) -> AnyMessage:
            return {"messages": [self.llm_with_tools.invoke([self.sys_msg] + state["messages"])]}
        return [assistant]

    def build_graph(self):
        nodes = self.get_nodes()
        builder = StateGraph(MessagesState)
        builder.add_node("assistant", nodes[0])
        builder.add_node("tools", ToolNode(tools_list))

        builder.add_edge(START, "assistant")
        builder.add_conditional_edges("assistant", tools_condition)
        builder.add_edge("tools", "assistant")
        graph = builder.compile(checkpointer=self.memory)
        return graph

    def get_response(self, query: str, config: dict , user_id: str):
        user_current_state = db.get_user_state(user_id)
        human_message = [HumanMessage(content=query + "USER ID : " + user_id + "User Current State" + str(user_current_state))]
        res = self.graph.invoke({"messages": human_message}, config)
        messages = res.get("messages", [])
        for msg in reversed(messages):
            if hasattr(msg, 'content') and msg.content:
                final_message = msg.content
                break
        
            # elif msg.__class__.__name__ == "AIMessage":
            #     last_ai_message = msg.content
            #     break
        if final_message:
            return  final_message
        else:
            return None



# graph = getGraphResponse()
# while True:
#     query = input("Enter your query: ")
#     response = graph.get_response(query)
#     print(response.content)
#     print("")
