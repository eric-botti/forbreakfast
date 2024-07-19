from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv("local.env")


# Response Format
class Response(BaseModel):
    content: str


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

from langchain_openai import ChatOpenAI

llm = ChatOpenAI()


def reasoning_step(state: State):
    most_recent_message = state["messages"][-1]
    most_recent_message.content += "Think about your response step by step."

    return {"messages": [llm.invoke(state["messages"])]}


def final_response(state: State):
    structured_llm = llm.with_structured_output(Response)

    return {"messages": [structured_llm.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("reasoning", reasoning_step)
graph_builder.add_node("response", final_response)


graph_builder.add_edge(START, "reasoning")
graph_builder.add_edge("reasoning", "response")
graph_builder.add_edge("response", END)

memory = MemorySaver()

graph = graph_builder.compile(checkpointer=memory)

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": ("user", user_input)}, config={"configurable": {"thread_id": "test"}}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)