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
            await self.player_turn(player)

        for player in self.players:
            await self.player_turn(player)

    async def player_turn(self, player):
        await self.game_message(f"It's your turn")

        # Phase 1: Buy ingredients
        # Buy ingredients from the market
        await self.game_message(
            f"{player.name}, you have {player.gold} gold. You can buy ingredients to brew potions."
        )

        # Show the player the market
        market_contents = [
            f"{ingredient.name} - {ingredient.cost} gold" for ingredient in self.market
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

        # Check if the player has enough gold to buy the ingredient
        if chosen_ingredient.cost > player.gold:
            await self.game_message(
                f"You don't have enough gold to buy {chosen_ingredient.name}.",
                recipient=player,
            )
            return
        else:
            # Deduct the cost of the ingredient from the player's gold
            player.gold -= chosen_ingredient.cost

            # Add the ingredient to the player's inventory
            player.ingredient_pouch.append(chosen_ingredient)

            # Remove the ingredient from the market
            del self.market[player_choice.choice_idx]

        await self.game_message(
            f"You bought {chosen_ingredient.name} for {chosen_ingredient.cost} gold.\n"
            f"You now have {player.gold} gold.",
            recipient=player,
        )

        # Phase 2: Brew potions
        # Use the ingredients you have to brew potions
        if player.brewable_potions:
            choices = [
                potion_name_from_id(potion_id) for potion_id in player.brewable_potions
            ]
            choices += ["Skip brewing"]

            await self.game_message(
                f"{player.name}, you can now brew potions with the ingredients you have.\n",
                recipient=player,
                choices=choices,
            )

            # Get the player's choice
            player_choice = await player.controller.generate_response()

        else:
            await self.game_message(
                f"{player.name}, you don't have enough ingredients to brew any potions.",
                recipient=player,
            )

        # Restock the market
        while len(self.market) < 5 and self.ingredient_deck:
            if self.ingredient_deck:
                new_ingredient = self.ingredient_deck.pop()
                self.market.append(new_ingredient)
            else:
                break

        # Phase 3: Fulfill orders
        # Check if the player can fulfill any orders
        if player.orders:
            order_strs = []
            for order in player.orders:
                potion_names = [
                    potion_name_from_id(potion_id) for potion_id in order.potions
                ]

                order_strs.append(
                    f"Order: {', '.join(potion_names)} for {order.value} gold"
                )

            await self.game_message(
                f"{player.name}, you have the following orders to fulfill:\n{'\n'.join(order_strs)}",
                recipient=player,
            )

            await self.game_message(
                f"{player.name}, you can now fulfill orders.",
                recipient=player,
            )

            choices = [
                f"Fulfill Order: {', '.join([potion_name_from_id(potion_id) for potion_id in order.potions])} for {order.value} gold"
                for order in player.orders
            ]
            choices += ["Skip fulfilling orders"]

            await self.game_message(
                "What would you like to do?",
                recipient=player,
                choices=choices,
            )

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
    