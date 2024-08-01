import random
from typing import ClassVar
from hippodrome import Game
from pydantic import Field

from games.potions.items import (
    Ingredient,
    potion_from_id,
    starting_ingredients,
    ingredient_name_from_id,
)
from games.potions.orders import random_order, pretty_print_orders, pretty_print_order

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

            await self.game_message(
                pretty_print_orders(player.orders, include_ingredients=True),
                recipient=player,
            )

        # Set up the market
        self.ingredient_deck = starting_ingredients()
        self.market = random.sample(self.ingredient_deck, 5)

    async def run_game(self):
        await self.game_message(
            "Welcome to Potion Peddlers! The game will begin shortly."
            "The Game is simple, you will be given a list of orders to fulfill, each order requires a set of potions to be fulfilled."
            "You will get ingredients from the market to brew potions, and then sell them to fulfill orders."
            "The player with the most gold at the end of the game wins."
        )

        await self.game_setup()



        for player in self.players:
            await self.player_turn(player)

        for player in self.players:
            await self.player_turn(player)

    async def player_turn(self, player):
        # Phase 1: Gather ingredients
        # Buy ingredients from the market
        await self.game_message(
            f"{player.name}, you may grab an ingredient from the market."
        )

        # Show the player the market
        market_contents = [
            ingredient.name for ingredient in self.market
        ]

        # Ask the player to buy ingredients
        await self.game_message(
            "What would you like to buy?",
            recipient=player,
            choices=market_contents,
        )

        # Get the player's choice
        player_choice = await player.controller.generate_response()

        chosen_ingredient = self.market[player_choice.choice_idx]

        # Add the ingredient to the player's inventory
        player.ingredient_pouch.append(chosen_ingredient)

        # Remove the ingredient from the market
        del self.market[player_choice.choice_idx]

        await self.game_message(
            f"You bought {chosen_ingredient.name} for {chosen_ingredient.cost} gold.\n"
            f"You now have {player.gold} gold.",
            recipient=player,
        )

        # Restock the market
        while len(self.market) < 5 and self.ingredient_deck:
            if self.ingredient_deck:
                new_ingredient = self.ingredient_deck.pop()
                self.market.append(new_ingredient)
            else:
                break

        # Phase 2: Brew and Fulfill orders
        # Check if the player can fulfill any orders
        if player.orders:
            await self.game_message(
                f"You are working on the following orders: \n{pretty_print_orders(player.orders)}\n"
                "Once you have the required ingredients, you can fulfill them.",
                recipient=player,
            )

            choices = []

            for order in player.orders:
                if order.can_fufill(player.brewable_potions):
                    choices.append(f"Fulfill Order: {pretty_print_order(order)}")

            if choices:
                choices += ["Skip fulfilling orders"]
                await self.game_message(
                    "You can fulfill one of the following orders, or wait",
                    recipient=player,
                    choices=choices,
                )

            if not choices:
                await self.game_message(
                    f"{player.name}, you don't have the potions to fulfill any of those orders.",
                    recipient=player,
                )
                return



            # Get the player's choice
            player_choice = await player.controller.generate_response()

            if player_choice.content.startswith("Fulfill Order"):
                order_idx = choices.index(player_choice.content)
                order = player.orders.pop(order_idx)

                # Check if the player has all the potions to fulfill the order
                if set(order.potions).issubset(player.brewable_potions):
                    player.gold += order.value
                    await self.game_message(
                        f"{player.name}, you fulfilled the order and earned {order.value} gold.",
                        recipient=player,
                    )
                else:
                    await self.game_message(
                        f"{player.name}, you don't have the required potions to fulfill this order.",
                        recipient=player,
                    )

        else:
            await self.game_message(
                f"{player.name}, you don't have any orders to fulfill.",
                recipient=player,
            )



    def get_random_orders(self):
        """Get a random set of potion orders for a player."""
        orders = []

        for i in range(STARTING_ORDER_COUNT):
            orders.append(random_order())

        return orders


