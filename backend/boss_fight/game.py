from typing import Literal, ClassVar

from hippodrome import Game, PlayerSubclass
from hippodrome.output_formats import OutputFormatModel

class BossFightPlayer(PlayerSubclass):
    health: int = 100


class ActionFormat(OutputFormatModel):
    action: Literal["attack", "heal", "flee"]



class BossFight(Game):

    number_of_players : ClassVar[int] = 2

    async def run_game(self):
        await self.game_message("Welcome to Boss Fight!")
        await self.game_message("You are a hero who has come to defeat the evil boss!")
        await self.game_message("You have 3 actions you can take each turn:")
        await self.game_message("Attack: Deal damage to the boss")
        await self.game_message("Heal: Heal yourself or a teammate for 10 health points")
        await self.game_message("Flee: Run away from the boss, but you will lose the game")

        for player in self.players:
            await self.game_message(f"What do you do", player)

            response = await player.controller.generate_formatted_response(
                ActionFormat
            )


            if response.action == "attack":
                await self.game_message(f"{player} attacks the boss!")

            elif response.action == "heal":
                await self.game_message(f"{player} heals themselves!")

            elif response.action == "flee":
                await self.game_message(f"{player} flees the boss fight!")






