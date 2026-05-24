"""Rich-based UI: console, colours, panels, highlights, and the game-loop presenter."""

from __future__ import annotations

from .board_renderer import render_board
from .console import console, error, info, success, warn
from .highlight import Highlight, parse_input_highlight
from .panels import HELP_LINES, goodbye_banner, help_panel, legend, rack_panel, show_launch_splash
from .presenter import GamePresenter
from .styles import (
    BLANK_TILE_STYLE,
    BONUS_GLYPHS,
    BONUS_STYLES,
    TILE_STYLE,
    bonus_cell,
    tile_cell,
)
