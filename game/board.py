"""Squabble board representation and move application."""

from __future__ import annotations

from .types import BoardState, Move


class Board:
    """15×15 grid with bonus-square layout and applied letters."""

    def __init__(self) -> None:
        """Initialize empty rows and the standard bonus-square pattern."""
        self.special_tiles: list[str] = [
            "W  l   W   l  W",
            " w   L   L   w ",
            "  w   l l   w  ",
            "l  w   l   w  l",
            "    w     w    ",
            " L   L   L   L ",
            "  l   l l   l  ",
            "W  l   *   l  W",
            "  l   l l   l  ",
            " L   L   L   L ",
            "    w     w    ",
            "l  w   l   w  l",
            "  w   l l   w  ",
            " w   L   L   w ",
            "W  l   W   l  W",
        ]
        self.state: BoardState = ["".join([" " for _ in range(15)]) for _ in range(15)]

    def play_move(self, move: Move) -> bool:
        """Write the word into the grid at coords along move.dir."""
        y, x = move.coords
        if move.dir == "D":
            for i, c in enumerate(move.word):
                row = self.state[y + i]
                self.state[y + i] = row[:x] + c + row[x + 1 :]
        if move.dir == "R":
            row = self.state[y]
            self.state[y] = row[:x] + move.word + row[x + len(move.word) :]
        return True
