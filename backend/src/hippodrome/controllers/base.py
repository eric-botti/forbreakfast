from json import JSONDecodeError
from typing import Type, List
import json

from pydantic import BaseModel, ValidationError

from hippodrome.output_formats import OutputFormatModel
from hippodrome.message import Message, AgentMessage
from hippodrome.data_collection import save


class BaseController(BaseModel):
    """
    The interface that controllers use to receive info from and interact with the game.
    This is the base class and should not be used directly.
    """

    agent_id: str
    """The id of the agent."""
    game_id: str
    """The id of the game the agent is in."""

    log_messages: bool = True
    """Whether to log messages or not."""
    messages: List[Message] = []
    """The message history of the agent."""
    is_human: bool = False
    """Whether the agent is human or not."""

    @property
    def is_ai(self):
        return not self.is_human

    async def add_message(self, message: Message):
        """Adds a message to the message history, without generating a response."""
        self.messages.append(message)

    # Respond To methods - These take a message as input and generate a response

    async def respond_to(self, message: Message) -> Message:
        """Take a message as input and return a response. Both the message and the response are added to history."""
        await self.add_message(message)
        save(AgentMessage.from_message(message, [self.agent_id], self.game_id))
        response = await self.generate_response()
        return response

    async def respond_to_formatted(
        self,
        message: Message,
        output_format: Type[OutputFormatModel],
        additional_fields: dict = None,
        **kwargs,
    ) -> OutputFormatModel:
        """Responds to a message and logs the response."""
        await self.add_message(message)
        output = await self.generate_formatted_response(
            output_format, additional_fields, **kwargs
        )
        return output

    # Generate response methods - These do not take a message as input and only use the current message history

    async def generate_response(self) -> Message | None:
        """Generates a response based on the current messages in the history."""
        content = await self._generate()
        if content:
            response = Message(
                sender=self.agent_id,
                type="agent",
                content=content,
                # choice_idx=choice_idx,
            )
            await self.add_message(response)
            save(AgentMessage.from_message(response, [self.agent_id], self.game_id))
            return response
        else:
            return None

    async def generate_formatted_response(
        self,
        output_format: Type[OutputFormatModel],
        additional_fields: dict = None,
        max_retries=3,
    ) -> OutputFormatModel:
        """Generates a response matching the provided format."""
        initial_response = await self.generate_response()

        reformat_message = Message(
            type="format", content=output_format.get_format_instructions()
        )

        output = None
        retries = 0

        while not output:
            try:
                formatted_response = await self.respond_to(reformat_message)

                fields = json.loads(formatted_response.content)
                if additional_fields:
                    fields.update(additional_fields)

                output = output_format.model_validate(fields)

            except ValidationError as e:
                # If the response doesn't match the format, we ask the agent to try again
                if retries > max_retries:
                    raise e

                retry_message = Message(
                    type="retry",
                    content=f"Error formatting response: {e} \n\n Please try again.",
                )
                reformat_message = retry_message

                retries += 1

            except JSONDecodeError as e:
                # Occasionally models will output json as a code block, which will cause a JSONDecodeError
                if retries > max_retries:
                    raise e

                retry_message = Message(
                    type="retry",
                    content="There was an Error with your JSON format. Make sure you are not using code blocks."
                    "i.e. your response should be:\n{...}\n"
                    "Instead of:\n```json\n{...}\n```\n\n Please try again.",
                )
                reformat_message = retry_message

                retries += 1

        return output

    async def _generate(self) -> str:
        """Generates a response from the Agent."""
        # This is the BaseAgent class, and thus has no response logic
        # Subclasses should implement this method to generate a response using the message history
        raise NotImplementedError
