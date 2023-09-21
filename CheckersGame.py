# Author: Timothy Ponce
# GitHub Username: timponce
# Date: 2023-03-19
# Description: Two player checkers game


class OutofTurn(Exception):
    """Raised when a player attempts to move a piece out of turn"""

    pass


class InvalidSquare(Exception):
    """
    Raised when a player attempts to move a piece they do not own or to/from a square that
    does not exist on the board
    """

    pass


class InvalidMove(Exception):
    """Raised when a player makes an invalid move"""

    pass


def sum_tuple(tup):
    """Returns the sum of all elements in a given tuple"""
    tup_sum = 0
    for i in tup:
        tup_sum += i
    return tup_sum


def step_coord(tup, stepper):
    return tup[0] + stepper[0], tup[1] + stepper[1]


import pyxel

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

TILE_WIDTH = 32
TILE_HEIGHT = 32


class Checker:
    def __init__(self, file, rank, color):
        self._file = file
        self._rank = rank
        self._color = color
        self._is_active = True
        self._piece_type = "standard"

    def draw(self):
        pyx_u = 0
        pyx_v = 0

        if self._color == "black":
            pyx_v = 32
        else:
            pyx_v = 0

        if self._piece_type == "standard":
            pyx_u = 0
        elif self._piece_type == "king":
            pyx_u = 32

        if self._is_active:
            pyxel.blt(
                self._file * TILE_WIDTH,
                SCREEN_HEIGHT - TILE_HEIGHT - (self._rank * TILE_HEIGHT),
                0,
                pyx_u,
                pyx_v,
                TILE_WIDTH,
                TILE_HEIGHT,
                4,
            )

    def get_coordinates(self):
        return (self._file, self._rank)

    def get_color(self):
        return self._color

    def get_status(self):
        return self._is_active

    def get_piece_type(self):
        return self._piece_type

    def set_coordinates(self, coordinates):
        x, y = coordinates
        self._file = x
        self._rank = y

    def set_status(self, new_status):
        self._is_active = new_status

    def set_piece_type(self, updated_type):
        self._piece_type = updated_type


class Player:
    def __init__(self, color):
        self._color = color
        self._pieces = {"standard": 12, "king": 0, "captured": 0}

    def get_piece_color(self):
        """Returns piece color"""
        return self._color

    def get_standard_count(self):
        """Returns the number of standard pieces that the player has"""
        return self._pieces["standard"]

    def get_king_count(self):
        """Returns the number of king pieces that the player has"""
        return self._pieces["king"]

    def get_captured_count(self):
        """Returns the number of opponent pieces that the player has captured"""
        return self._pieces["captured"]

    def inc_standard_count(self, val):
        """Updates the number of standard pieces that the player has"""
        self._pieces["standard"] += val

    def inc_king_count(self, val):
        """Updates the number of king pieces that the player has"""
        self._pieces["king"] += val

    def inc_captured_count(self, val):
        """Updates the number of opponent pieces that the player has captured"""
        self._pieces["captured"] += val


class Board:
    """Represents a checkers board"""

    def __init__(self):
        self._board = self.init_board()

    def draw(self):
        for i in range(0, 8):
            for j in range(0, 8):
                if i % 2 == 0:
                    if j % 2 == 0:
                        pyxel.rect(
                            i * TILE_WIDTH, j * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT, 15
                        )
                    else:
                        pyxel.rect(
                            i * TILE_WIDTH, j * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT, 4
                        )
                else:
                    if j % 2 == 1:
                        pyxel.rect(
                            i * TILE_WIDTH, j * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT, 15
                        )
                    else:
                        pyxel.rect(
                            i * TILE_WIDTH, j * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT, 4
                        )
        for checker in self._board.values():
            if checker is not None:
                checker.draw()

    def init_board(self):
        """Initialize checkers board with pieces"""
        board = {}
        coord = [0, 0]
        color = "black"
        for RANK in range(0, 8):
            if RANK == 5:
                color = "white"
            for FILE in range(0, 8):
                coord[0] = FILE
                coord[1] = RANK
                if RANK not in {3, 4} and sum(coord) % 2 == 0:
                    board[tuple(coord)] = Checker(FILE, RANK, color)
                else:
                    board[tuple(coord)] = None
        return board

    def is_playable(self, coordinates):
        """Checks if the given coordinates are playable"""
        x, y = coordinates
        if not 0 <= x <= 7 or not 0 <= y <= 7:
            raise InvalidSquare("This square does not exist")
        if not sum_tuple(coordinates) % 2 == 0:
            raise InvalidSquare("This square is not playable")
        return True

    def get_square_details(self, coordinates):
        """
        Given x, y coordinates, returns:
            Checker object if found
            None if square is empty and playable
            InvalidSquare exception if not playable or outside of board range
        """
        if self.is_playable(coordinates):
            return self._board[coordinates]

    def remove_from_board(self, coordinates):
        """Removes the piece at the given coordinates"""
        if self.is_playable(coordinates):
            checker = self._board[coordinates]
            checker.set_status(False)
            self._board[coordinates] = None

    def add_to_board(self, coordinates, checker):
        """Adds the given piece at the given coordinates"""
        if self.is_playable(coordinates) and not self.get_square_details(coordinates):
            self._board[coordinates] = checker
        else:
            raise InvalidSquare("A piece already exists at this square")

    def move_piece(self, starting_coordinates, ending_coordinates, checker):
        """Moves the given piece from the starting coordinates to the ending coordinates"""
        if (
            self.is_playable(starting_coordinates)
            and self.is_playable(ending_coordinates)
            and not self.get_square_details(ending_coordinates)
        ):
            checker.set_coordinates((ending_coordinates))
            self._board[starting_coordinates] = None
            self._board[ending_coordinates] = checker
        else:
            raise InvalidSquare("A piece already exists at this square")

    def promote_piece(self, coordinates):
        """Promote a piece at the given coordinates"""
        x, y = coordinates
        checker = self.get_square_details(coordinates)
        piece_type = checker.get_piece_type()
        if self.is_playable(coordinates) and checker and checker.get_status():
            if piece_type == "standard":
                checker.set_piece_type("king")

    def print_board(self):
        """Prints the current board as an array of arrays of rows"""
        all_pieces = [
            self._board[key].get_color()[:2] if self._board[key] else None
            for key in sorted(self._board.keys(), key=lambda a: a[1], reverse=False)
        ]
        current_board = [all_pieces[i : i + 8] for i in range(0, 64, 8)]
        for each_row in current_board:
            print(each_row)


class App:
    """A game of checkers between two players"""

    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Checkers", capture_scale=1)
        pyxel.mouse(True)
        pyxel.load("assets/resources.pyxres")
        self._select_error = False
        self._error_capture_time = 0

        self._hovered_file = None
        self._hovered_rank = None
        self._selected_file = None
        self._selected_rank = None

        self._board = Board()
        self._players = [Player("black"), Player("white")]
        self._player_turn = self._players[0]
        self._last_move = {
            "color": None,
            "starting_square": None,
            "ending_square": None,
        }
        self._game_winner = False

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self._hovered_file = pyxel.mouse_x // TILE_WIDTH
        self._hovered_rank = pyxel.mouse_y // TILE_HEIGHT

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x, y = pyxel.mouse_x // TILE_WIDTH, pyxel.mouse_y // TILE_HEIGHT
            if self._selected_file is not None and self._selected_rank is not None:
                try:
                    if not self._board.get_square_details((x, 7 - y)):
                        self.play_game(
                            self._board.get_square_details(
                                (self._selected_file, self._selected_rank)
                            ).get_color(),
                            (self._selected_file, self._selected_rank),
                            (x, 7 - y),
                        )
                except:
                    pass

            try:
                if self._board.get_square_details((x, 7 - y)):
                    self._selected_file, self._selected_rank = x, 7 - y
                    self._select_error = False
            except:
                self._select_error = "INVALID SQUARE"
                self._error_capture_time = pyxel.frame_count

            # self._board.print_board()

    def draw(self):
        pyxel.cls(0)
        self._board.draw()

        if self._select_error and pyxel.frame_count - self._error_capture_time < 90:
            pyxel.text(
                99,
                112,
                self._select_error,
                0 if pyxel.frame_count % 30 < 25 else 7,
            )

        if self._game_winner:
            pyxel.text(
                99,
                112,
                f"{self._game_winner.upper()} WINS!!",
                0 if pyxel.frame_count % 30 < 25 else 7,
            )

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x = pyxel.mouse_x // TILE_WIDTH
            y = (SCREEN_HEIGHT - pyxel.mouse_y) // TILE_HEIGHT

        if self._selected_file is not None and self._selected_rank is not None:
            pyxel.blt(
                self._selected_file * TILE_WIDTH,
                SCREEN_HEIGHT - TILE_HEIGHT - (self._selected_rank * TILE_HEIGHT),
                0,
                32,
                64,
                TILE_WIDTH,
                TILE_HEIGHT,
                0,
            )

        pyxel.blt(
            self._hovered_file * TILE_WIDTH,
            self._hovered_rank * TILE_HEIGHT,
            0,
            0,
            64,
            TILE_WIDTH,
            TILE_HEIGHT,
            0,
        )

    def change_turn(self):
        """Change player who's turn it is"""
        for i in range(len(self._players)):
            if self._players[i] != self._player_turn:
                self._player_turn = self._players[i]
                break

    def play_game(
        self, checker_color, starting_square_location, destination_square_location
    ):
        """Plays a move"""
        player = None
        opponent = None
        for i, a_player in enumerate(self._players):
            if a_player.get_piece_color() == checker_color:
                player = a_player
                j = 0 if i == 1 else 1
                opponent = self._players[j]
                break
        pieces_captured = 0

        # set home and opponent ranks
        player_home_rank = 0
        opponent_home_rank = 7
        if checker_color == "white":
            player_home_rank, opponent_home_rank = opponent_home_rank, player_home_rank

        # check if the starting square is valid and owned by player/is valid
        player_checker = self._board.get_square_details(starting_square_location)
        if self._board.get_square_details(starting_square_location) and checker_color:
            if checker_color != player_checker.get_color():
                raise InvalidSquare("Invalid starting square")

        # check if destination square is playable and is not occupied
        try:
            self._board.is_playable(
                destination_square_location
            ) and not self._board.get_square_details(destination_square_location)
        except:
            self._select_error = "INVALID SQUARE"
            self._error_capture_time = pyxel.frame_count

        # determine valid moves along piece's diagonal(s)
        valid_destinations = []

        this_square = starting_square_location
        stepper = [None, None]

        if checker_color == "black":
            stepper[1] = 1
        else:
            stepper[1] = -1

        stepper[0] = 1
        for i in range(6):
            this_square = step_coord(this_square, stepper)
            valid_destinations.append(this_square)

        this_square = starting_square_location
        stepper[0] = -1
        for i in range(6):
            this_square = step_coord(this_square, stepper)
            valid_destinations.append(this_square)

        if player_checker.get_piece_type() == "king":
            this_square = starting_square_location
            stepper[1] = -1 * stepper[1]
            stepper[0] = 1
            for i in range(6):
                this_square = step_coord(this_square, stepper)
                valid_destinations.append(this_square)

            this_square = starting_square_location
            stepper[0] = -1
            for i in range(6):
                this_square = step_coord(this_square, stepper)
                valid_destinations.append(this_square)

        if destination_square_location not in valid_destinations:
            self._select_error = "ILLEGAL MOVE"
            self._error_capture_time = pyxel.frame_count
            raise InvalidMove("This is not a legal move")

        # check for captures
        squares_jumped = (
            abs(destination_square_location[1] - starting_square_location[1]) - 1
        )
        stepper = [+1, +1]
        this_square = starting_square_location
        if destination_square_location[0] < starting_square_location[0]:
            stepper[0] = -1
        if destination_square_location[1] < starting_square_location[1]:
            stepper[1] = -1

        if squares_jumped == 0 and self._last_move["color"] == checker_color:
            self._select_error = "NOT THIS PLAYER'S TURN"
            self._error_capture_time = pyxel.frame_count
            raise OutofTurn("It is not this player's turn")

        for i in range(squares_jumped):
            this_square = step_coord(this_square, stepper)
            this_piece = self._board.get_square_details(this_square)

            if squares_jumped > 1 or (squares_jumped == 1 and this_piece is None):
                self._select_error = "ILLEGAL MOVE"
                self._error_capture_time = pyxel.frame_count
                raise InvalidMove("This is not a legal move")

            if this_piece is not None:
                if this_piece.get_color() == checker_color:
                    self._select_error = "ILLEGAL MOVE"
                    self._error_capture_time = pyxel.frame_count
                    raise InvalidMove("This is not a legal move")

                if self._last_move["color"] == checker_color and not (
                    self._last_move["ending_square"] == starting_square_location
                    and this_piece.get_color() == opponent.get_piece_color()
                ):
                    self._select_error = "NOT THIS PLAYER'S TURN"
                    self._error_capture_time = pyxel.frame_count
                    raise OutofTurn("It is not this player's turn")

                if this_piece.get_piece_type() == "king":
                    opponent.inc_king_count(-1)
                else:
                    opponent.inc_standard_count(-1)
                pieces_captured += 1
                self._board.remove_from_board(this_square)

        player.inc_captured_count(pieces_captured)

        self._last_move["color"] = player.get_piece_color()
        self._last_move["starting_square"] = starting_square_location
        self._last_move["ending_square"] = destination_square_location

        self._selected_file = None
        self._selected_rank = None

        # update board and check for promotions
        # if opponent home row, piece == king
        # else, piece == piece
        if (
            destination_square_location[1] == opponent_home_rank
            and player_checker.get_piece_type() == "standard"
        ):
            player.inc_standard_count(-1)
            player.inc_king_count(1)
            player_checker.set_piece_type("king")

        self._board.move_piece(
            starting_square_location, destination_square_location, player_checker
        )

        if player.get_captured_count() == 12:
            self._game_winner = checker_color

        return

    def game_winner(self):
        """Returns the winner of the game, if the game is over"""
        for i in range(len(self._players)):
            if self._players[i].get_captured_count() == 12:
                return self._players[i]
        return "Game has not ended"


App()
