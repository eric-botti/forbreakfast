import random
from typing import List
from collections import Counter

from pydantic import BaseModel

from games.potions.items import Ingredient, Potion, potion_from_id, all_potions

from games.potions.items import ingredient_name_from_id


class Order(BaseModel):
    """An order for a group of potions that can be fulfilled."""

    potions: list[int]
    """A list of potion IDs in the order."""
    value: int
    """How many gold coins the order is worth."""

    def can_fufill(self, player_potions: List[int]):
        """Check if the player can fulfill this order."""
        order_potions = set(self.potions)
        player_potions = set(player_potions)

        return order_potions.issubset(player_potions)


def random_order():
    """Create a random order for a player."""
    potions = []
    order_size = random.randint(2, 3)
    value = 0

    for i in range(order_size):
        potion = random.choice(all_potions)
        potions.append(potion.id)
        value += potion.value

    # Increase the value of the order, larger orders are worth more
    value = int(value * (1 + (0.25 * order_size)) + 0.5)

    order = Order(potions=potions, value=value)

    return order


def pretty_print_order(order: Order, include_ingredients=False):
    """Prints out an order in a more player friendly way."""

    potion_strs = []
    required_ingredients = []

    for potion_id, count in Counter(order.potions).items():
        potion = potion_from_id(potion_id)
        if count == 1:
            plural = ""
        else:
            plural = "s"

        potion_strs.append(f"{count} potion{plural} of {potion.effect}")

        required_ingredients.extend(potion.ingredients)

    order_str = f"{', '.join(potion_strs)} for {order.value} gold"

    if include_ingredients:
        order_str += "\nTo brew this order you would need the required ingredients:"
        for ingredient_id, count in Counter(required_ingredients).items():
            ingredient = ingredient_name_from_id(ingredient_id)
            plural = "s" if count > 1 else ""
            order_str += f"\n- {count} {ingredient}"

    return order_str





def pretty_print_orders(orders: List[Order], include_ingredients=False):
    """Prints out a list of orders in a more player friendly way."""
    order_strs = []

    for order in orders:
        order_strs.append(f"Order: {pretty_print_order(order, include_ingredients=include_ingredients)}")

    return "\n".join(order_strs)