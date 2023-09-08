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


class Checkers:
    """something"""

    def __init__(self):
        self._board = self.create_board()
        self._players = []
        self._last_move = {"player": None, "starting_square": None, "ending_square": None}

    def create_board(self):
        """Initialize checkers board with pieces"""
        board = {}
        coord = [0, 0]
        piece = "White"
        for i in range(0, 8):
            if i == 5:
                piece = "Black"
            for j in range(0, 8):
                coord[1] = j
                coord[0] = i
                if i not in {3, 4} and sum(coord) % 2 != 0:
                    board[tuple(coord)] = piece
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

    def play_game(self, player_name, starting_square_location, destination_square_location):
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
        squares_jumped = abs(destination_square_location[1] - starting_square_location[1]) - 1
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
                self._last_move["ending_square"] == starting_square_location and pieces_captured > 0):
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
        all_pieces = [self._board[key] for key in sorted(self._board.keys(), key=lambda a: a[0], reverse=False)]
        current_board = [all_pieces[i:i + 8] for i in range(0, 64, 8)]
        print(current_board)

    def game_winner(self):
        """Returns the winner of the game, if the game is over"""
        for i in range(len(self._players)):
            if self._players[i].get_captured_pieces_count() == 12:
                return self._players[i].get_player_name()
        return "Game has not ended"

    def pretty_print_board(self):
        """Pretty prints the current board"""
        all_pieces = [self._board[key] for key in sorted(self._board.keys(), key=lambda a: a[0], reverse=False)]
        all_symbols = [
            "\033[97m\033[7m   \033[0m" if val == "White" else "\033[97m\033[7m k \033[0m" if val == "White_king"
            else "\033[97m\033[7m K \033[0m" if val == "White_Triple_King" else "\033[90m\033[7m\033[1m   \033[0m"
            if val == "Black" else "\033[90m\033[7m\033[1m k \033[0m" if val == "Black_king" else
            "\033[90m\033[7m\033[1m K \033[0m" if val == "Black_Triple_King" else "   " for val in all_pieces]
        print()
        print(f"   +  -  +  -  +  -  +  -  +  -  +  -  +  -  +  -  +")
        for i in range(0, 64, 4):
            if i % 8 == 0:
                print(f"\033[1m{int(i/8)}\033[0m  | {' | '.join(all_symbols[i:i + 8])} | ")
            else:
                print(f"   +  -  +  -  +  -  +  -  +  -  +  -  +  -  +  -  +")
        print("\033[1m      0     1     2     3     4     5     6     7\033[0m")
        print()


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


game = Checkers()
game.pretty_print_board()