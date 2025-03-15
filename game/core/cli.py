import os
import random
from copy import deepcopy
from time import sleep
from InquirerPy import inquirer
from InquirerPy.separator import Separator
from rich import console
from rich.table import Table

from game.core.rpsls import RPSLS
from game.styles.textures import asciify, texture
from game.data.specs import Player

c = console.Console()

GAMEDATA_FILEPATH = "game/data/game_data.yaml"


class CLI:
    def __init__(self, game: RPSLS):
        self.game = game
        self.running = True

    def clear_terminal(self):
        os.system("cls" if os.name == "nt" else "clear")

    def prompt_main_menu(self):
        while self.running:
            self.clear_terminal()

            c.print(
                asciify(
                    text="Rock, Paper, Scissors",
                    colour="bold purple",
                )
            )
            c.print(
                asciify(
                    text="... Lizard? Spock?!?",
                    colour="bold green",
                )
            )

            c.print("Main menu:", style="bold blue underline")
            main_menu = inquirer.select(
                message="What would you like to do?",
                choices=["Play Game!", "View Stats", "How to Play"]
                + [Separator("─" * 40), "Exit"],
                pointer="↳",
                transformer=lambda x: "Let's have a match!"
                if x == "Play Game!"
                else "",
                style=texture,
            ).execute()

            match main_menu:
                case "Play Game!":
                    self.prompt_game()
                case "View Stats":
                    self.prompt_view_stats()
                case "How to Play":
                    self.prompt_instructions()
                case "Exit":
                    self.running = False
                    c.print("\nGame exited.", style="bold red")

    def prompt_game(self) -> None:
        P1, P2 = self.prompt_player_choice()

        rematch = True
        while rematch:
            draw = True
            while draw:
                draw = self.prompt_element_choice(P1, P2)

            rematch = inquirer.confirm(
                message="Rematch? ...", default=False, style=texture
            ).execute()

            self.game.save_game_data(GAMEDATA_FILEPATH)

        c.print("Returning to main menu...", style="italic white")

    def prompt_player_choice(self) -> tuple[Player, Player]:
        c.print("\nPlease select your players...", style="bold blue underline")
        player_names = [player.name for player in self.game.players]

        name_1 = inquirer.select(
            message="Player 1 | choose your character!",
            choices=player_names,
            pointer="↳",
            mandatory=False,
            style=texture,
        ).execute()

        player_names.remove(name_1)

        name_2 = inquirer.select(
            message="Player 2 | choose your character!",
            choices=player_names,
            pointer="↳",
            mandatory=False,
            style=texture,
        ).execute()

        P1 = self.game.find_player_by_name(name_1)
        P2 = self.game.find_player_by_name(name_2)

        P1.active_score = 0
        P2.active_score = 0

        return P1, P2

    def prompt_element_choice(self, P1=Player, P2=Player) -> bool:
        """
        This is the main game for players to select their elements of choice
        If the outcome happens to be a draw, the game will be retried
        """
        c.print(
            "\nGet ready to choose your element!", style="bold spring_green4 underline"
        )
        options = [element.name for element in self.game.elements]

        P1_decision = self.display_element_choices(P1, options)
        P2_decision = self.display_element_choices(P2, options)

        P1.element = self.game.find_element_by_name(P1_decision)
        P2.element = self.game.find_element_by_name(P2_decision)

        assert P1.element is not None
        assert P2.element is not None

        c.print(f"\n{P1.name} chose: {P1.element.name}", style="bold cyan")
        c.print(f"{P2.name} chose: {P2.element.name}", style="bold red")

        return self.game.determine_winner(P1, P2)

    def display_element_choices(self, player: Player, options=list[str]) -> str:
        """
        Inquires the user to choose an element.
        The choices are randomised so the other player cannot guess by click counting.
        """
        if player.name == "CPU":
            return random.choice(options)

        random.shuffle(options)

        decision = inquirer.select(
            message=f"{player.name} | Choose an element wisely...",
            choices=options,
            transformer=lambda _: "You have made your choice!",
            mandatory=False,
            style=texture,
        ).execute()

        return decision

    def prompt_view_stats(self) -> None:
        self.clear_terminal()
        c.print(
            asciify(
                text=f"High Score : {self.game.record.high_score}",
                font="alligator",
                colour="Magenta",
            )
        )
        c.print()
        c.print(
            asciify(text=f" - {self.game.record.player}", font="cosmic", colour="white")
        )
        stats = Table()
        stats.add_column("Player", style="bold cyan")
        stats.add_column("Score", style="bold green", justify="center")
        stats.add_column("Battles Fought", style="bold red", justify="center")
        top_score = deepcopy(self.game.players)
        top_score.sort(key=lambda player: player.total_win_count, reverse=True)

        for value in top_score:
            stats.add_row(
                value.name, str(value.total_win_count), str(value.battles_fought)
            )
            stats.add_row()

        c.print(stats)
        reset = inquirer.select(
            message="What would you like to do?",
            choices=["Reset Game Data"] + [Separator("─" * 40), "Exit"],
            default="Exit",
            style=texture,
        ).execute()

        if reset == "Reset Game Data":
            confirm_reset = inquirer.confirm(
                message="Are you sure you want to reset game data?\nThis resets the high score and all player data.",
                default=False,
                style=texture,
            ).execute()

            if confirm_reset:
                self.game.reset_game_data(GAMEDATA_FILEPATH)
                c.print("\nGame data has been reset!! ☠", style="bold red")
                sleep(2)
            else:
                pass

    def prompt_instructions(self) -> None:
        self.clear_terminal()

        c.print("Instructions:", style="bold blue underline")
        instructions = Table()
        instructions.add_column("Element", style="bold cyan")
        instructions.add_column("Wins Against", style="bold green")
        instructions.add_column("Reason", style="bold yellow")

        for value in self.game.elements:
            name = value.name
            strengths = ", ".join([outcome["state"] for outcome in value.wins_against])
            reasons = ", ".join(
                [
                    f"{outcome['action'].capitalize()} {outcome['state']}"
                    for outcome in value.wins_against
                ]
            )

            instructions.add_row(
                name,
                strengths,
                reasons,
            )
            instructions.add_row()

        c.print(instructions)
        inquirer.confirm(
            message="Press Enter to return to the main menu...",
            default=True,
            style=texture,
        ).execute()


if __name__ == "__main__":
    game = RPSLS(GAMEDATA_FILEPATH)
    cli = CLI(game)
    try:
        cli.prompt_main_menu()
    except Exception:
        c.print("\nGame exited.", style="bold red")
