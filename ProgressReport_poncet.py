# Author: Timothy Ponce
# GitHub Username: timponce
# Date: 2023-03-08
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


class Checkers:
    """A class to represent the checkers game. Uses Player class."""

    def __init__(self):
        self._board = self.create_board()
        self._players = []
        self._player_turn = "None"
        self._last_move = []

    def create_board(self):
        """
        Initialize checkers board with pieces.

        Parameters:
            none
        Returns:
            a dictionary representing a checkers board in the starting position

        This method is called as soon as a Checkers class is created to create the board.
        Create a dictionary, then for each of the 8 rows, increment the y coordinate,
            for each of the 8 squares in each row, increment the x coordinate,
            if not in middle two rows, check if the sum of the coordinates is even,
                place a piece (color dependent on which row currently in).
            update library with coordinates and piece as key value pair.
        """
        pass

    def create_player(self, player_name, piece_color):
        """
        Creates and returns a player

        Parameters:
            player_name
            piece_color
        Returns:
            new Player class with player_name and piece_color

        uses Player class
        """
        return Player(player_name, piece_color)

    def get_player(self, player_name):
        """
        Returns player name and piece color in tuple

        Parameters:
            player_name
        Returns:
            player object of player_name

        Iterate over player array while checking if player_name in array
            If true, return player
            else, raise InvalidPlayer exception
        """

    def change_turn(self):
        """
        Change whose turn it is

        Parameters:
            none
        Returns:
            updates self._player_turn with appropriate Player object

        Get current player whose turn it is
            For each player in the players array
                If player is not currently in turn
                    set that player as in turn
        """
        pass

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """
        Plays a move

        Parameters:
            player_name
            starting_square_location
            destination_square_location
        Returns:
            the number of captured pieces, if none, then 0

        Check player name exists
            Call self.get_player(player_name)
            (this method contains error handling)
        Check for invalid square(s)
            Call self.get_checker_details for the starting square
            Call self.get_player to obtain the player color
            If player color is not in the results of the first call,
                raise InvalidSquare exception
            Call self.get_checker_details for the destination square
                This method contains error handling if the square does not exist
        Check player is in turn
            Check self._last_move,
            If player color is player color recorded in last_move
                If starting square of current move is destination square recorded in last_move
                and captured pieces of current move > 0
                    Continue
                Else,
                    Raise OutofTurnException
        Check for promotion
            If destination square has y-coordinate 7
                If piece is black,
                    update piece to king by updating key:value pair of board dictionary
                If piece is white,
                    update piece to triple king by updating key:value pair of board dictionary
            If destination square has y-coordinate 0
                If piece is black,
                    update piece to triple king by updating key:value pair of board dictionary
                If piece is white,
                    update piece to king by updating key:value pair of board dictionary
        Check for captured pieces
            Calculate absolute value of x-coordinate of starting square - destination square
            Subtract 1 to see how many spaces were jumped over by the piece
            Initialize captured_pieces to = 0
            Initialize stepper variable to [+1, +1] (default to 'up' and 'right')
            If y of destination square < y of starting square ('down' the board)
                Set stepper[1] to -1
            If x of destination square < x of starting square ('left' move on the board)
                Set stepper[0] to -1
            For each square 'jumped' in this move:
                Call get_checker_details
                If not none:
                    captured_pieces += 1
        Save current move to self._last_move with piece color, starting square, destination square
            and captured pieces saved in an array
        Return captured_pieces
        """
        pass

    def get_checker_details(self, square_location):
        """
        Returns information on which piece is in a given square

        Parameters:
            square_location
        Returns:
            piece or None, where piece can be "{color}", "{color}_king", "{color}_Triple_King"

        Check if given coordinates are outside the board range ( < 0 or > 7)
            If True,
                raise InvalidSquare exception
            Else,
                return value stored in board dictionary by the coordinate key value
        """
        if not 0 <= square_location[0] <= 7 or not 0 <= square_location[1] <= 7:
            raise InvalidSquare("This square does not exist")
        else:
            return self._board[square_location]

    def print_board(self):
        """
        Prints the current board as an array of arrays of rows

        Parameters:
            none
        Returns:
            prints to the console a single array containing 8 arrays representing board rows,
                with values corresponding to what piece, if any, occupies that space

        Because dictionaries are not stored in sequential order in memory,
        First, convert the dictionary to an array while sorting by key
        Then, for every 8 values in the array, create a new array within this array
        """
        all_pieces = [self._board[key] for key in sorted(self._board.keys(), key=lambda a: a[1], reverse=True)]
        current_board = [all_pieces[i:i + 8] for i in range(0, 64, 8)]
        print(current_board)

    def game_winner(self):
        """
        Returns the winner of the game, if the game is over

        Parameters:
            none
        Returns:
            If there is a winner, the player's name
            If there is not a winner, return "Game has not ended"

        For each player,
            if captured pieces is equal to 12, return their name
        Else,
            return "Game has not ended"
        """


class Player:
    """
    Represents a player of the game checkers.
    Is utilized by Checkers class
    """

    def __init__(self, player_name, piece_color):
        self._player_name = player_name
        self._piece_color = piece_color
        self._player_pieces = {"king": 0, "triple king": 0, "captured": 0}

    def get_piece_color(self):
        """Returns piece color"""
        return self._piece_color

    def get_king_count(self):
        """Returns the number of king pieces that the player has"""
        return self._player_pieces["king"]

    def get_triple_king_count(self):
        """Returns the number of triple king pieces that the player has"""
        return self._player_pieces["triple king"]

    def get_captured_pieces_count(self):
        """Returns the number of opponent pieces that the player has captured"""
        return self._player_pieces["captured"]


# DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS

# 1. I will initialize the Checkers class with a board represented by a dictionary with keys being the coordinates
#    and values being which piece occupies that space. I will also have an empty array to store the players that
#    will be created. I will set the players turn to None and will update when the players are created. Lastly,
#    last_move will be an empty array that will be used to store the last valid move made to reference when determining
#    if a player is out of turn. These will all be private data members.
#    The Player's class will have private data members, _player_name, _piece_color, and _player_pieces
#    the first two will be set based on the parameters given when creating a new Player object while _player_pieces
#    is a dictionary with key:value pairs of king, triple king, and captured corresponding to the values of
#    kings and triple kings a player has and the number of enemy pieces they have captured

# 2. create_player will simply return Player(player_name, piece_color) to create a new Player object

# 3. Because I chose to store the board as a dictionary with coordinates as keys and square information as
#    values, I will use list comprehension to convert this dictionary to an array. Additionally, since dictionaries
#    are not sorted like arrays are, I will have to sort them by their keys. Then, another list comprehension will
#    be used to make a single parent array wherein every 8 values are split into a new array within the single parent
#    array.

# 4. When game_winner is called, iterate through the players array. Check each of the two players to see if
#    player's captured pieces is equal to 12. If this condition is met, then we can return their name. If neither
#    player satisfies this condition, we return the message "Game has not ended"

# 5. The play_game will first have a series of checks before proceeding.
#    First, we check if the player name exists by calling the appropriate method and passing the
#    player name to it. Since this method contains error handling by comparing the player name received
#    to the player array of the Checkers object, that is all we need to do.
#    Second, we check for invalid square(s).
#    We can do this by invoking the get_checker_details method to see what color is stored there. Then
#    we can call get_player to see the player color. Comparing these two values, if the AND comparison is True,
#    then we continue, else we raise an InvalidSquare exception. For the destination square, we only have to call
#    the get_checker_details method and that method will handle if that square exists or not.
#    Third, to determine that the player is not out of turn, we refer to the last_move saved in this Checkers object
#    If, within this array, we determine that the player color of the current move is that same as the
#    player move of the last move, then we must check that this is not out of turn. If the starting square of
#    the current square shares the same coordinates as the destination square of the last move AND the number
#    of captured pieces last move is greater than 0, we can continue. Else, we raise an OutofTurn exception.
#    Now, to check for promotion we will check if the destination square has a y-coordinate of 7 or 0.
#    If y = 7, then we check piece color. If black, we update piece to king as this piece has made it to the
#    opponents 'home row'. If white, we update to triple king as this piece has made it back to its own 'home row'.
#    If y = 0, we check piece color again but with the conditions switched for each color.
#    To check for captured pieces we must determine how many squares were 'jumped' in the current move.
#    We can do this by taking the absolute value of the x coordinate of the starting square minus the x
#    coordinate of the destination square then subtracting the absolute value by 1.
#    Then, we initialize two variables: captured_pieces to 0 and stepper to [+1, +1].
#    This stepper is set to a 'forward' and 'right' move (from black's perspective. Then, we check if a 'backward/down'
#    move was made by checking if the y coordinate of the destination square is less than the y coordinate
#    of the starting square. If so, set the second value of stepper to -1. Then, we check if a 'left' move was
#    made by checking if the x coordinate of the destination square is less than the x coordinate of the
#    starting square. And if so, setting the first value of stepper to -1. Now, for each square 'jumped' in this move
#    we call get_checker_details, if None is not returned, then we increment captured_pieces by 1.
#    Finally, we can save this move to the last_move value for future reference and we
#    return the number of captured pieces.

# 6. Because I chose to store my board in a dictionary, we only need to return the value corresponding to the
#    key of the coordinates passed as a parameter. First, we check if the coordinates are valid by comparing
#    the x and y coordinates to 0 and 7, if either is outside the range [0, 7], we raise the InvalidSquare exception,
#    else we proceed with return self._board[square_location]

# 7. We initialize the exception classes as such:
#
#         class ExceptionName(Exception):
#         """Raised when some condition is met"""
#         pass
#

# WANT TO MAKE THIS PROJECT BETTER
# DIAGONAL STEPPER TO STEP THRU MOVES
"""
    def diagonal_stepper(self, square, direction):
        description: Generator function that steps through board diagonally
        possible_directions = {
            "up-left": [-1, +1],
            "up-right": [+1, +1],
            "down-left": [-1, -1],
            "down-right": [+1, -1]
        }
        x_step = possible_directions[direction][0]
        y_step = possible_directions[direction][1]
        coord = square
        stop_flag = False
        while not stop_flag:
            coord = [coord[0] + x_step, coord[1] + y_step]
            try:
                piece = self.get_checker_details(coord)
                yield piece
            except:
                yield False
                
"""

"""
def check_possible_moves(self, current_location, piece):

    description: 
    Check if more moves are possible
    Returns True if so, else returns False

    any_moves = False
    if piece == "Black":
        step_1 = next(self.diagonal_stepper(current_location, "up-left"))
        if step_1 == "White":
            step_2 = next(self.diagonal_stepper(current_location, "up-left"))
            if step_2 == "None":
                any_moves = True
    if piece == "Black":
        step_3 = next(self.diagonal_stepper(current_location, "up-right"))
        if step_1 == "White":
            step_4 = next(self.diagonal_stepper(current_location, "up-right"))
            if step_2 == "None":
                any_moves = True
    return any_moves
"""
