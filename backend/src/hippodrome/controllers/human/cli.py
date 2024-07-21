from hippodrome.controllers import BaseHumanController

from colorama import Fore, Style
from hippodrome.message import Message


def multiple_choice(choices) -> tuple[str, int]:
    """
    Displays a multiple choice question and returns the user's choice.

    :param choices: list of str - The possible answers to choose from
    :return: str - The user's chosen answer
    """
    # Print the choices with corresponding numbers
    for idx, choice in enumerate(choices, start=1):
        print(f"{idx}. {choice}")

    # Get the user's choice
    while True:
        try:
            # Ask the user to choose a number
            user_input = input("Enter the number of your choice: ")
            # Convert the input to an integer
            user_choice = int(user_input)
            # Check if the choice is within the valid range
            if 1 <= user_choice <= len(choices):
                # Return the chosen option
                choice_idx = user_choice - 1

                return choices[choice_idx], choice_idx
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")


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
        last_message = self.messages[-1]

        if last_message.choices:
            response, choice_idx = multiple_choice(last_message.choices)
        else:
            response = input()
            choice_idx = None

        return response, choice_idx
