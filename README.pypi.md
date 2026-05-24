# squabble-game

A familiar-seeming but legally distinct word game for the terminal. Play hot-seat against friends or let computer opponents search the move space each turn.

## Install

```bash
pip install squabble-game
```

Requires Python 3.12+.

## Play

```bash
squabble                                        # 1 human vs 1 computer (default)
squabble <human_players> <computer_players>     # e.g. squabble 2 0, squabble 0 2
```

### Commands during a game

| Command | Effect |
|---|---|
| `<x> <y> <R\|D> <WORD>` | Place a word at column `x`, row `y`, going right or down |
| `exchange <LETTERS>` | Return tiles to the bag and draw new ones |
| `define <WORD>` | Look up a word's definition |
| `skip` | Pass the turn |
| `quit` | End the game |

Coordinates follow the hex digit column headers shown on the printed board.

## Credits

Word definitions sourced via the [Free Dictionary API](https://github.com/meetDeveloper/freeDictionaryAPI).
