RPSLS (Rock, Paper, Scissors, Lizard, Spock) is a CLI game implemented in Python. It extends the regular game of Rock, Paper Scissors by creating x2 additional strengths and weaknesses. 
The game allows players to choose their profiles and modify the existing elements to compete against each other.
Alternatively, there is a CPU that can also be beaten.

## Features

- Play against another player (locally) or the in-built CPU
- View game statistics
- Learn how to play the game (TBD)
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
    git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.10.2
    echo '. $HOME/.asdf/asdf.sh' >> ~/.bashrc
    source ~/.bashrc

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
    poetry run python rpsls/rpsls_cli.py
    ```

2. Alternatively, you can use the `justfile` to play the game:
    ```sh
    just play
    ```

3. Follow the on-screen prompts to play the game, view stats, or learn how to play.

## Customization

You can customize the game by updating the `rpsls/rules/gamedata.yaml` file to add more players and elements and update scores.

### Example `gamedata.yaml`

```yaml
Game:
  High_score: 10
  Player: "Player1"

Players:
  - name: "Player1"
    total_win_count: 5

  - name: "Player2"
    total_win_count: 3

  - name: "CPU"
    total_win_count: 2

Elements:
  - name: "Rock"
    colour: "grey"
    font: "standard"
    wins_against:
      - state: "Scissors"
        action: "crushes"

      - state: "Lizard"
        action: "crushes"

  - name: "Paper"
    colour: "white"
    font: "standard"
    wins_against:
      - state: "Rock"
        action: "covers"

      - state: "Spock"
        action: "disproves"

  - name: "Scissors"
    colour: "silver"
    font: "standard"
    wins_against:
      - state: "Paper"
        action: "cuts"

      - state: "Lizard"
        action: "decapitates"

  - name: "Lizard"
    colour: "green"
    font: "standard"
    wins_against:
      - state: "Spock"
        action: "poisons"

      - state: "Paper"
        action: "eats"

  - name: "Spock"
    colour: "blue"
    font: "standard"
    wins_against:
      - state: "Scissors"
        action: "smashes"

      - state: "Rock"
        action: "vaporizes"