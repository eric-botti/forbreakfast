import random
from typing import ClassVar
from hippodrome import Game
from pydantic import Field

from games.potions.items import (
    Ingredient,
    random_order,
    potion_name_from_id,
    starting_ingredients,
    ingredient_name_from_id,
)
from games.potions.player import PotionPeddlersPlayer

STARTING_ORDER_COUNT = 3


class PotionPeddlers(Game):
    # Game metadata
    name: ClassVar[str] = "Potion Peddlers"
    description: ClassVar[str] = (
        "A game of strategy and negotiation where players compete to brew and sell the most potions."
    )
    number_of_players: ClassVar[int] = 1
    player_class = PotionPeddlersPlayer

    # Game state
    market: list[Ingredient] = Field(default_factory=list)
    """The current ingredients available for purchase in the market."""
    ingredient_deck: list[Ingredient] = Field(default_factory=list)
    """The deck of all ingredients available for purchase."""

    async def game_setup(self):

        # Deal out initial orders to each player
        for player in self.players:
            player.orders = self.get_random_orders()

            player_orders = []
            for order in player.orders:
                potion_names = [
                    potion_name_from_id(potion_id) for potion_id in order.potions
                ]

                player_orders.append(
                    f"Order: {', '.join(potion_names)} for {order.value} gold"
                )

            player_order_str = "\n".join(player_orders)

            await self.game_message(
                f"{player.name}, you have the following orders to fulfill:\n{player_order_str}",
                recipient=player,
            )

        # Set up the market
        self.ingredient_deck = starting_ingredients()
        self.market = random.sample(self.ingredient_deck, 5)

    async def run_game(self):
        await self.game_setup()

        await self.game_message(
            "Welcome to Potion Peddlers! The game will begin shortly."
        )

        for player in self.players:
            await self.game_message(f"It's your turn")

            # Phase 1: Buy ingredients
            # Buy ingredients from the market
            await self.game_message(
                f"{player.name}, you have 10 gold. You can buy ingredients to brew potions."
            )

            # Show the player the market
            market_contents = [
                f"{ingredient.name} - {ingredient.cost} gold"
                for ingredient in self.market
            ]
            market_str = "\n".join(market_contents)
            await self.game_message(f"Market:\n{market_str}", recipient=player)

            # Ask the player to buy ingredients
            await self.game_message(
                "What would you like to buy?",
                recipient=player,
                choices=market_contents,
            )

            # Get the player's choice
            player_choice = await player.controller.generate_response()

            # Phase 2: Trade
            # Make trade offers to other players to get the ingredients you need

            # Phase 3: Brew potions
            # Use the ingredients you have to brew potions

    def get_random_orders(self):
        """Get a random set of potion orders for a player."""
        orders = []

        for i in range(STARTING_ORDER_COUNT):
            orders.append(random_order())

        return orders
