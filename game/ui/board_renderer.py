"""Rich renderable for the game board."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console, ConsoleOptions, RenderResult
from rich.text import Text

from .highlight import Highlight
from .styles import (
    BLANK_TILE_STYLE,
    BONUS_GLYPHS,
    BONUS_STYLES,
    COORD_ACTIVE_STYLE,
    COORD_STYLE,
    HIGHLIGHT_CELL_STYLE,
    HIGHLIGHT_LINE_STYLE,
    TILE_STYLE,
)

# Board is imported only for type checking to avoid a circular dependency:
# board.py is pure game logic and must not import from the ui package.
if TYPE_CHECKING:
    from ..board import Board


class _BoardRenderable:
    """Wraps a Board + Highlight snapshot into a Rich console protocol object."""

    def __init__(self, board: Board, highlight: Highlight) -> None:
        self._board = board
        self._hl = highlight

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        hl = self._hl
        path_chars: dict[tuple[int, int], str] = {(r, c): ch for r, c, ch in hl.path}

        # Column header row
        header = Text("   ")
        for c in range(15):
            col_hex = format(c, "x")
            active = hl.col == c and hl.row is None
            header.append(f" {col_hex} ", style=COORD_ACTIVE_STYLE if active else COORD_STYLE)
        yield header

        # Grid rows
        for r in range(15):
            row_hex = format(r, "x")
            line = Text()
            active_row = hl.row == r and hl.col is None
            line.append(f"{row_hex}  ", style=COORD_ACTIVE_STYLE if active_row else COORD_STYLE)

            for c in range(15):
                tile = self._board.state[r][c]
                marker = self._board.special_tiles[r][c]

                if (r, c) in path_chars:
                    # Letter the player is about to place
                    line.append(f" {path_chars[(r, c)].upper()} ", style=HIGHLIGHT_CELL_STYLE)
                elif tile != " ":
                    # Already-placed tile
                    style = BLANK_TILE_STYLE if tile.islower() else TILE_STYLE
                    line.append(f" {tile.upper()} ", style=style)
                elif hl.col == c and hl.row == r:
                    # Cursor cell: show direction arrow once the player has typed one
                    glyph = ("→" if hl.direction == "R" else "↓") if hl.direction else BONUS_GLYPHS.get(marker, "·")
                    line.append(f" {glyph} ", style=HIGHLIGHT_CELL_STYLE)
                elif hl.col == c or hl.row == r:
                    # Guide line along the active column or row
                    line.append(f" {BONUS_GLYPHS.get(marker, '·')} ", style=HIGHLIGHT_LINE_STYLE)
                else:
                    style = BONUS_STYLES.get(marker, "grey50")
                    line.append(f" {BONUS_GLYPHS.get(marker, '·')} ", style=style)

            yield line


def render_board(board: Board, highlight: Highlight | None = None) -> _BoardRenderable:
    """Return a Rich renderable for *board*, optionally with move-input *highlight*."""
    return _BoardRenderable(board, highlight or Highlight())
