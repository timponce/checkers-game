CHECKERS

checkerboard: 8x8 = 64 squares
12 piece each

BOARD

7  N  w  N  w  N  w  N  w
6  w  N  w  N  w  N  w  N
5  N  w  N  w  N  w  N  w
4  N  N  N  N  N  N  N  N
3  N  N  N  N  N  N  N  N
2  b  N  b  N  b  N  b  N
1  N  b  N  b  N  b  N  b
0  b  N  b  N  b  N  b  N
   0  1  2  3  4  5  6  7


STARTING SQUARES
WHITE
(0,0),(2,0),(4,0),(6,0)
(1,1),(3,1),(5,1),(7,1)
(0,2),(2,2),(4,2),(6,2)

ITERATE BOARD v1

board = {}
coord = [0, 0]
for i in range(0, 7):
    coord[0] = coord[0] + 1
    for j in range(0, 7):
        coord[1] = coord[1] + 1
        t_coord = tuple(coord)
        if coord[0] in {1, 2, 3}:
            if coord[1] in {
        if coord[0] in {4, 5}:
            board[t_coord] = "None"

ITERATE BOARD v2

j + i*7

i is y coordinate (row)
j is x coordinate (file)

board = {}
coord = [0, 0]
piece = "White"
for i in range(0, 8):
    if i == 5:
        piece = "Black"
    for j in range(0, 8):
        coord[0] = j
        coord[1] = i
        if i not in {3, 4} and sum(coord) % 2 == 0:
            board[tuple(coord)] = piece
        else:
            board[tuple(coord)] = "None"
return board


WHO"S TURN IS IT?

If black piece moves:
    Is there a diagonal to the left and up occupied by a white piece,
        followed by another diagonal to the left and up that is unoccupied
    Is there a diagonal to the right and up occupied by a white piece,
        followed by another diagonal to the right and up that is empty
    If any of above are true: still black's turn, else white's

If white piece moves:
    Is there a diagonal to the left and down occupied by a black piece,
        followed by another diagonal to the left and down that is unoccupied
    Is there a diagonal to the right and down occupied by a black piece,
        followed by another diagonal to the right and down that is empty
    If any of above are true: still white's turn, else black's

If any king moves:
    Is there any diagonal (left & up, right & up, left & down, right & down)
    in which there are any number of unoccupied squares (in any order) with only
    one enemy piece with at least one unoccupied square directly behind the enemy
    piece.

If any triple king moves:
    Is there any diagonal (left & up, right & up, left & down, right & down)
    in which there are any number of unoccupied squares (in any order) with exactly
    two enemy pieces next to each other on the diagonal with at least one unoccupied 
    square directly behind the enemy pieces.

Can i use a generator to trace diagonals?
    step
        up-left
        up-right
        down-left
        down-right

Main diagonal stepper function
    which direction 4 functions with inheritance?
    what are parameters?
    coord = (starting_square)
    stop_flag = False
    while not stop_flag:
        coord = [coord[0] x_step, coord[1] + y_step]
        yield coord


b (2, 2), (1, 3)
w (1, 5), (2, 4)
b (1, 1), (2, 2)
w (5, 5), (6, 4)
b (6, 2), (7, 3)
w (6, 6), (5, 5)
b (5, 1), (6, 2)
w (2, 4), (3, 3)
b (2, 2), (4, 4) forced to make another move


    def diagonal_stepper(self, square, direction):
        """
        Generator function that steps through board diagonally
        Starting from the given square, moves in a given direction and calls
            get_checker_details method to find what is at the next square
        Can be called multiple times to find if another move is possible and thus,
            a player must continue their turn

        Parameters:
            square
            direction
        Returns:
            information about next square in given direction

        While some stop_flag is not True,
            increment coordinates based on the direction given from the
            starting square, to the next adjacent square.
            call get_checker_details with new coordinates
                return checker details

        ***NOTE***
        After reading some Ed Discussions, it seems an easier method for determining if
            a player can go again is to check if the same color piece moves again and captures
            a piece.
        This is because we assume the player is aware of and following the rules, and thus
            the player will continue to capture when able.
        Therefore, we only raise an OutofTurn exception if a player makes a non-capturing move
            after they have already moved (to my understanding).
        However, I would like to try this method because it seems more robust and could be used
            in other situations, like maybe implementing a simple program that can make moves
            for a one player game
        """
        possible_directions = {
            "up-left": [-1, +1],
            "up-right": [+1, +1],
            "down-left": [-1, -1],
            "down-right": [+1, -1]
        }
        pass

    def check_possible_moves(self, current_location, piece):
        """
        Check if more moves are possible by calling self.diagonal_stepper

        Parameters:
            current_location
            piece
        Returns:
            Boolean

        Three cases:
        (1) For standard piece:
                Call diagonal stepper only in the two possible forward directions
                If return value is an opponent piece,
                    Call again in same direction,
                    If empty space, return True
                    else, return False
                else, return False
        (2) For king piece:
                Call diagonal stepper in all four directions
                For each direction, continue calling whilst storing the return values in 
                    successive order in 4 different arrays for the 4 different directions
                Next, initialize a stop flag to False
                
                rec_king_poss_move(self, value):
                    if value == none:
                        rec_king_poss_move(self, next value)
                
                While stop flag is False,
                    For each array,
                        Iterate through the array
                        If value is a friendly piece,
                            set stop flag to True
                        If value is none,
                        
                If return value is an opponent piece.
                    Call again in same direction,
                    If empty space, return True
                    else, return False
                else, return False
                
        (3) For Triple King piece:
                Ditto king piece above
                In addition:
                If return value is
        """