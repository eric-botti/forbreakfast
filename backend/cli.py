from dotenv import load_dotenv

load_dotenv("local.env")


import asyncio
import os

from hippodrome.controllers.human.cli import HumanCLIController
# from games.potions.game import PotionPeddlers as Game

from chameleon.chameleon_game import ChameleonGame as Game


def main():
    print("Please Enter your name, or leave blank to run an AI only game")
    name = input()

    game = Game.from_human_name(name)

    asyncio.run(game.run_game())


if __name__ == "__main__":
    main()
