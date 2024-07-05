import logging

from fastapi import WebSocket
from hippodrome.controllers.human.base import BaseHumanController
from hippodrome import Message

from markdown_it import MarkdownIt

md = MarkdownIt()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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