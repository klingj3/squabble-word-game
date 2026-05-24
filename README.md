# Python command-line SQUABBLE

[![PyPI version](https://img.shields.io/pypi/v/squabble-game.svg)](https://pypi.org/project/squabble-game/)
[![Python versions](https://img.shields.io/pypi/pyversions/squabble-game.svg)](https://pypi.org/project/squabble-game/)
[![License](https://img.shields.io/pypi/l/squabble-game.svg)](https://pypi.org/project/squabble-game/)
[![Release](https://github.com/klingj3/squabble-word-game/actions/workflows/release.yml/badge.svg)](https://github.com/klingj3/squabble-word-game/actions/workflows/release.yml)

A familiar-seeming but legally distinct word game for the terminal: local hot-seat play or computer opponents that search the move space each turn.

![Squabble demo](docs/demo.gif)

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Setup

From the repository root:

```bash
uv sync
```

Or with pip:

```bash
python3 -m pip install -e .
```

Copy `.env.example` to `.env` if you need to override where data files live (see **Data files** below).

## Data files

Dictionary and tile data are loaded from the directory pointed to by **`DATA_ROOT`**. If unset, it defaults to `game/data` next to the installed package (the usual layout in this repo).

You can set `DATA_ROOT` in a `.env` file at the project root (loaded automatically via `python-dotenv`) or export it in your shell.

## Run the game

```bash
uv run squabble
uv run squabble <human_players> <computer_players>
```

Or:

```bash
python3 -m game
python3 game_manager.py
```

### Moves (human)

- `quit` — leave the game
- `skip` — pass the turn
- `exchange <LETTERS>` — trade tiles (when bag rules allow)
- `define <WORD>` — look up a definition (when available)
- `<x> <y> <R|D> <WORD>` — play at column `x`, row `y`, direction right or down (coordinates use the same hex digit column headers as the printed board)

## Development

```bash
uv run pytest
uv run mypy game tests
```

Type checking targets the `game` package and `tests` with strict defaults (`pyproject.toml`).

## Layout

- `game/cli.py` — entry point and argument parsing
- `game/board.py` — board state
- `game/rulebook.py` — dictionary, scoring, validation
- `game/tile_bag.py` — tile pool
- `game/game_master.py` — turn loop and scoring
- `game/players/` — human and computer players
- `game/ui/` — rendering, panels, and display logic (includes deliberate animation delays for readability)
- `game/paths.py` — `DATA_ROOT` / `data_path()`
- `game/types.py` — shared type definitions
- `tests/` — pytest suite

The AI move search is fast enough that two computer players can complete multiple full games per second when run without the UI layer.

## Credits

- Word definitions sourced via the [Free Dictionary API](https://github.com/meetDeveloper/freeDictionaryAPI)
