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


class InvalidPlayer(Exception):
    """Raised if player_name is not valid"""

    pass


class ExceedPlayerCount(Exception):
    """Raised when a third player is attempted to be added"""

    pass


class InvalidColor(Exception):
    """Raised when a player attempts to use a color that is already associated with another player"""

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
    def __init__(self, file, rank, color, status):
        self.file = file
        self.rank = rank
        self.color = color
        self.status = status

    def draw(self):
        pyx_u = 0
        pyx_v = 0

        if self.color == "Black":
            pyx_v = 32
        else:
            pyx_v = 0

        if self.status == "standard":
            pyx_u = 0
        elif self.status == "king":
            pyx_u = 32
        else:
            pyx_u = 64

        pyxel.blt(
            self.file * TILE_WIDTH,
            self.rank * TILE_HEIGHT,
            0,
            pyx_u,
            pyx_v,
            TILE_WIDTH,
            TILE_HEIGHT,
            4,
        )


class Selector:
    def __init__(self):
        self.hovered_file = 0
        self.hovered_rank = 0
        self.selected_file = -1
        self.selected_rank = -1

    def update(self):
        self.hovered_file = pyxel.mouse_x // TILE_WIDTH
        self.hovered_rank = pyxel.mouse_y // TILE_HEIGHT

    def draw(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.selected_file = pyxel.mouse_x // TILE_WIDTH
            self.selected_rank = pyxel.mouse_y // TILE_HEIGHT

        if self.selected_file >= 0 and self.selected_rank >= 0:
            pyxel.blt(
                self.selected_file * TILE_WIDTH,
                self.selected_rank * TILE_HEIGHT,
                0,
                32,
                64,
                TILE_WIDTH,
                TILE_HEIGHT,
                0,
            )

        pyxel.blt(
            self.hovered_file * TILE_WIDTH,
            self.hovered_rank * TILE_HEIGHT,
            0,
            0,
            64,
            TILE_WIDTH,
            TILE_HEIGHT,
            0,
        )


class Checkers:
    """A game of checkers between two players"""

    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Checkers", capture_scale=1)
        pyxel.mouse(True)
        pyxel.load("assets/resources.pyxres")

        self.selector = Selector()

        self._board = self.create_board()
        self._players = []
        self._last_move = {
            "player": None,
            "starting_square": None,
            "ending_square": None,
        }

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.selector.update()

    def draw(self):
        pyxel.cls(0)
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
        self.selector.draw()

    def create_board(self):
        """Initialize checkers board with pieces"""
        board = {}
        coord = [0, 0]
        color = "White"
        for i in range(0, 8):
            if i == 5:
                color = "Black"
            for j in range(0, 8):
                coord[1] = j
                coord[0] = i
                if i not in {3, 4} and sum(coord) % 2 != 0:
                    board[tuple(coord)] = Checker(j, i, color, "standard")
                else:
                    board[tuple(coord)] = None
        return board

    def create_player(self, player_name, piece_color):
        """Creates and returns a player"""
        if piece_color not in {"White", "Black"}:
            raise InvalidColor("This is not a valid color")

        num_players = len(self._players)
        if num_players == 0:
            player = Player(player_name, piece_color)
            self._players.append(player)
        elif num_players == 1:
            if self._players[0].get_piece_color() != piece_color:
                player = Player(player_name, piece_color)
                self._players.append(player)
            else:
                raise InvalidColor("This color has already been chosen")
        else:
            raise ExceedPlayerCount("There can only be two players per game")

        if piece_color == "Black":
            self._player_turn = player
        return player

    def get_player(self, player_name):
        """Returns player name and piece color in tuple"""
        for i in range(len(self._players)):
            if self._players[i].get_player_name() == player_name:
                return self._players[i]
        raise InvalidPlayer("This player does not exist")

    def change_turn(self):
        """Change player who's turn it is"""
        for i in range(len(self._players)):
            if self._players[i] != self._player_turn:
                self._player_turn = self._players[i]
                break

    def play_game(
        self, player_name, starting_square_location, destination_square_location
    ):
        """Plays a move"""

        # check player_name exists
        player = self.get_player(player_name)
        for i in range(len(self._players)):
            if player != self._players[i]:
                opponent = self._players[i]
        player_color = player.get_piece_color()
        pieces_captured = 0

        # set home and opponent ranks
        player_home_rank = 7
        opponent_home_rank = 0
        if player_color == "White":
            temp = player_home_rank
            player_home_rank = opponent_home_rank
            opponent_home_rank = temp

        # check if the starting square is valid and owned by player/is valid
        if self.get_checker_details(starting_square_location):
            if player_color not in self.get_checker_details(starting_square_location):
                raise InvalidSquare("Invalid starting square")

        # check if destination square exists/is valid
        self.get_checker_details(destination_square_location)

        player_piece = self.get_checker_details(starting_square_location)

        # update board and check for promotions
        self._board[starting_square_location] = None
        # if opponent home row, piece == king
        # if home row, piece == triple king
        # else, piece == piece
        if destination_square_location[0] == opponent_home_rank:
            self._board[destination_square_location] = f"{player_color}_king"
            player.inc_king_count(1)
            change_turn_bool = False
        elif destination_square_location[0] == player_home_rank:
            self._board[destination_square_location] = f"{player_color}_Triple_King"
            player.inc_king_count(-1)
            player.inc_triple_king_count(1)
            change_turn_bool = False
        else:
            self._board[destination_square_location] = player_piece

        # check for captures
        squares_jumped = (
            abs(destination_square_location[1] - starting_square_location[1]) - 1
        )
        stepper = [-1, +1]
        this_square = starting_square_location
        if destination_square_location[0] > starting_square_location[0]:
            stepper[0] = +1
        if destination_square_location[1] < starting_square_location[1]:
            stepper[1] = -1
        for i in range(squares_jumped):
            this_square = step_coord(this_square, stepper)
            this_piece = self.get_checker_details(this_square)
            if this_piece is not None:
                if "_king" in this_piece:
                    opponent.inc_king_count(-1)
                elif "_Triple_King" in this_piece:
                    opponent.inc_triple_king_count(-1)
                pieces_captured += 1
                self._board[tuple(this_square)] = None

        # check out of turn
        if self._last_move["player"] == player and not (
            self._last_move["ending_square"] == starting_square_location
            and pieces_captured > 0
        ):
            raise OutofTurn("It is not this player's turn")

        player.inc_captured_pieces_count(pieces_captured)

        self._last_move["player"] = player
        self._last_move["starting_square"] = starting_square_location
        self._last_move["ending_square"] = destination_square_location

        return pieces_captured

    def get_checker_details(self, square_location):
        """Returns the piece that is on a square"""
        if not 0 <= square_location[0] <= 7 or not 0 <= square_location[1] <= 7:
            raise InvalidSquare("This square does not exist")
        elif sum_tuple(square_location) % 2 == 0:
            raise InvalidSquare("This square is not playable")
        else:
            return self._board[square_location]

    def print_board(self):
        """Prints the current board as an array of arrays of rows"""
        all_pieces = [
            self._board[key]
            for key in sorted(self._board.keys(), key=lambda a: a[0], reverse=False)
        ]
        current_board = [all_pieces[i : i + 8] for i in range(0, 64, 8)]
        print(current_board)

    def game_winner(self):
        """Returns the winner of the game, if the game is over"""
        for i in range(len(self._players)):
            if self._players[i].get_captured_pieces_count() == 12:
                return self._players[i].get_player_name()
        return "Game has not ended"


class Player:
    """Represents a player of the game Checkers"""

    def __init__(self, player_name, piece_color):
        self._player_name = player_name
        self._piece_color = piece_color
        self._player_pieces = {"king": 0, "triple king": 0, "captured": 0}

    def get_player_name(self):
        """Returns the player name"""
        return self._player_name

    def get_piece_color(self):
        """Returns piece color"""
        return self._piece_color

    def get_king_count(self):
        """Returns the number of king pieces that the player has"""
        return self._player_pieces["king"]

    def inc_king_count(self, val):
        """Updates the number of king pieces that the player has"""
        self._player_pieces["king"] += val

    def get_triple_king_count(self):
        """Returns the number of triple king pieces that the player has"""
        return self._player_pieces["triple king"]

    def inc_triple_king_count(self, val):
        """Updates the number of triple king pieces that the player has"""
        self._player_pieces["triple king"] += val

    def get_captured_pieces_count(self):
        """Returns the number of opponent pieces that the player has captured"""
        return self._player_pieces["captured"]

    def inc_captured_pieces_count(self, val):
        """Updates the number of opponent pieces that the player has captured"""
        self._player_pieces["captured"] += val


Checkers()
