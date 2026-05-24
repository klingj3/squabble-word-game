"""Tile and bonus-square styling shared by the board and panels."""

from __future__ import annotations

from rich.text import Text

# Bonus-square palette; keys match Board.special_tiles encoding.
BONUS_STYLES: dict[str, str] = {
    "W": "bold white on red",       # Triple Word
    "w": "bold white on magenta",   # Double Word
    "L": "bold white on blue",      # Triple Letter
    "l": "bold white on cyan",      # Double Letter
    "*": "bold yellow on magenta",  # Center star
}

BONUS_GLYPHS: dict[str, str] = {
    "W": "W",
    "w": "w",
    "L": "L",
    "l": "l",
    "*": "★",
    " ": "·",
}

# Style used for letters actually placed on the board.
TILE_STYLE: str = "bold black on bright_yellow"

# Style for tiles played from a blank (lowercase letters).
BLANK_TILE_STYLE: str = "bold black on bright_white"

# Board coordinate header styles.
COORD_STYLE: str = "grey50"
COORD_ACTIVE_STYLE: str = "bold bright_yellow underline"

# Cell highlight styles used during move input.
HIGHLIGHT_CELL_STYLE: str = "bold black on bright_green"
HIGHLIGHT_LINE_STYLE: str = "bold bright_yellow"

# Rack tile states: available, used (spent in the current preview), dim (not yet revealed).
USED_TILE_STYLE: str = "bold grey35 on grey19"
DIM_TILE_STYLE: str = "grey35 on grey19"
TILE_SCORE_STYLE: str = "grey70"
USED_TILE_SCORE_STYLE: str = "grey35"

# Scoreboard score value styles.
SCORE_STYLE: str = "bold bright_green"
SCORE_WINNER_STYLE: str = "bold bright_yellow"
SCORE_HIGHLIGHT_STYLE: str = "bold reverse bright_yellow"


def tile_cell(char: str) -> Text:
    """Render a played tile letter with the standard tile background."""
    if char.islower():
        return Text(f" {char.upper()} ", style=BLANK_TILE_STYLE)
    return Text(f" {char} ", style=TILE_STYLE)


def bonus_cell(marker: str) -> Text:
    """Render a bonus-square marker (or empty dot) with colour."""
    glyph = BONUS_GLYPHS.get(marker, "·")
    style = BONUS_STYLES.get(marker, "grey50")
    return Text(f" {glyph} ", style=style)
