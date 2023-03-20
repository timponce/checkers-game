import unittest
from CheckersGame import Checkers, InvalidSquare, ExceedPlayerCount, InvalidColor, InvalidPlayer, OutofTurn


class UnitTests(unittest.TestCase):

    def test_initialize_player(self):
        game = Checkers()
        Player1 = game.create_player("Adam", "White")
        self.assertEqual(Player1.get_piece_color(), "White")

    def test_attempt_to_add_three_players(self):
        game = Checkers()
        Player1 = game.create_player("Adam", "White")
        Player2 = game.create_player("Lucy", "Black")
        with self.assertRaises(ExceedPlayerCount) as cm:
            Player3 = game.create_player("Tony", "White")
        self.assertEqual(str(cm.exception), "There can only be two players per game")

    def test_attempt_to_use_invalid_color(self):
        game = Checkers()
        with self.assertRaises(InvalidColor) as cm:
            Player1 = game.create_player("Emilio", "Red")
        self.assertEqual(str(cm.exception), "This is not a valid color")

    def test_attempt_to_reuse_color(self):
        game = Checkers()
        Player1 = game.create_player("Adam", "White")
        with self.assertRaises(InvalidColor) as cm:
            Player2 = game.create_player("Lucy", "White")
        self.assertEqual(str(cm.exception), "This color has already been chosen")

    def test_initialize_board_and_checker_details_func(self):
        game = Checkers()
        self.assertEqual(game.get_checker_details((6, 1)), "Black")
        self.assertEqual(game.get_checker_details((3, 0)), None)
        self.assertEqual(game.get_checker_details((4, 7)), None)
        self.assertEqual(game.get_checker_details((0, 7)), "White")

    def test_checker_details_invalid_square_exception(self):
        game = Checkers()
        self.assertEqual(game.get_checker_details((6, 1)), "Black")
        with self.assertRaises(InvalidSquare) as cm:
            game.get_checker_details((0, 10))
        self.assertEqual(str(cm.exception), "This square does not exist")

    def test_checker_details_invalid_player_exception(self):
        game = Checkers()
        Player1 = game.create_player("Adam", "White")
        Player2 = game.create_player("Lucy", "Black")
        with self.assertRaises(InvalidPlayer) as cm:
            game.play_game("Miyoko", (5, 0), (4, 1))
        self.assertEqual(str(cm.exception), "This player does not exist")

    def test_play_game_out_of_turn_exception(self):
        game = Checkers()
        Player1 = game.create_player("Adam", "White")
        Player2 = game.create_player("Lucy", "Black")
        game.play_game("Lucy", (5, 2), (4, 1))
        game.play_game("Adam", (2, 1), (3, 2))
        with self.assertRaises(OutofTurn) as cm:
            game.play_game("Adam", (2, 5), (3, 6))
        self.assertEqual(str(cm.exception), "It is not this player's turn")

    def test_checker_details_invalid_starting_square_exception(self):
        game = Checkers()
        Player1 = game.create_player("Adam", "White")
        Player2 = game.create_player("Lucy", "Black")
        with self.assertRaises(InvalidSquare) as cm:
            game.play_game("Lucy", (0, 5), (1, 4))
        self.assertEqual(str(cm.exception), "Invalid starting square")

    def test_checker_details_invalid_starting_square_exception2(self):
        game = Checkers()
        Player1 = game.create_player("Adam", "White")
        Player2 = game.create_player("Lucy", "Black")
        with self.assertRaises(InvalidSquare) as cm:
            game.play_game("Lucy", (5, 6), (4, 6))
        self.assertEqual(str(cm.exception), "This square is not playable")

    def test_simple_move(self):
        game = Checkers()
        Player1 = game.create_player("Adam", "White")
        Player2 = game.create_player("Lucy", "Black")
        self.assertEqual(game.get_checker_details((5, 2)), "Black")
        game.play_game("Lucy", (5, 2), (4, 3))
        self.assertEqual(game.get_checker_details((5, 2)), None)
        self.assertEqual(game.get_checker_details((4, 3)), "Black")

    def test_more_simple_moves_and_change_turn(self):
        game = Checkers()
        Player1 = game.create_player("Adam", "White")
        Player2 = game.create_player("Lucy", "Black")
        self.assertEqual(game.get_checker_details((5, 2)), "Black")
        game.play_game("Lucy", (5, 2), (4, 3))
        self.assertEqual(game.get_checker_details((5, 2)), None)
        self.assertEqual(game.get_checker_details((4, 3)), "Black")
        game.play_game("Adam", (2, 1), (3, 2))
        self.assertEqual(game.get_checker_details((2, 1)), None)
        self.assertEqual(game.get_checker_details((3, 2)), "White")

    def test_more_simple_moves_and_keep_turn(self):
        game = Checkers()
        Player1 = game.create_player("Adam", "White")
        Player2 = game.create_player("Lucy", "Black")
        game.play_game("Lucy", (5, 2), (4, 1))
        game.play_game("Adam", (2, 1), (3, 2))
        game.play_game("Lucy", (6, 1), (5, 2))
        game.play_game("Adam", (2, 5), (3, 6))
        game.play_game("Lucy", (5, 6), (4, 7))
        game.play_game("Adam", (1, 6), (2, 5))
        game.play_game("Lucy", (6, 5), (5, 6))
        game.play_game("Adam", (3, 2), (4, 3))
        game.play_game("Lucy", (5, 2), (3, 4))
        game.play_game("Lucy", (3, 4), (1, 6))
        self.assertEqual(Player2.get_captured_pieces_count(), 2)

    def test_full_game(self):
        """Test promote king, promote triple king, capture pieces, and declare game winner"""
        game = Checkers()
        Player1 = game.create_player("Adam", "White")
        Player2 = game.create_player("Lucy", "Black")
        game.play_game("Lucy", (5, 0), (4, 1))
        game.play_game("Adam", (2, 5), (3, 4))
        game.play_game("Lucy", (4, 1), (3, 0))
        game.play_game("Adam", (2, 1), (3, 2))
        game.play_game("Lucy", (5, 4), (4, 5))
        game.play_game("Adam", (1, 4), (2, 5))
        game.play_game("Lucy", (6, 1), (5, 0))
        game.play_game("Adam", (0, 3), (1, 4))
        game.play_game("Lucy", (6, 5), (5, 4))
        game.play_game("Adam", (2, 5), (3, 6))
        game.play_game("Lucy", (5, 2), (4, 1))
        game.play_game("Adam", (1, 2), (2, 1))
        game.play_game("Lucy", (4, 1), (3, 0))
        game.play_game("Adam", (3, 4), (4, 3))
        game.play_game("Lucy", (7, 4), (6, 5))
        game.play_game("Adam", (4, 3), (5, 2))
        game.play_game("Lucy", (6, 3), (4, 1))
        game.play_game("Adam", (3, 2), (5, 0))
        game.play_game("Lucy", (7, 2), (6, 1))
        game.play_game("Adam", (5, 0), (7, 2))
        self.assertEqual(Player1.get_king_count(), 1)
        game.play_game("Lucy", (3, 0), (1, 2))
        game.play_game("Adam", (2, 3), (3, 4))
        game.play_game("Lucy", (4, 5), (2, 3))
        game.play_game("Adam", (1, 4), (3, 2))
        game.play_game("Lucy", (5, 6), (4, 5))
        game.play_game("Adam", (0, 1), (2, 3))
        game.play_game("Lucy", (5, 4), (5, 6))
        game.play_game("Adam", (7, 2), (6, 1))
        game.play_game("Lucy", (7, 0), (5, 2))
        self.assertEqual(Player1.get_king_count(), 0)
        game.play_game("Adam", (3, 2), (4, 3))
        game.play_game("Lucy", (5, 2), (3, 4))
        game.play_game("Lucy", (3, 4), (1, 2))
        game.play_game("Adam", (0, 7), (2, 5))
        game.play_game("Lucy", (6, 5), (5, 4))
        game.play_game("Adam", (3, 6), (4, 5))
        game.play_game("Lucy", (5, 6), (3, 4))
        game.play_game("Lucy", (3, 4), (1, 6))
        game.play_game("Adam", (2, 7), (3, 6))
        game.play_game("Lucy", (5, 4), (4, 3))
        game.play_game("Adam", (0, 5), (2, 7))
        game.play_game("Lucy", (4, 3), (3, 2))
        game.play_game("Adam", (3, 6), (4, 5))
        game.play_game("Lucy", (1, 2), (0, 1))
        self.assertEqual(Player2.get_king_count(), 1)
        game.play_game("Adam", (2, 7), (3, 6))
        game.play_game("Lucy", (3, 2), (2, 1))
        game.play_game("Adam", (1, 0), (3, 2))
        game.play_game("Lucy", (7, 6), (6, 5))
        game.play_game("Adam", (3, 2), (4, 3))
        game.play_game("Lucy", (6, 5), (5, 6))
        game.play_game("Adam", (4, 5), (5, 4))
        game.play_game("Lucy", (0, 1), (1, 0))
        game.play_game("Adam", (3, 6), (4, 5))
        game.play_game("Lucy", (1, 0), (6, 5))
        game.play_game("Adam", (4, 5), (5, 4))
        game.pretty_print_board()
        game.play_game("Lucy", (6, 5), (7, 4))
        self.assertEqual(Player2.get_king_count(), 0)
        self.assertEqual(Player2.get_triple_king_count(), 1)
        # Technically, Lucy should have captured and won last move
        #   but, want to test for triple king
        game.play_game("Adam", (5, 4), (6, 3))
        self.assertEqual(Player2.get_captured_pieces_count(), 11)
        game.play_game("Lucy", (7, 4), (5, 2))
        self.assertEqual(Player2.get_captured_pieces_count(), 12)
        self.assertEqual(game.game_winner(), "Lucy")


if __name__ == "__main__":
    unittest.main()
