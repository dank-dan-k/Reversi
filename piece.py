
class Grid_Point:
    '''
    Class to hold points in a human readable form (1 indexed rather than 0)

    Attributes:
        pos (int, int): tuple containing 1 indexed position
    '''

    def __init__(self, i, j):
        '''
        Constructor

        ARGS: 
            i, j (int, int): takes two ints which it incriments by one and stores in the position attribute
        '''
        self.pos = (i+1, j+1)

    def __str__(self):
        '''
        string method
        RETURNS:
            str: string representation of the point
        '''
        return f'({self.pos[0]}, {self.pos[1]})'

    def __repr__(self):
        '''
        representation method

        RETURNS:
            str: string representation of the point (for printing lists of Grid_points)
        '''
        return self.__str__()

    def __eq__(self, other):
        '''
        equality method

        ARGS:
            other (Grid_Point or (int, int)): Takes another grid point or a 2d tuple of ints
        RETURNS:
            bool: true or false whether this object and the other are equivelant
        '''
        if(isinstance(other, Grid_Point)):
            return self.pos == other.pos
        elif(isinstance(other, tuple)):
            return self.pos == (other[0], other[1])
    
    def __getitem__(self, key):
        '''
        Get item method
        ARGS:
            key (int): key to get value of out of internal position attribute
        RETURNS:
            self.pos[key]: returns the element at the key in the point
        '''
        return self.pos[key]

class Piece:
    '''
    Piece class which represents a signle piece on the board

    Attributes:
        pos (int, int): tuple of two ints holding the grid position of the piece
        val: 'X' or 'O' for which player the piece belongs to

    Methods:
        get_value(): returns the val attribute of the piece (owning player)
        set_value(): sets the val attribute of the piece (owning player)
    '''
    def __init__(self, i, j, val):
        '''
        Constructor for piece

        ARGS:
            i, j (int, int): position of the piece
            val (str): player which owns the piece, 'X' or 'O'
        '''
        self.pos = (i, j)
        self.val = val


    def __str__(self):
        '''
        String method for the piece

        RETURNS:
            str: the player which owns the piece for printing
        '''
        return self.val

    def get_value(self):
        '''
        Gets player which owns the piece

        RETURNS:
            str: player which owns the piece 'X' or 'O'
        '''
        return self.val

    def set_value(self, val):
        '''
        Sets the player which owns a piece

        ARGS: 
            val (str): player which owns the piece now 'X' or 'O'
        '''
        self.val = val


if __name__ == "__main__":
    pass

