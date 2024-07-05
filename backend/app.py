import asyncio
import os
import logging
import random
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from pydantic import BaseModel, Field


from chameleon.chameleon_game import ChameleonGame
from hippodrome.controllers.human.fastapi import FastAPIHumanController


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

games = {}


async def cleanup_games():
    while True:
        await asyncio.sleep(900)  # Run every 15 minutes
        for game_id, game in list(games.items()):
            if game["state"] == "disconnected":
                del games[game_id]
                logger.info(f"Cleaned up disconnected game: {game_id}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    cleanup_task = asyncio.create_task(cleanup_games())
    logger.info("Background cleanup task started")

    yield
    # Shutdown: cancel background task
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        logger.info("Background cleanup task cancelled")


app = FastAPI(lifespan=lifespan)


class PlayerName(BaseModel):
    player_name: str = Field(..., min_length=1, max_length=50)


@app.post("/api/game/create", response_model=Dict[str, str])
async def create_game(name: PlayerName):
    """Create a new game."""
    game = ChameleonGame.from_human_name(name.player_name, FastAPIHumanController)

    game_id = game.game_id

    games[game_id] = {
        "game": game,
        "state": "created",
        "human": name.player_name
    }

    return {"game_id": game_id}


@app.websocket("/api/ws/{player_name}")
async def websocket_endpoint(websocket: WebSocket, player_name: str):
    await websocket.accept()
    logger.info(f"WebSocket connection established for {player_name}")

    # Create the game
    game = ChameleonGame.from_human_name(player_name, FastAPIHumanController)

    # Set the websocket for the human player
    game.player_from_name(player_name).controller.websocket = websocket

    try:
        await game.run_game()
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for player: {player_name}")


#
# @app.websocket("/ws/{game_id}")
# async def websocket_endpoint(websocket: WebSocket, game_id: str):
#     await websocket.accept()
#     logger.info(f"WebSocket connection established for {game_id}")
#
#     game: ChameleonGame = games[game_id]["game"]
#     games[game_id]["state"] = "connected"
#
#     # Set the websocket for the human player
#     game.player_from_name(games[game_id]["human"]).controller.websocket = websocket
#
#     try:
#         await game.run()
#
#     except WebSocketDisconnect:
#         logger.info(f"WebSocket disconnected for game: {game_id}")
#     finally:
#         games[game_id]["state"] = "disconnected"
