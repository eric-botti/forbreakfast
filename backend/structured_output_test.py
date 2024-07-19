from typing import Literal, Annotated, Type

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from pydantic import StringConstraints
from langchain_core.pydantic_v1 import BaseModel, Field, validator

from dotenv import load_dotenv
load_dotenv("local.env")

response_description = """\
Respond with the number of the action you would like to take:
1. Raise your sword and prepare to attack the giga troll.
2. Run away from the giga troll.
3. Stand your ground and prepare to defend yourself.
4. Try to reason with the giga troll.
"""


def chain_of_thought_model(output_model: Type[BaseModel]):

    class ChainOfThoughtModel(BaseModel):
        reasoning: str = Field(..., description="Think step by step about the prompt before responding.")
        response: str = Field(..., description="Your response to the prompt")

    return ChainOfThoughtModel




class BattleResponse(BaseModel):
    response: int = Field(..., description=response_description)


Response = chain_of_thought_model(BattleResponse)

llm = ChatAnthropic(model_name="claude-3-haiku-20240307")
# llm = ChatOpenAI(model="gpt-4o-mini")

structured_llm = llm.with_structured_output(Response)

x = structured_llm.invoke("You are fighting a giga troll as a boss battle. The giga troll raises it's ugly head and roars at you. What do you do?")

if isinstance(x, dict):
    x = Response(**x)

print("Reasoning:")
print(x.reasoning)
print("Response:")
print(x.response)