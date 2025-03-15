import json
import yaml
from typing import Optional
from jsonschema import validate, ValidationError
from rich.console import Console
from rich.text import Text

from ..data.specs import Player, Element, Record
from ..styles.textures import asciify

c = Console()

SCHEMA_FILEPATH = "game/data/game_schema.json"


class RPSLS:
    def __init__(self, gamedata=str):
        """
        Args: gamedata(str) - Filepath to the game_data.yaml file
        """
        try:
            # Initialising Game
            self.record = None
            self.players = []
            self.elements = []

            self.load_game_data(filepath=gamedata)

        except ValidationError as e:
            raise ValueError(f"Invalid game data: {e.message}", style="italic red")

    def determine_winner(self, P1: Player, P2: Player) -> bool:
        assert P1.element is not None
        assert P2.element is not None

        # Checks if outcome is the same
        if P1.element.name == P2.element.name:
            c.print(
                f"\n --= Both players have chosen {P1.element.name} - it's a draw! =--",
                style="bold dark_orange",
            )
            return True

        # Checks if P1's element is stronger
        for outcome in P1.element.wins_against:
            if outcome["state"] == P2.element.name:
                P1.total_win_count += 1
                P1.active_score += 1
                P1.battles_fought += 1

                text1 = asciify(P1.element.name, P1.element.font, P1.element.colour)
                text2 = asciify((outcome["action"]))
                text3 = asciify(P2.element.name, P2.element.font, P2.element.colour)

                combined_text = Text()
                combined_text.append(text1)
                combined_text.append(" ")
                combined_text.append(text2)
                combined_text.append(" ")
                combined_text.append(text3)

                c.print(combined_text)
                c.print(f"\n{P1.name} wins!", style="bold green")
                c.print(
                    f"\n{P1.name} : {P1.active_score} | {P2.active_score} : {P2.name}"
                )

                self.find_highscore()
                return False

        # Checks if P2's element is stronger
        for outcome in P2.element.wins_against:
            if outcome["state"] == P1.element.name:
                P2.total_win_count += 1
                P2.active_score += 1
                P2.battles_fought += 1
                self.print_combined_text(P2.element, outcome["action"], P1.element)
                c.print(f"\n{P2.name} wins!", style="bold green")
                c.print(
                    f"\n{P1.name} : {P1.active_score} | {P2.active_score} : {P2.name}"
                )

                self.find_highscore()
                return False

    def print_combined_text(
        self, element1: Element, action: str, element2: Element
    ) -> None:
        """
        Helper function to print combined ASCII text with different fonts and colors.
        """
        text1 = asciify(element1.name, font=element1.font, colour=element1.colour)
        text2 = asciify(text=action, colour="yellow")
        text3 = asciify(element2.name, font=element2.font, colour=element2.colour)

        combined_text = Text()
        combined_text.append(text1)
        combined_text.append(" ")
        combined_text.append(text2)
        combined_text.append(" ")
        combined_text.append(text3)

        c.print(combined_text)

    def find_highscore(self) -> None:
        highest_score_player = max(
            self.players, key=lambda player: player.total_win_count
        )
        self.record.high_score = highest_score_player.total_win_count
        self.record.player = highest_score_player.name

    def find_player_by_name(self, name: str) -> Player:
        for player in self.players:
            if player.name == name:
                return player
        raise ValueError(f"Player with name {name} not found!")

    def find_element_by_name(self, name: str) -> Optional[Element]:
        for element in self.elements:
            if element.name == name:
                return element
        return None

    def load_game_data(self, filepath) -> None:
        # Opens and validates YAML gamedata to schema
        try:
            schema_file = open(SCHEMA_FILEPATH, "r")
            schema = json.load(schema_file)

            yaml_file = open(filepath, "r")
            game_data = yaml.safe_load(yaml_file)

            validate(instance=game_data, schema=schema)
        except ValidationError as e:
            raise ValueError(f"Invalid game data: {e.message}")

        # Parses through the game data to collect: Elements, Player and Game Data
        self.record = Record(
            high_score=game_data["Record"]["High_score"],
            player=game_data["Record"]["Player"],
        )

        self.players = [
            Player(value["name"], value["total_win_count"], value["battles_fought"])
            for value in game_data["Players"]
        ]

        self.elements = [
            Element(
                value["name"], value["colour"], value["font"], value["wins_against"]
            )
            for value in game_data["Elements"]
        ]

    def reset_game_data(self, filepath) -> None:
        # Resets player data
        for player in self.players:
            player.total_win_count = 0
            player.battles_fought = 0

        # Reset record data
        self.record.high_score = 0
        self.record.player = ""

        # Savess the reset data
        self.save_game_data(filepath)

    def save_game_data(self, filepath) -> None:
        """
        Description: Saves the game data
        Args: filepath(str) - Filepath to the game_data.yaml file
        """
        game_data = {
            "Record": {
                "High_score": self.record.high_score,
                "Player": self.record.player,
            },
            "Players": [
                {
                    "name": player.name,
                    "total_win_count": player.total_win_count,
                    "battles_fought": player.battles_fought,
                }
                for player in self.players
            ],
            "Elements": [
                {
                    "name": element.name,
                    "colour": element.colour,
                    "font": element.font,
                    "wins_against": element.wins_against,
                }
                for element in self.elements
            ],
        }

        with open(filepath, "w") as updated_yaml_file:
            updated_yaml_file.write("# Game Data set\n")
            updated_yaml_file.write(
                "# yaml-language-server: $schema=./game_schema.json\n"
            )
            yaml.safe_dump(
                game_data,
                updated_yaml_file,
                default_flow_style=False,
                sort_keys=False,
            )
