from typing import List

from pydantic import Field

from hippodrome import PlayerSubclass
from games.potions.items import Order


class PotionPeddlersPlayer(PlayerSubclass):
    orders: List[Order] = Field(default_factory=list)
