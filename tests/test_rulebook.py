"""Rulebook tests."""

from __future__ import annotations

from typing import ClassVar
from unittest import TestCase

import pytest

from game.rulebook import INVALID_PLACEMENT, INVALID_WORD, Rulebook
from game.types import Move


class TestRulebook(TestCase):
    rulebook: ClassVar[Rulebook]

    @classmethod
    def setUpClass(cls) -> None:
        cls.rulebook = Rulebook()

    def test_score_moves(self) -> None:
        blank_board = ["".join([" " for _ in range(15)]) for _ in range(15)]
        test_board = blank_board.copy()
        test_board[1] = "    DOG        "

        test_move = Move((1, 7), "D", "SLAP")
        self.assertTrue(self.rulebook.score_move(test_move, test_board) > 0)

        test_move = Move((2, 6), "R", "ORANGE")
        self.assertTrue(self.rulebook.score_move(test_move, test_board) > 0)

        test_move = Move((2, 1), "R", "CHROMO")
        self.assertTrue(self.rulebook.score_move(test_move, test_board) > 0)

        test_move = Move((2, 1), "R", "CRUNCH")
        self.assertEqual(self.rulebook.score_move(test_move, test_board), INVALID_WORD)

        test_move = Move((2, 1), "R", "ZXVY")
        self.assertEqual(self.rulebook.score_move(test_move, test_board), INVALID_WORD)

        test_move = Move((7, 7), "R", "QI")
        self.assertEqual(self.rulebook.score_move(test_move, blank_board), 22)
        test_board = blank_board.copy()
        test_board[8] = " " * 7 + "I" + " " * 7

        test_move = Move((7, 7), "R", "QI")
        self.assertEqual(self.rulebook.score_move(test_move, test_board), 44)

        test_board = blank_board.copy()
        test_board[14] = " " + "U" + " " * 13
        test_move = Move((14, 0), "R", "QUINTETS")
        self.assertEqual(self.rulebook.score_move(test_move, test_board, allow_illegal=True), 50 + 18 * 9)

    def test_disconnected_move_returns_invalid_placement(self) -> None:
        """A valid word with no board connection returns INVALID_PLACEMENT, not INVALID_WORD."""
        blank_board = ["".join([" " for _ in range(15)]) for _ in range(15)]
        board = blank_board.copy()
        board[0] = "CAT            "  # existing word nowhere near center
        test_move = Move((14, 0), "R", "DOG")
        self.assertEqual(self.rulebook.score_move(test_move, board), INVALID_PLACEMENT)


@pytest.mark.integration
def test_define_live() -> None:
    result = Rulebook().define("HELLO")
    assert "HELLO" in result
    assert "dictionary server" not in result
    assert "not in the Scrabble word list" not in result
