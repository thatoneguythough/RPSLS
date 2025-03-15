# R.P.S.L.S

RPSLS (Rock, Paper, Scissors, Lizard, Spock) is a CLI game implemented in Python. It extends the regular game of Rock, Paper Scissors by creating x2 additional strengths and weaknesses. 
The game allows players to choose their profiles and modify the existing elements to compete against each other.
Alternatively, there is a CPU that can also be beaten.

## Features

- Play against another player (locally) or the in-built CPU - which chooses randomly
- View and reset the game statistics
- Learn the strengths and weakneses
- Customizable profiles and elements
- Consistent scoreboarding between two players

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/rpsls.git
    cd rpsls
    ```

2. Install `asdf` and use it to install Poetry:
    ```sh
    # Install asdf (if not already installed)
    https://asdf-vm.com/guide/getting-started.html

    # Install Poetry using asdf
    asdf plugin-add poetry
    asdf install poetry 1.8.4
    asdf local poetry 1.8.4
    ```

3. Install the required dependencies using Poetry:
    ```sh
    poetry install
    ```

## Usage

1. Run the game:
    ```sh
    poetry run python game/core/cli.py
    ```

2. Alternatively, you can use the `justfile` to play the game:
    ```sh
    brew install just
    ```

    ```sh
    just play
    ```

3. Follow the on-screen prompts to play the game, view stats, or learn how to play.

## Customization

You can customize the game by updating the `game/data/game_data.yaml` file to add more players and elements and update scores.

### Example `game_data.yaml`

```yaml
Record:
  High_score: 0
  Player: "Jazz"

Players:
  - name: "Jazz"
    total_win_count: 0
    battles_fought: 0

  - name: "Fabiana"
    total_win_count: 0
    battles_fought: 0

  - name: "Aadil"
    total_win_count: 0
    battles_fought: 0

  - name: "CPU"
    total_win_count: 0
    battles_fought: 0

Elements:
  - name: "Rock"
    colour: "red"
    font: "isometric1"
    wins_against:
      - state: "Scissors"
        action: "crushes"

      - state: "Lizard"
        action: "crushes"

  - name: "Paper"
    colour: "tan"
    font: "lean"
    wins_against:
      - state: "Rock"
        action: "covers"

      - state: "Spock"
        action: "disproves"

  - name: "Scissors"
    colour: "bright_black"
    font: "5lineoblique"
    wins_against:
      - state: "Paper"
        action: "cuts"

      - state: "Lizard"
        action: "decapitates"

  - name: "Lizard"
    colour: "green"
    font: "cosmic"
    wins_against:
      - state: "Spock"
        action: "poisons"

      - state: "Paper"
        action: "eats"

  - name: "Spock"
    colour: "blue"
    font: "epic"
    wins_against:
      - state: "Scissors"
        action: "smashes"

      - state: "Rock"
        action: "vaporizes"
