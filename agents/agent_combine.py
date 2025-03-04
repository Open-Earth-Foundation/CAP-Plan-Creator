from state.agent_state import AgentState
from pathlib import Path
from datetime import datetime

OUTPUT_PATH = Path(__file__).parent.parent / "data" / "output"


def custom_agent_combine(state: AgentState) -> AgentState:

    response_agent_1 = state["response_agent_1"].content
    response_agent_2 = state["response_agent_2"].content
    response_agent_3 = state["response_agent_3"].content
    response_agent_4 = state["response_agent_4"].content
    response_agent_5 = state["response_agent_5"].content
    response_agent_6 = state["response_agent_6"].content
    response_agent_7 = state["response_agent_7"].content
    response_agent_8 = state["response_agent_8"].content

    # Create a new dictionary based on the existing state
    result_state = AgentState(state)

    # Concatenate the responses (all in Markdown) into one big Markdown string
    combined_markdown = (
        f"{response_agent_1}\n\n"
        f"{response_agent_2}\n\n"
        f"{response_agent_3}\n\n"
        f"{response_agent_4}\n\n"
        f"{response_agent_5}\n\n"
        f"{response_agent_6}\n\n"
        f"{response_agent_7}\n\n"
        f"{response_agent_8}"
    )

    # Store the combined Markdown response under a new key
    result_state["response_agent_combine"] = combined_markdown

    # File output
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    # Get current date/time in hh:mm format
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")

    file_name = f"{current_time}_climate_action_implementation_plan.md"

    # Write the combined Markdown text to a local file (e.g. "combined_responses.md")
    with open(OUTPUT_PATH / file_name, "w", encoding="utf-8") as md_file:
        md_file.write(combined_markdown)

    # Return an AgentState with the updated responses
    return AgentState(**result_state)
