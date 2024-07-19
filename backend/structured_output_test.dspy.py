from typing import Literal, Annotated, Type, List

import dspy
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from pydantic import StringConstraints

from pydantic import BaseModel, Field, field_validator

from dspy import TypedPredictor, Signature, InputField, OutputField

gpt3_turbo = dspy.OpenAI(model='gpt-3.5-turbo-1106')
haiku = dspy.Claude(model='claude-3-haiku-20240307')
dspy.configure(lm=haiku)


def chain_of_thought_model(output_model: Type[BaseModel]):

    class ChainOfThoughtModel(BaseModel):
        reasoning: str = Field(..., description="Step by step thoughts about the prompt before responding.")
        final_answer: output_model = Field(..., description="The final answer to the prompt.")

    return ChainOfThoughtModel




response_description = """\
1. Raise your sword and prepare to attack the giga troll.
2. Run away from the giga troll.
3. Stand your ground and prepare to defend yourself.
4. Try to reason with the giga troll.
"""

class BattleResponse(BaseModel):
    response: int = Field(..., description=response_description)


Response = chain_of_thought_model(BattleResponse)


class BattleSignature(Signature):
    """Choose your next action in a boss battle."""
    messages: List[dict] = InputField()
    response: Response = OutputField()


llm = TypedPredictor(BattleSignature, max_retries=3)

prompt = "You are fighting a giga troll as a boss battle. The giga troll raises it's ugly head and roars at you. What do you do?"

messages = [
    {"sender": "Damian", "content": "I cast enrage on the giga troll, lowering its defense."},
    {"sender": "Game Master", "content": "Damian successfully lowers the giga troll's defense! It's your turn, the Giga troll raises it's ugly head and roars at you. What do you do?"},
]


x = llm(messages=messages)



print(x)

def generate_response(prompt, choices: list[str] = None):
    if choices:
        response_description = "\n".join([f"{i + 1}. {choice}" for i, choice in enumerate(choices)])

        class ResponseFormat(BaseModel):
            response: int = Field(..., description=response_description)

    else:
        response_description = "Choose your response."



    class GameSignature(Signature):
        """Take your next action in the game."""
        prompt = InputField()
        response: ResponseFormat = OutputField()


    llm = TypedPredictor(GameSignature, max_retries=3)

    return llm(prompt=prompt)