from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from utils.render_graph import render_graph
from state.agent_state import AgentState

from agents.agent_1_main_action import build_custom_agent_1
from agents.agent_2_sub_actions import build_custom_agent_2
from agents.agent_3_involved_partners import build_custom_agent_3
from agents.agent_4_goals_milestones import build_custom_agent_4
from agents.agent_5_timeline import build_custom_agent_5
from agents.agent_6_cost_budget import build_custom_agent_6
from agents.agent_7_mer import build_custom_agent_7
from agents.agent_8_sgds import build_custom_agent_8
from agents.agent_combine import custom_agent_combine

from tools.tools import document_retriever_tool, search, placeholder_tool

# 1. Brazil_NDC_November2024.pdf
#    - Document Name: Brazil's Nationally Determined Contribution (NDC) to the Paris Agreement
#    - Content: This document outlines Brazil's climate action plan strategy.

# 2. Green_Cities_Brazil.pdf
#    - Document Name: Green Cities: Cities and Climate Change in Brazil
#    - Content: This report from the World Bank discusses opportunities for mitigating urban greenhouse gas emissions in sectors like transport, land use, energy efficiency, waste management, and urban forestry in Brazil.

# Both documents are limited in scope to Brazil's climate action plan and its implementation.


# Create the agents
model = ChatOpenAI(model="gpt-4o", temperature=0.0, seed=42)

placeholder_tools = [placeholder_tool]


agent_1 = build_custom_agent_1(model, [document_retriever_tool])
agent_2 = build_custom_agent_2(model, placeholder_tools)
agent_3 = build_custom_agent_3(
    model, [search]
)  # for debugging purposes, 'search' tool is not provided to save on API calls. Add [search] to the list of tools to enable search tool.
agent_4 = build_custom_agent_4(model, placeholder_tools)
agent_5 = build_custom_agent_5(model, placeholder_tools)
agent_6 = build_custom_agent_6(model, placeholder_tools)
agent_7 = build_custom_agent_7(model, placeholder_tools)
agent_8 = build_custom_agent_8(model, placeholder_tools)
agent_combine = custom_agent_combine


def create_graph():
    # Build the graph
    builder = StateGraph(AgentState)
    builder.add_node("agent_1", agent_1)
    builder.add_node("agent_2", agent_2)
    builder.add_node("agent_3", agent_3)
    builder.add_node("agent_4", agent_4)
    builder.add_node("agent_5", agent_5)
    builder.add_node("agent_6", agent_6)
    builder.add_node("agent_7", agent_7)
    builder.add_node("agent_8", agent_8)
    builder.add_node("agent_combine", agent_combine)

    # Define the edges
    builder.add_edge(START, "agent_1")
    builder.add_edge("agent_1", END)
    # builder.add_edge("agent_1", "agent_2")
    # builder.add_edge("agent_2", "agent_3")
    # builder.add_edge("agent_3", "agent_4")
    # builder.add_edge("agent_4", "agent_5")
    # builder.add_edge("agent_5", "agent_6")
    # builder.add_edge("agent_6", "agent_7")
    # builder.add_edge("agent_7", "agent_8")
    # builder.add_edge("agent_8", "agent_combine")
    # builder.add_edge("agent_combine", END)

    # Compile the graph
    compiled_graph = builder.compile()

    render_graph(compiled_graph)

    return compiled_graph
