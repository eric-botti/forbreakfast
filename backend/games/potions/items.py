import json
import os

from typing import List
from pydantic import BaseModel



class Ingredient(BaseModel):
    """An ingredient that can be used to brew a potion."""

    id: int
    name: str
    """The name of the ingredient."""
    cost: int


class Potion(BaseModel):
    """A potion that can be brewed and sold as part of an order."""

    id: int
    effect: str
    ingredients: List[int]
    value: int = 5

    @property
    def name(self):
        """Get the name of the potion."""
        return "potion of " + self.effect

    def can_brew(self, ingredient_pouch: List[int]):
        """Check if the player can brew this potion."""
        ingredients = set(self.ingredients)
        pouch = set(ingredient_pouch)

        return ingredients.issubset(pouch)


# Get the path of the items
item_data_path = os.path.join(os.path.dirname(__file__), "items")

ingredients_path = os.path.join(item_data_path, "ingredients.json")
potions_path = os.path.join(item_data_path, "potions.json")

with open(ingredients_path) as f:
    ingredients = json.load(f)["ingredients"]
    ingredients = [Ingredient(**ingredient) for ingredient in ingredients]


with open(potions_path) as f:
    potions = json.load(f)["potions"]
    all_potions = [Potion(**potion) for potion in potions]


def potion_from_id(potion_id: int):
    """Get the name of a potion from its ID."""
    potion = next(potion for potion in all_potions if potion.id == potion_id)

    return potion


def ingredient_name_from_id(ingredient_id: int):
    """Get the name of an ingredient from its ID."""
    ingredient = next(
        ingredient for ingredient in ingredients if ingredient.id == ingredient_id
    )

    return ingredient.name


def starting_ingredients():
    """Get the starting ingredients for the game."""
    ingredient_deck = []
    for ingredient in ingredients:
        # Add 5 copies of each ingredient to the deck
        ingredient_deck.extend([ingredient] * 5)

    return ingredient_deck
