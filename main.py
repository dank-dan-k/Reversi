from board import Board
from piece import Grid_Point

#variable controlling board size
size = 8
current_player = 'O'
def main():
    #create board and current player string
    selection = 0
    global size
    global current_player

    #loop until player starts game
    while(selection != '1'):
        #print welcome message and menu options
        print("Welcome to Reversi")
        print("Please select a menu option")
        print("\t1: Play Game")
        print("\t2: Show Rules")
        print("\t3: Change Settings \n")

        selection = input("Please select: ")

        if(selection == '1'):
            print("Game Starting... \n")
        elif(selection == '2'):
            #print rules
            print("RULES: ")
            print("\tPlayers O and X take turns placing their respective pieces on the board.")
            print("\tPieces must be placed on open cell that sandwhiches at least one opponent piece either vertically, horizontally, or diagonally.")
            print("\tAll opposing pieces that are sandwhiched flip are flipped over and become friendly pieces.")
            print("\tIf a player has no legal moves, their turn is skipped.")
            print("\tThe game continues until a player has no pieces left, there are no empty tiles left, or neither player has a legal move.")
            print("\tThe player with more pieces on the board at the end wins. \n")
            
        elif(selection == '3'):
            #get player choice on starting player and grid size
            print("SETTINGS:")
            inp = input("Please enter the grid size (default 8): ")

            #catch illegal inputs and set it to default if it is
            try:
                size = int(inp)
                if(size <= 4):
                    raise ValueError
            except ValueError:
                print("Invalid size entered, set to default of 8")
                size = 8

            inp = input("Please enter which player starts first O or X (default O): ").upper()

            #catch illegal inputs and set it to default if it is
            if(inp != 'X' or inp != 'O'):
                print("Invalid starting player, set to default of O")
                current_player = 'O'
            else:
                current_player = inp

        else:
            print("Unknown selection, please choose again \n")
            pass

        input("Input any key to continue: ")

    #create the board
    global brd
    brd = Board(size)

    #enter the main game loop
    gameLoop()

def gameLoop():
    global current_player 
    global brd
    
    
    #variable for checking if both players have skipped their turns in order to terminate if neither player has moves
    turn_skipped = False

    while(1):
        #print the board
        print(brd)

        

        #get the current piece count
        o_num, x_num = brd.get_piece_count()

        #get all possible moves for the current player
        possible_moves = brd.get_available_moves(current_player)

        #if a player has no possible moves and the previous player did not skip their turn, skip the current_players turn
        if(not possible_moves and not turn_skipped):
            turn_skipped = True
            print("\nTurn Skipped!\n")
            if current_player == 'X':
                current_player = 'O'
            else:
                current_player = 'X'

            continue

        #if the previous player has skipped their turn or either play has 0 pieces, the game is over so check who wins
        elif((not possible_moves and turn_skipped) or o_num == 0 or x_num == 0):
            print(f'Current Score: {o_num} O\'s, {x_num} X\'s \n')
            if(o_num < x_num):
                print('Player X wins!')
                quit()
            elif(o_num > x_num):
                print('Player O wins')
                quit()
            else:
                print('Its a tie!')
                quit()

        #resset turn skipped to false if a player has a legal move
        turn_skipped = False

        #print out the player, current score, and possible moves
        print(f'Current Score: {o_num} O\'s, {x_num} X\'s \n')


        print(f'Player {current_player}\'s turn: ')
        print(f'Possible Moves: {possible_moves}\n')


        desired_position = ()
        allowed = False

        #get a legal input for a position
        while(not allowed):
            inp = input("Please enter which position you'd like (row, col) or 'exit' to terminate program:")

            #terminate program on exit
            if(inp == 'exit'):
                print('program terminating...')
                quit()

            #otherwise split the input
            vals = [x.strip() for x in inp.split(',')]

            #a proper input is a list with length 2, where each element is a numeric string
            if (not (isinstance(vals, list) and len(vals) == 2 and vals[0].isdigit() and vals[1].isdigit())):
                print('Please enter a valid input!')
                continue
            
            #if the input is legal, convert it to a grid_point
            #grid point auto incriments its input for Human printing so need to subtract one from the human input which is already in that form
            desired_position = Grid_Point(int(vals[0]) - 1, int(vals[1]) - 1)

            #if the desired position is in the possible moves, its legal, otherwise they must select a new point
            allowed = desired_position in possible_moves
            if(not allowed):
                print("Please enter a legal move\n")

        #add the current player's piece to their desired position. Also handles flipping pieces
        brd.add_piece(desired_position, current_player)

        #switch the current player
        if current_player == 'X':
            current_player = 'O'
        else:
            current_player = 'X'





if __name__ == "__main__":
    main()