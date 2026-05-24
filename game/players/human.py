"""Human player CLI input with live board highlights during entry."""

from __future__ import annotations

import random
import sys
from collections.abc import Generator

from rich.console import Group, RenderableType
from rich.live import Live
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from ..board import Board
from ..exceptions import InvalidPlacementError, QuitGame
from ..rulebook import INVALID_PLACEMENT, INVALID_WORD, Rulebook
from ..types import EXCHANGE_COORDS, SKIP_MOVE, BoardState, Move
from ..ui import HELP_LINES, console, help_panel, parse_input_highlight, rack_panel, render_board, warn
from .base import Player


class HumanPlayer(Player):
    """Interactive player reading commands from stdin."""

    def __init__(
        self,
        player_id: int,
        init_tiles: list[str],
        rulebook: Rulebook,
        name: str | None = None,
    ) -> None:
        """If name is given, skip asking for it on stdin; otherwise prompt with help panel."""
        if name is None:
            while True:
                entered = Prompt.ask(
                    f"[bold bright_green]Name for Player {player_id}[/]", console=console
                )
                if entered.strip():
                    name = entered.strip()
                    break
                warn("Player names must contain non-space characters.")
        super().__init__(player_id, init_tiles, rulebook, name)

    def get_move(self, board_state: BoardState, board: Board | None = None) -> Move:
        """Read stdin until a valid move; QuitGame means the player quit."""
        typed_board = board if isinstance(board, Board) else None
        if typed_board is not None and sys.stdin.isatty():
            return self._tty_get_move(typed_board, board_state)

        err: str | None = None
        while True:
            console.print(rack_panel(self.tiles))
            if err:
                warn(err)
            line = Prompt.ask("[bold bright_green]Action[/]", console=console)
            err = None
            segments = line.lower().strip().split()
            if not segments:
                continue
            result = self._interpret(segments, board_state)
            if isinstance(result, Move):
                return result
            if result == "shuffle":
                continue
            err = "\n".join(f"{cmd:<22} {desc}" for cmd, desc in HELP_LINES) if result == "help" else result

    def _tty_get_move(self, board: Board, board_state: BoardState) -> Move:
        """TTY path: one Rich Live session for typing, errors, and the board."""
        buf = ""
        message: str | None = None

        def render() -> RenderableType:
            hl = parse_input_highlight(buf)
            needed = [ch for r, c, ch in hl.path if board.state[r][c] == " "]
            used = _rack_used_indices(self.tiles, needed)
            pieces: list[RenderableType] = [render_board(board, hl), rack_panel(self.tiles, used)]
            if message:
                pieces.append(Panel(message, title="[bold bright_cyan]Message[/]",
                                    border_style="cyan", padding=(0, 1)))
            if buf:
                pieces.append(Text.assemble(("Action: ", "bold bright_green"), (buf, "bright_white")))
            else:
                pieces.append(Text.assemble(
                    ("Action: ", "bold bright_green"),
                    ("type 'help' for a list of commands", "grey50"),
                ))
            return Group(*pieces)

        keys = _keystrokes()
        try:
            with Live(render(), console=console, auto_refresh=False,
                      transient=False) as live:
                while True:
                    for ch in keys:
                        if ch in ("\r", "\n"):
                            break
                        if ch in ("\x7f", "\x08"):
                            buf = buf[:-1]
                        elif ch.isprintable():
                            buf += ch
                        live.update(render(), refresh=True)

                    segments = buf.lower().strip().split()
                    buf = ""
                    if not segments:
                        live.update(render(), refresh=True)
                        continue
                    result = self._interpret(segments, board_state)
                    if isinstance(result, Move):
                        return result
                    message = None if result == "shuffle" else (
                        "\n".join(f"{cmd:<22} {desc}" for cmd, desc in HELP_LINES) if result == "help" else result
                    )
                    live.update(render(), refresh=True)
        finally:
            keys.close()

    def _interpret(self, segments: list[str], board_state: BoardState) -> Move | str:
        """Parse tokens into a Move, the string "help", or an error message."""
        if len(segments) == 1:
            if segments[0] == "skip":
                return SKIP_MOVE
            if segments[0] == "quit":
                raise QuitGame()
            if segments[0] == "help":
                return "help"
            if segments[0] == "shuffle":
                random.shuffle(self.tiles)
                return "shuffle"
            return f"Command '{segments[0]}' not recognized. Type 'help' for help."

        if len(segments) == 2 and segments[0] == "exchange":
            letters = segments[1].upper()
            if self._tiles_present(Move(EXCHANGE_COORDS, "", letters), board_state):
                return Move(EXCHANGE_COORDS, "", letters)
            return "Tiles for this exchange are not present in your rack."
        if len(segments) == 2 and segments[0] == "define":
            return self.rulebook.define(segments[1])

        if len(segments) != 4:
            return f"Command '{segments[0]}' not recognized. Type 'help' for help."

        sx, sy, direction, word = segments
        direction = direction.upper()
        try:
            move = Move((int(sy, 16), int(sx, 16)), direction, word.upper())
        except ValueError:
            return "Coordinates must be hex digits 0–d (e.g. 7, a, d)."
        move = _extend_move(move, board_state)
        row, col = move.coords
        if not (0 <= row <= 14 and 0 <= col <= 14):
            return "Moves must be within the boundaries 0 and d (d being hexadecimal 14)."
        if direction not in ("D", "R"):
            return f"Direction must be D or R, not {direction}."
        try:
            if not self._tiles_present(move, board_state):
                return "Your rack does not contain the tiles needed for this move."
            score = self.rulebook.score_move(move, board_state)
            if score == INVALID_PLACEMENT:
                return "Your word must connect to an existing tile (or the center square on the first move)."
            if score == INVALID_WORD:
                return "That word, or a word it forms on the board, isn't in the dictionary."
        except InvalidPlacementError as exc:
            return str(exc)
        return move

    def _tiles_present(self, move: Move, board_state: BoardState) -> bool:
        """True if the rack can cover every empty square this play needs."""
        rack = self.tiles.copy()
        is_d, is_r = move.dir == "D", move.dir == "R"
        y, x = move.coords
        wlen = len(move.word)
        if wlen and max(y + is_d * (wlen - 1), x + is_r * (wlen - 1)) > 14:
            return False
        for i, tile in enumerate(move.word.upper()):
            if move.coords == EXCHANGE_COORDS or board_state[y + i * is_d][x + i * is_r] == " ":
                if tile not in rack and "?" in rack:
                    tile = "?"
                try:
                    rack.remove(tile)
                except ValueError:
                    return False
        return True


def _extend_move(move: Move, board_state: BoardState) -> Move:
    """Prepend/append any already-placed tiles adjacent to the word along its axis."""
    y, x = move.coords
    dy, dx = (1, 0) if move.dir == "D" else (0, 1)

    # Walk backward to collect tiles placed before the word's start.
    prefix = ""
    py, px = y - dy, x - dx
    while 0 <= py <= 14 and 0 <= px <= 14 and board_state[py][px] != " ":
        prefix = board_state[py][px] + prefix
        py -= dy
        px -= dx

    # Walk forward from the word's end to collect tiles placed after it.
    suffix = ""
    ey = y + dy * len(move.word)
    ex = x + dx * len(move.word)
    while 0 <= ey <= 14 and 0 <= ex <= 14 and board_state[ey][ex] != " ":
        suffix += board_state[ey][ex]
        ey += dy
        ex += dx

    if not prefix and not suffix:
        return move
    return Move((y - dy * len(prefix), x - dx * len(prefix)), move.dir, prefix + move.word + suffix)


def _rack_used_indices(rack: list[str], needed: list[str]) -> set[int]:
    """Return the rack indices consumed by *needed* letters (blanks used as fallback)."""
    used: set[int] = set()
    for letter in needed:
        for i, tile in enumerate(rack):
            if i not in used and tile.upper() == letter:
                used.add(i)
                break
        else:
            for i, tile in enumerate(rack):
                if i not in used and tile == "?":
                    used.add(i)
                    break
    return used


def _keystrokes() -> Generator[str, None, None]:
    """Yield one character at a time from raw stdin."""
    if sys.platform == "win32":
        import msvcrt
        getwch = msvcrt.getwch  # type: ignore[attr-defined]
        while True:
            ch = getwch()
            if ord(ch) in (0, 224):
                getwch()
                continue
            yield ch
    else:
        import termios
        import tty

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch == "\x1b":
                    import select
                    if select.select([sys.stdin], [], [], 0)[0]:
                        sys.stdin.read(2)
                    continue
                if ch == "\x03":
                    raise KeyboardInterrupt
                yield ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
