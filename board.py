from piece import Piece, Grid_Point

#
class Board:
    '''
    Main board class, contains all info on board state plus functions to allow board state modification within rules

    Attributes:

    grid_values [[pieces]]: 2d list containing all pieces and none which represents entire board
    piece_dirs[[[int]]]: 2d list that contains a list of directions in which pieces would get flipped if a piece gets placed at a position
    O_num int: number of O pieces
    X_num int: number of X pieces
    dimensions (int, int): dimensions of the board

    Methods:

    get_available_moves(player): returns a list of all available moves for a player and updates the piece_dirs list
    add_piece(pos, player): adds a piece at a position. Updates board state, flips pieces, and updates counts
    get_piece(i, j): returns the player string ('X' or 'O') for who owns a piece at a position i, j
    is_valid_move(i, j, player): returns None if its an invalid move for player. Otherwise returns a list of ints representing directions in which pieces would be flipped
    flip_piece(i, j): flips a piece to the other player
    count_pieces(): updates O_num and X_num attributes based on current piece count on board
    get_piece_count(): returns a tuple containing the O and X piece counts
    '''
    def __init__(self, size):
        '''
        Board constructor

        ARGS: 
            size (int): size of the square board
        '''

        self.dimensions = (size, size)

        #variables for holding the number of each piece on the board
        self.O_num = 2
        self.X_num = 2

        #grid values array contains the info for every cell, its either an X piece, an O piece, or None
        self.grid_values = []

        #piece_dirs holds the directions in which pieces would get flipped if a piece was placed here for the current player
        self.piece_dirs = []

        #initialize both lists as empty
        for i in range(size):
            self.grid_values.append([])
            self.piece_dirs.append([])
            for j in range(size):
                self.grid_values[i].append(None)
                self.piece_dirs[i].append(None)

        #create the starting 4 pieces
        self.grid_values[size//2 - 1][size//2 - 1] = Piece(size//2 - 1, size//2 - 1, 'O')
        self.grid_values[size//2][size//2] = Piece(size//2, size//2, 'O')
        self.grid_values[size//2][size//2 - 1] = Piece(size//2, size//2 - 1, 'X')
        self.grid_values[size//2 - 1][size//2] = Piece(size//2 - 1, size//2, 'X')

    def __str__(self):
        '''
        Board String method

        RETURNS:
            (str): string representation of the board for printing
        '''
        #create the return string with starting whitespace for top row labels
        return_string = '   '

        #add the column labels to the first line of the string
        for i in range(1, self.dimensions[0] + 1):
            return_string += f'  {i} '
        return_string += '\n'

        i = 1
        for row in self.grid_values:
            #add a horizontal row of dashes offset slighlty for each row
            return_string += ('   ' + '-' * 4 * self.dimensions[0] + '-\n')

            #print the row label
            return_string += f' {i} '
            i+=1

            #print the value of each piece in the grid if it exists properly spaced with vertical seperation
            for piece in row:
                return_string += '|'
                if(piece):
                    return_string += f' {piece} '
                else:
                    return_string += '   '
            return_string += '|\n'
        return_string += ('   ' + '-' * 4 * self.dimensions[0] + '-\n')

        return return_string
    
    def get_available_moves(self, player):
        '''
        returns all availabe moves for a player

        ARGS:
            player (str): either 'X' or 'O' depending on which player's turn it is
        RETURNS:
            [(int, int)]: a list of tuples containing all possible moves (1 indexed)
        '''
        possible_moves = []

        #loop through entire board
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[0]):
                #get the flip directions for each position on the board for that player
                self.piece_dirs[i][j] = self.is_valid_move(i, j, player)

                #if its not None for a cell, append that cell to possible moves as it is legal
                if(self.piece_dirs[i][j]):
                    possible_moves.append((i + 1, j + 1))


        return possible_moves

    def add_piece(self, pos, player):
        '''
        Adds a piece for a player to the board to a position

        ARGS:
            pos ((int, int) or Grid_Point): position for piece to be placed, can be a tuple or grid_point
            player (str): 'X' or 'O' for which player is placing a piece
        '''

        #tuples passed will always be 0 indexed while grid_points will be 1 indexed
        offset = 0

        #if the position is a grid_point, it needs to be offset down by 1 to access array
        if(isinstance(pos, Grid_Point)):
            offset = 1
        
        #flip all pieces needed due to placement and the position
        self.turn_pieces(pos[0] - offset, pos[1] - offset, player)

        #add the piece to grid values
        self.grid_values[pos[0] - offset][pos[1] - offset] = Piece(pos[0] - offset, pos[1] - offset, player)

        #recount pieces as the board state has changed
        self.count_pieces()

    def get_piece(self, i, j):
        '''
        gets a position's piece's player

        ARGS:
            i, j (int, int): position at which to get piece

        RETURNS:
            (str): 'X', 'O', or None depending on which player owns the piece or if there is a piece at all
        '''
        if(self.grid_values[i][j]):
            return self.grid_values[i][j].get_value()
        else:
            return None

    def is_valid_move(self, i, j, player):
        '''
        Function which checks if a move is valid

        ARGS:
            i, j (int, int): position which to check
            player (str): 'X' or 'O' for which player is checking for valid move
        
        RETURNS: 
            [int]: returns a list of ints with values 1-8 depending on which directions pieces would get flipped if player placed a piece at i, j
                    1: Right
                    2: Left
                    3: Up
                    4: Down
                    5: Up Right
                    6: Up Left
                    7: Down Right
                    8: Down Left
        '''

        #if there is already a piece there, return None as its not a valid move
        if(self.grid_values[i][j]):
            return None

        #list for holding directions in which proper move was found
        #used for turning the pieces later
        #1: right, 2: left, 3: up, 4: down, 5: up right, 6: up Left, 7: down right, 8: down left
        found_directions = []

        #get the string representation of the other player
        opposite_player = ''
        if(player == 'X'):
            opposite_player = 'O'
        else:
            opposite_player = 'X'

        #check all 8 directions for if a move is valid and which directions would get flipped pieces

        #check R
        x = j + 1
        opposite_found = False

        #loop until index reaches an edge or a piece is not the opposing_player's piece
        while(x < self.dimensions[0] and self.get_piece(i, x) == opposite_player):
            x += 1
            opposite_found = True

        #if index is still in range, the piece stopped on is the current players piece, and at least one opponent piece was found in the direction
        #append that direction to the return list
        if(x < self.dimensions[0] and self.get_piece(i, x) == player and opposite_found):
            found_directions.append(1)

        #check L
        x = j - 1
        opposite_found = False

        while(x >= 0 and self.get_piece(i, x) == opposite_player):
            x -= 1
            opposite_found = True

        if(x >= 0 and self.get_piece(i, x) == player and opposite_found):
            found_directions.append(2)


        #check U
        x = i - 1
        opposite_found = False

        while(x >= 0 and self.get_piece(x, j) == opposite_player):
            x -= 1
            opposite_found = True

        if(x >= 0 and self.get_piece(x, j) == player and opposite_found):
            found_directions.append(3)


        #check D
        x = i + 1
        opposite_found = False

        while(x < self.dimensions[0] and self.get_piece(x, j) == opposite_player):
            x += 1
            opposite_found = True

        if(x < self.dimensions[0] and self.get_piece(x, j) == player and opposite_found):
            found_directions.append(4)


        #check UR

        x = j + 1
        y = i - 1
        opposite_found = False

        while(x < self.dimensions[0] and y >= 0 and self.get_piece(y, x) == opposite_player):
            x += 1
            y -= 1
            opposite_found = True

        if(x < self.dimensions[0] and y >= 0 and self.get_piece(y, x) == player and opposite_found):
            found_directions.append(5)

        #check UL
        x = j - 1
        y = i - 1
        opposite_found = False

        while(x >= 0 and y >= 0 and self.get_piece(y, x) == opposite_player):
            x -= 1
            y -= 1
            opposite_found = True

        if(x >= 0 and y >= 0 and self.get_piece(y, x) == player and opposite_found):
            found_directions.append(6)

        #check DR
        x = j + 1
        y = i + 1
        opposite_found = False

        while(x < self.dimensions[0] and y < self.dimensions[0] and self.get_piece(y, x) == opposite_player):
            x += 1
            y += 1
            opposite_found = True

        if(x < self.dimensions[0] and y < self.dimensions[0] and self.get_piece(y, x) == player and opposite_found):
            found_directions.append(7)

        #check DL
        x = j - 1
        y = i + 1
        opposite_found = False

        while(x >= 0 and y < self.dimensions[0] and self.get_piece(y, x) == opposite_player):
            x -= 1
            y += 1
            opposite_found = True

        if(x >= 0  and y < self.dimensions[0] and self.get_piece(y, x) == player and opposite_found):
            found_directions.append(8)
        return found_directions

    def flip_piece(self, i, j):
        '''
        Flips a piece to the opposite player

        ARGS: {Note: function expects a position at which a piece is located, will error otherwise as only valid positions should get passed}
            i, j (int, int): position at which to flip piece
        '''
        if(self.get_piece(i, j) == 'X'):
            self.grid_values[i][j].set_value('O')
        else:
            self.grid_values[i][j].set_value('X')

    def turn_pieces(self, i, j, player):
        '''
        Function to flip needed pieces after a piece is played
        
        ARGS: 
            i, j (int, int): position at which piece was played
            player (str): 'X' or 'O' for which player placed the piece
        '''

        #first get the directions pieces need to get flipped in
        dirs = self.piece_dirs[i][j]

        #get the opposite player string representation
        opposite_player = ''
        if(player == 'X'):
            opposite_player = 'O'
        else:
            opposite_player = 'X'

        #if a direction needs to get flipped, keep flipping until a non opposing player piece is found

        #flip right
        if(1 in dirs):
            x = j + 1
            while(self.get_piece(i, x) == opposite_player):
                self.flip_piece(i, x)
                x += 1

        #flip left
        if(2 in dirs):
            x = j - 1
            while(self.get_piece(i, x) == opposite_player):
                self.flip_piece(i, x)
                x -= 1

        #flip up
        if(3 in dirs):
            x = i - 1
            while(self.get_piece(x, j) == opposite_player):
                self.flip_piece(x, j)
                x -= 1

        #flip down
        if(4 in dirs):
            x = i + 1
            while(self.get_piece(x, j) == opposite_player):
                self.flip_piece(x, j)
                x += 1

        #flip up_right
        if(5 in dirs):
            y = i - 1
            x = j + 1
            while(self.get_piece(y, x) == opposite_player):
                self.flip_piece(y, x)
                y -= 1
                x += 1

        #flip up_left
        if(6 in dirs):
            y = i - 1
            x = j - 1
            while(self.get_piece(y, x) == opposite_player):
                self.flip_piece(y, x)
                y -= 1
                x -= 1

        #flip down_right
        if(7 in dirs):
            y = i + 1
            x = j + 1
            while(self.get_piece(y, x) == opposite_player):
                self.flip_piece(y, x)
                y += 1
                x += 1

        #flip down_leftf
        if(8 in dirs):
            y = i + 1
            x = j - 1
            while(self.get_piece(y, x) == opposite_player):
                self.flip_piece(y, x)
                y += 1
                x -= 1

    def count_pieces(self):
        '''
        counts the number of pieces for each player and stores in member O_num and X_num
        '''
        O_num = 0
        X_num = 0

        #loop through all cells and count the number of each player's piece
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[0]):
                if(self.get_piece(i, j) == 'O'):
                    O_num += 1
                elif(self.get_piece(i, j) == 'X'):
                    X_num += 1

        self.O_num = O_num
        self.X_num = X_num

    def get_piece_count(self):
        '''
        returns the a tuple containing the number of pieces for each player
        
        RETURN:
            ((int, int)): tuple containing number of O pieces followed by number of X pieces
        '''
        return (self.O_num, self.X_num)



if __name__ == "__main__":
    pass