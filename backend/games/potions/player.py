from typing import List

from pydantic import Field

from hippodrome import PlayerSubclass

from games.potions.items import Order, all_potions


class PotionPeddlersPlayer(PlayerSubclass):
    orders: List[Order] = Field(default_factory=list)

    gold: int = 10
    """The amount of gold the player has."""
    ingredient_pouch: List[int] = Field(default_factory=list)
    """The ingredients the player has in their pouch."""

    @property
    def brewable_potions(self):
        """Returns the potions that can be brewed with the current ingredients."""
        brewable_potions = []

        if not self.ingredient_pouch:
            return brewable_potions

        for potion in all_potions:
            ingredients = set(potion.ingredients)
            pouch = set([ingredient.id for ingredient in self.ingredient_pouch])

            # Check if the player has all the ingredients for the potion
            can_brew = ingredients.issubset(pouch)

            if can_brew:
                brewable_potions.append(potion.id)

        return brewable_potions
