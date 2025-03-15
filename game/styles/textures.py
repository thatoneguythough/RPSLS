import pyfiglet  # type: ignore
from typing import Optional
from rich.text import Text
from InquirerPy import get_style


def asciify(
    text: str,
    font: str = "slant",
    colour: Optional[str] = None,
    width: Optional[int] = 150,
):
    ascii_text = pyfiglet.figlet_format(text, font, width=150)
    rich_text = Text(ascii_text)
    if colour:
        rich_text.stylize(colour)
    return rich_text


texture = get_style(
    {
        "questionmark": "black",
        "answer": "#2196F3 bold",
        "input": "#673AB7",
        "question": "#FFE338",
        "pointer": "#E91E63 bold",
        "highlighted": "#673AB7 bold",
        "separator": "#CC5454",
        "instruction": "",  # default
        "text": "",
        "disabled": "#858585 italic",
    }
)
