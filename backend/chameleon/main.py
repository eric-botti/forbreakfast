import asyncio
import os
import logging
import random

from markdown_it import MarkdownIt

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

# Setup the Game
from chameleon_game import ChameleonGame
from hippodrome.controllers.human.base import BaseHumanController
from hippodrome import Message


import openai

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()
md = MarkdownIt()

@app.get("/")
def get():
    """A simple UI for testing the chatbot."""
    html_path = os.path.join("backend", "chameleon", "index.html")

    with open(html_path) as f:
        html = f.read()

    return HTMLResponse(html)

@app.get("/openai_test/")
def openai_test():
    """Test call to OpenAI API."""
    client = openai.Client()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the meaning of life?"},
        ],
    )

    return response.json()


class FastAPIHumanController(BaseHumanController):
    # Set arbitrary_types_allowed=True to allow for the use of the WebSocket class
    class Config:
        arbitrary_types_allowed = True

    websocket: WebSocket = None

    async def add_message(self, message: Message):
        if message.type not in ["agent", "system"]:
            html = md.render(message.content)
            # Tailwind CSS classes for lists
            html = html.replace("<ul>", "<ul class='list-disc list-inside space-y-1'>")
            html = html.replace("<ol>", "<ol class='list-decimal list-inside space-y-1'>")

            await self.websocket.send_json(
                {"sender": message.sender, "content": html}
            )

    async def _generate(self) -> str:
        player_message = await self.websocket.receive_json()
        logger.info(f"Received data: {player_message}")

        user_input = player_message["message"]["content"]
        return user_input


def setup_game(player_name: str, websocket: WebSocket):
    """Set up the game."""
    game = ChameleonGame.from_human_name(player_name, FastAPIHumanController)

    # This feels like cheating...
    game.player_from_name(player_name).controller.websocket = websocket
    # human_player_index = next(i for i, player in enumerate(game.players) if player.name == player_name)

    # game.players[human_player_index] = human_player

    return game


@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established.")

    game = setup_game("Hugh", websocket)

    await game.run_game()
