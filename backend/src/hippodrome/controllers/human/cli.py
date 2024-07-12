from hippodrome.controllers import BaseHumanController

from colorama import Fore, Style
from hippodrome.message import Message


class HumanCLIController(BaseHumanController):
    """A Human agent that uses the command line interface to generate responses."""
    async def add_message(self, message: Message):
        await super().add_message(message)
        if message.type == "verbose":
            print(Fore.GREEN + message.content + Style.RESET_ALL)
        elif message.type == "debug":
            print(Fore.YELLOW + "DEBUG: " + message.content + Style.RESET_ALL)
        elif message.type != "agent":
            # Prevents the agent from seeing its own messages on the command line
            print(message.content)

    async def _generate(self) -> str:
        """Generates a response using the message history"""
        response = input()
        return response
