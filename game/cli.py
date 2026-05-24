"""CLI entry point."""

from __future__ import annotations

import sys

from rich.prompt import IntPrompt

from .exceptions import QuitGame
from .game_master import GameMaster
from .ui import console, show_launch_splash


def _ask_player_counts() -> tuple[int, int]:
    """Interactively prompt for human/computer player counts after the splash."""
    while True:
        human_count = IntPrompt.ask(
            "[bold bright_green]Number of human players[/]", console=console, default=1
        )
        computer_count = IntPrompt.ask(
            "[bold bright_green]Number of computer players[/]", console=console, default=1
        )
        if human_count < 0 or computer_count < 0:
            console.print("[bold red]Counts cannot be negative.[/]")
            continue
        if human_count + computer_count < 1:
            console.print("[bold red]Need at least one player.[/]")
            continue
        return human_count, computer_count


def main() -> int:
    """Run from argv; exit 0 even when the player quits."""
    try:
        if len(sys.argv) == 1:
            show_launch_splash()
            human_count, computer_count = _ask_player_counts()
            gm = GameMaster(human_count=human_count, computer_count=computer_count)
            gm.play_game(True, show_splash=False)
        elif len(sys.argv) == 3:
            try:
                human_count = int(sys.argv[1])
                computer_count = int(sys.argv[2])
            except ValueError:
                print("Usage: squabble [<humans> <computers>]", file=sys.stderr)
                return 1
            gm = GameMaster(human_count, computer_count)
            gm.play_game(True)
        else:
            print("Usage: squabble [<humans> <computers>]", file=sys.stderr)
            return 1
    except QuitGame:
        pass
    return 0
