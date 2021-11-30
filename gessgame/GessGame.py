# Author: Ian Rolph
# Date: 6/4/20
# Description: Simulates the game of Gess.


def pair_to_coords(pair):
    """ Given a string containing the ordered column and row, returns the corresponding coordinates on the board """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    column = alphabet.index(pair[0])
    row = int(pair[1:]) - 1
    return row, column

def coords_to_pair(x, y):
    """ Given a pair of integer coordinates, returns the ordered column and row on the board """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    column = alphabet[y]
    row = x + 1
    return str(column) + str(row)

def abs_check(a, b):
    """ Checks if the absolute values of a and b are equal """
    return (a == b or -a == b)

class GessGame:
    def __init__(self):
        """ Initializes the game state and board, and sets the first turn to black """
        self._gamestate = "UNFINISHED"
        # MEMO: coordinate pairs are (row, column)
        self._board = [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", "B", " ", "B", " ", "B", "B", "B", "B", "B", "B", "B", "B", " ", "B", " ", "B", " ", " "],
                       [" ", "B", "B", "B", " ", "B", " ", "B", "B", "B", "B", " ", "B", " ", "B", " ", "B", "B", "B", " "],
                       [" ", " ", "B", " ", "B", " ", "B", "B", "B", "B", "B", "B", "B", "B", " ", "B", " ", "B", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", "B", " ", " ", "B", " ", " ", "B", " ", " ", "B", " ", " ", "B", " ", " ", "B", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", "W", " ", " ", "W", " ", " ", "W", " ", " ", "W", " ", " ", "W", " ", " ", "W", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", "W", " ", "W", " ", "W", "W", "W", "W", "W", "W", "W", "W", " ", "W", " ", "W", " ", " "],
                       [" ", "W", "W", "W", " ", "W", " ", "W", "W", "W", "W", " ", "W", " ", "W", " ", "W", "W", "W", " "],
                       [" ", " ", "W", " ", "W", " ", "W", "W", "W", "W", "W", "W", "W", "W", " ", "W", " ", "W", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]
        self._current_turn = "BLACK"

    def print_board(self):
        """ Prints the board row by row, for testing purposes """
        print(" ", "a   ", "b   ", "c   ", "d   ", "e   ", "f   ", "g   ", "h   ", "i   ", "j   ", "k   ", "l   ", "m   ", "n   ", "o   ", "p   ", "q   ", "r   ", "s   ", "t")
        for i in range(0, len(self._board)):
            print(self._board[i], i+1) 

    def get_game_state(self):
        """ Returns the current game state """
        return self._gamestate

    def get_current_turn(self):
        """ Returns the player whose turn it is """
        return self._current_turn

    def get_board(self):
        """ Returns the game board """
        return self._board

    def resign_game(self):
        """ Concedes the game, giving the player whose turn it isn't the win """
        if self._gamestate == "UNFINISHED":
            if self._current_turn == "BLACK":
                self._gamestate = "WHITE_WON"
            elif self._current_turn == "WHITE":
                self._gamestate = "BLACK_WON"

    def ring_check(self, player, board):
        """ Checks the given player's ring count on the given board. """
        rings = []
        if player == "BLACK":
            color = "B"
        elif player == "WHITE":
            color = "W"
        for i, v in enumerate(board):
            for j, k in enumerate(v):
                if 1 <= i <= 18 and 1 <= j <= 18:
                    if board[i][j] == " ":
                        if board[i + 1][j + 1] == color and board[i - 1][j - 1] == color and board[i + 1][j] == color and board[i - 1][j] == color and board[i][j + 1] == color and board[i][j - 1] == color and board[i - 1][j + 1] == color and board[i + 1][j - 1] == color:
                            rings.append((i, j))
        return rings


    def make_move(self, from_pos, to_pos):
        """ Moves the piece to the given position provided the move is legal """
        if self._gamestate != "UNFINISHED":
            return False
        for i in self._board[0]:
            i = " "
        for i in self._board[19]:
            i = " "
        for i in self._board:
            i[0] = " "
            i[19] = " "
        curr_player = self._current_turn
        from_coord = pair_to_coords(from_pos)
        to_coord = pair_to_coords(to_pos)
        from_x = from_coord[1]
        from_y = from_coord[0]
        to_x = to_coord[1]
        to_y = to_coord[0]
        diff_x = from_x - to_x
        diff_y = from_y - to_y
        intended_dir = None
        black_rings = self.ring_check("BLACK", self._board)
        white_rings = self.ring_check("WHITE", self._board)
        #print(white_rings)
        #print(black_rings)
        if len(white_rings) == 0:   # this should never happen but i'm keeping it as insurance
            self._gamestate = "BLACK_WON"
        elif len(black_rings) == 0: # neither should this
            self._gamestate = "WHITE_WON"

        if diff_x == 0 and diff_y == 0: # not moving
            #print("NOT MOVING")
            return False
        #print("FROM:", from_pos, from_coord) # debug
        #print("TO:", to_pos, to_coord) # debug
        #print("DIFFERENCE:", (diff_y, diff_x))
        if not(0 < from_x < 19 and 0 < from_y < 19 and 0 < to_x < 19 and 0 < to_y < 19):    # either from or to position is out of bounds
            #print("OUT OF BOUNDS ERROR") # debug
            return False
        if (not abs_check(diff_x, diff_y) and (diff_x != 0 and diff_y != 0)):   # proposed move is not vertical, horizontal, or diagonal
            #print("MOVE IS NOT VERTICAL, HORIZONTAL, OR DIAGONAL")
            return False
        p = Piece(self._board, from_pos)
        color_check = p.check_color()
        if color_check == False or color_check != self._current_turn:   # selected Piece is not one color or is not the current player's color, or has no stones in it
            #print("COLOR ERROR OR NO STONES IN SELECTED PIECE")
            return False
        valid_dir = p.valid_directions()
        #print("valid:", valid_dir)
        if diff_x > 0 and diff_y < 0:
            intended_dir = "SW"
        elif diff_x < 0 and diff_y < 0:
            intended_dir = "SE"
        elif diff_x < 0 and diff_y > 0:
            intended_dir = "NE"
        elif diff_x > 0 and diff_y > 0:
            intended_dir = "NW"
        elif diff_x == 0 and diff_y < 0:
            intended_dir = "S"
        elif diff_x == 0 and diff_y > 0:
            intended_dir = "N"
        elif diff_x < 0 and diff_y == 0:
            intended_dir = "E"
        elif diff_x > 0 and diff_y == 0:
            intended_dir = "W"
        else:
            #print("OOPS")
            return False
        #print("INTENDED DIRECTION", intended_dir)
        if not intended_dir in valid_dir:
            #print("NO STONE IN INTENDED DIRECTION")
            return False
        if intended_dir == "N" or intended_dir == "S" or intended_dir == "SW" or intended_dir == "NW" or intended_dir == "NE" or intended_dir == "SE":
            if p.get_stone_vals()[4] == " ":
                #print("CENTER IS NOT A STONE")
                if abs(diff_y) > 3:
                    #print("CENTER NOT STONE AND TRIED TO MOVE MORE THAN 3")
                    return False
                else:
                    result = p.rec_move(intended_dir, abs(diff_y))
                    if result[4] == to_coord:
                        values = p.get_stone_vals()
                        stones = p.get_stones()
                        temp_board = []
                        for i in self._board:
                            temp_board.append(list(i))
                        for i in stones:
                            temp_board[i[0]][i[1]] = " "
                        for i, v in enumerate(result):
                            temp_board[v[0]][v[1]] = values[i]
                        if len(self.ring_check(curr_player, temp_board)) == 0:   # proposed move would leave the current player w/o a ring
                            #print("CURRENT PLAYER BROKE LAST RING")
                            return False
                        else:
                            for i in stones:
                                self._board[i[0]][i[1]] = " "
                            for i, v in enumerate(result):
                                self._board[v[0]][v[1]] = values[i]
                    #self.print_board()  #debug
                    if curr_player == "BLACK":
                        if len(self.ring_check("WHITE", self._board)) == 0:
                            #print("BLACK WON")
                            self._gamestate = "BLACK_WON"
                        self._current_turn = "WHITE"
                        return True
                    elif curr_player == "WHITE":
                        if len(self.ring_check("BLACK", self._board)) == 0:
                            #print("WHITE WON")
                            self._gamestate = "WHITE_WON"
                        self._current_turn = "BLACK"
                        return True
            else:
                #print("CENTER IS A STONE")
                result = p.rec_move(intended_dir, abs(diff_y))
                #print("RESULT:",result[4])
                #print("EXPECTED:", to_coord)
                if result[4] == to_coord:
                    values = p.get_stone_vals()
                    stones = p.get_stones()
                    temp_board = []
                    for i in self._board:
                        temp_board.append(list(i))
                    for i in stones:
                        temp_board[i[0]][i[1]] = " "
                    for i, v in enumerate(result):
                        temp_board[v[0]][v[1]] = values[i]
                    if len(self.ring_check(curr_player, temp_board)) == 0:   # proposed move would leave the current player w/o a ring
                        #print("CURRENT PLAYER BROKE LAST RING")
                        return False
                    else:
                        for i in stones:
                            self._board[i[0]][i[1]] = " "
                        for i, v in enumerate(result):
                            self._board[v[0]][v[1]] = values[i]
                #self.print_board()  #debug
                if curr_player == "BLACK":
                    if len(self.ring_check("WHITE", self._board)) == 0:
                        #print("BLACK WON")
                        self._gamestate = "BLACK_WON"
                    self._current_turn = "WHITE"
                    return True
                elif curr_player == "WHITE":
                    if len(self.ring_check("BLACK", self._board)) == 0:
                        #print("WHITE WON")
                        self._gamestate = "WHITE_WON"
                    self._current_turn = "BLACK"
                    return True
        elif intended_dir == "E" or intended_dir == "W":
            if p.get_stone_vals()[4] == " ":
                #print("CENTER IS NOT A STONE")
                if abs(diff_x) > 3:
                    #print("CENTER NOT STONE AND TRIED TO MOVE MORE THAN 3")
                    return False
                else:
                    result = p.rec_move(intended_dir, abs(diff_x))
                    if result[4] == to_coord:
                        values = p.get_stone_vals()
                        stones = p.get_stones()
                        temp_board = []
                        for i in self._board:
                            temp_board.append(list(i))
                        for i in stones:
                            temp_board[i[0]][i[1]] = " "
                        for i, v in enumerate(result):
                            temp_board[v[0]][v[1]] = values[i]
                        if len(self.ring_check(curr_player, temp_board)) == 0:   # proposed move would leave the current player w/o a ring
                            #print("CURRENT PLAYER BROKE LAST RING")
                            return False
                        else:
                            for i in stones:
                                self._board[i[0]][i[1]] = " "
                            for i, v in enumerate(result):
                                self._board[v[0]][v[1]] = values[i]
                    #self.print_board()  #debug
                    if curr_player == "BLACK":
                        if len(self.ring_check("WHITE", self._board)) == 0:
                            #print("BLACK WON")
                            self._gamestate = "BLACK_WON"
                        self._current_turn = "WHITE"
                        return True
                    elif curr_player == "WHITE":
                        if len(self.ring_check("BLACK", self._board)) == 0:
                            #print("WHITE WON")
                            self._gamestate = "WHITE_WON"
                        self._current_turn = "BLACK"
                        return True
            else:
                #print("CENTER IS A STONE")
                result = p.rec_move(intended_dir, abs(diff_x))
                if result[4] == to_coord:
                    values = p.get_stone_vals()
                    stones = p.get_stones()
                    temp_board = []
                    for i in self._board:
                        temp_board.append(list(i))
                    for i in stones:
                        temp_board[i[0]][i[1]] = " "
                    for i, v in enumerate(result):
                        temp_board[v[0]][v[1]] = values[i]
                    if len(self.ring_check(curr_player, temp_board)) == 0:   # proposed move would leave the current player w/o a ring
                        #print("CURRENT PLAYER BROKE LAST RING")
                        return False
                    else:
                        for i in stones:
                            self._board[i[0]][i[1]] = " "
                        for i, v in enumerate(result):
                            self._board[v[0]][v[1]] = values[i]
                #self.print_board()  #debug
                if curr_player == "BLACK":
                    if len(self.ring_check("WHITE", self._board)) == 0:
                        #print("BLACK WON")
                        self._gamestate = "BLACK_WON"
                    self._current_turn = "WHITE"
                    return True
                elif curr_player == "WHITE":
                    if len(self.ring_check("BLACK", self._board)) == 0:
                        #print("WHITE WON")
                        self._gamestate = "WHITE_WON"
                    self._current_turn = "BLACK"
                    return True

        


        
        



class Piece:
    def __init__(self, board, center):
        """ Initializes the piece's center and list of stones """
        self._center = pair_to_coords(center)
        self._stones = []
        self._board = board
        self._stone_vals = []
        x = self._center[1]
        y = self._center[0]
        #print("CENTER OF NEW PIECE:", self._center) # debug
        for i in range(-1, 2):
            for j in range(-1, 2):
                self._stones.append((y + j, x + i))
        #print("STONES IN NEW PIECE:", self._stones) # debug
        self._stone_vals = [self._board[i[0]][i[1]] for i in self._stones]
        #print("STONE VALUES:", self._stone_vals)
    
    def get_stones(self):
        """ Returns a list of the Piece's stones """
        return self._stones
    
    def get_stone_vals(self):
        """ Returns a list of the values that the Piece's stones hold """
        return self._stone_vals

    def check_color(self):
        """ Returns the color of the Piece, or False if the piece has multiple colors """
        color = None
        for i in self._stones:
            if color == None:
                if self._board[i[0]][i[1]] == "B":
                    color = "B"
                elif self._board[i[0]][i[1]] == "W":
                    color = "W"
            if self._board[i[0]][i[1]] != " " and self._board[i[0]][i[1]] != color:
                #print("DETECTED OTHER COLOR")
                return False
        if color == "B":
            #print("COLOR CHECK BLACK")
            return "BLACK"
        elif color == "W":
            #print("COLOR CHECK WHITE")
            return "WHITE"
        else:
            #print("COLOR CHECK FALSE")
            return False
    
    def valid_directions(self):
        """ Returns the valid directions that the Piece can move """
        d = []
        if self._stone_vals[0] != " ":
            d.append("NW")
        if self._stone_vals[3] != " ":
            d.append("N")
        if self._stone_vals[6] != " ":
            d.append("NE")
        if self._stone_vals[1] != " ":
            d.append("W")
        if self._stone_vals[7] != " ":
            d.append("E")
        if self._stone_vals[2] != " ":
            d.append("SW")
        if self._stone_vals[5] != " ":
            d.append("S")
        if self._stone_vals[8] != " ":
            d.append("SE")
        return d

    def rec_move(self, dir, count, end_stones=None, ended=False):
        """ Recursively checks the path of a piece, checking if its next position has a stone in it """
        if end_stones == None:
            end_stones = self._stones

        center_x = end_stones[4][1]
        center_y = end_stones[4][0]
        if count == 0:
            return end_stones

        if dir == "N":
            if ended:
                temp = []
                for i in end_stones:
                    temp.append((i[0] - 1, i[1]))
                return temp
            else:
                if (0 <= center_y - 2 <= 19):
                    if (self._board[center_y - 2][center_x - 1] == " " and self._board[center_y - 2][center_x] == " " and self._board[center_y - 2][center_x + 1] == " "):
                        temp = []
                        for i in end_stones:
                            #print("BEFORE: ", i)
                            temp.append((i[0] + -1, i[1] + 0))
                            #print("AFTER: ", i)
                            #print()
                        return self.rec_move(dir, count - 1, temp, False)
                    else:
                        #print("STONE DETECTED")
                        #print("END STONES:", end_stones)
                        temp = []
                        for i in end_stones:
                            temp.append((i[0], i[1]))
                        return self.rec_move(dir, count, temp, True)
                else:
                    return False
        if dir == "NE":
            if ended:
                temp = []
                for i in end_stones:
                    temp.append((i[0] - 1, i[1] + 1))
                return temp
            else:
                if (0 <= center_y - 2 <= 19):
                    if (self._board[center_y - 1][center_x + 2] == " " and self._board[center_y - 2][center_x + 2] == " " and self._board[center_y - 2][center_x + 1] == " "):
                        temp = []
                        for i in end_stones:
                            #print("BEFORE: ", i)
                            temp.append((i[0] - 1, i[1] + 1))
                            #print("AFTER: ", i)
                            #print()
                        return self.rec_move(dir, count - 1, temp, False)
                    else:
                        #print("STONE DETECTED")
                        #print("END STONES:", end_stones)
                        temp = []
                        for i in end_stones:
                            temp.append((i[0], i[1]))
                        return self.rec_move(dir, count, temp, True)
                else:
                    return False
        if dir == "E":
            if ended:
                temp = []
                for i in end_stones:
                    temp.append((i[0], i[1] + 1))
                return temp
            else:
                if (0 <= center_x + 2 <= 19):
                    if (self._board[center_y + 1][center_x + 2] == " " and self._board[center_y][center_x + 2] == " " and self._board[center_y - 1][center_x + 2] == " "):
                        temp = []
                        for i in end_stones:
                            #print("BEFORE: ", i)
                            temp.append((i[0], i[1] + 1))
                            #print("AFTER: ", i)
                            #print()
                        return self.rec_move(dir, count - 1, temp, False)
                    else:
                        #print("STONE DETECTED")
                        #print("END STONES:", end_stones)
                        temp = []
                        for i in end_stones:
                            temp.append((i[0], i[1]))
                        return self.rec_move(dir, count, temp, True)
                else:
                    return False
        if dir == "SE":
            if ended:
                temp = []
                for i in end_stones:
                    temp.append((i[0] + 1, i[1] + 1))
                return temp
            else:
                if (0 <= center_y + 2 <= 19):
                    if (self._board[center_y + 2][center_x + 1] == " " and self._board[center_y + 2][center_x + 2] == " " and self._board[center_y + 1][center_x + 2] == " "):
                        temp = []
                        for i in end_stones:
                            #print("BEFORE: ", i)
                            temp.append((i[0] + 1, i[1] + 1))
                            #print("AFTER: ", i)
                            #print()
                        return self.rec_move(dir, count - 1, temp, False)
                    else:
                        #print("STONE DETECTED")
                        #print("END STONES:", end_stones)
                        temp = []
                        for i in end_stones:
                            temp.append((i[0], i[1]))
                        return self.rec_move(dir, count, temp, True)
                else:
                    return False
        if dir == "S":
            if ended:
                temp = []
                for i in end_stones:
                    temp.append((i[0] + 1, i[1]))
                return temp
            else:
                if (0 <= center_y + 2 <= 19):
                    if (self._board[center_y + 2][center_x - 1] == " " and self._board[center_y + 2][center_x] == " " and self._board[center_y + 2][center_x + 1] == " "):
                        temp = []
                        for i in end_stones:
                            #print("BEFORE: ", i)
                            temp.append((i[0] + 1, i[1] + 0))
                            #print("AFTER: ", i)
                            #print()
                        return self.rec_move(dir, count - 1, temp, False)
                    else:
                        #print("STONE DETECTED")
                        #print("END STONES:", end_stones)
                        temp = []
                        for i in end_stones:
                            temp.append((i[0], i[1]))
                        return self.rec_move(dir, count, temp, True)
                else:
                    return False
        if dir == "SW":
            if ended:
                temp = []
                for i in end_stones:
                    temp.append((i[0] + 1, i[1] - 1))
                return temp
            else:
                if (0 <= center_y + 2 <= 19):
                    if (self._board[center_y + 1][center_x - 2] == " " and self._board[center_y + 2][center_x - 2] == " " and self._board[center_y + 2][center_x - 1] == " "):
                        temp = []
                        for i in end_stones:
                            #print("BEFORE: ", i)
                            temp.append((i[0] + 1, i[1] - 1))
                            #print("AFTER: ", i)
                            #print()
                        return self.rec_move(dir, count - 1, temp, False)
                    else:
                        #print("STONE DETECTED")
                        #print("END STONES:", end_stones)
                        temp = []
                        for i in end_stones:
                            temp.append((i[0], i[1]))
                        return self.rec_move(dir, count, temp, True)
                else:
                    return False
        if dir == "W":
            if ended:
                temp = []
                for i in end_stones:
                    temp.append((i[0], i[1] - 1))
                return temp
            else:
                if (0 <= center_x - 2 <= 19):
                    if (self._board[center_y + 1][center_x - 2] == " " and self._board[center_y][center_x - 2] == " " and self._board[center_y - 1][center_x - 2] == " "):
                        temp = []
                        for i in end_stones:
                            #print("BEFORE: ", i)
                            temp.append((i[0], i[1] - 1))
                            #print("AFTER: ", i)
                            #print()
                        return self.rec_move(dir, count - 1, temp, False)
                    else:
                        #print("STONE DETECTED")
                        #print("END STONES:", end_stones)
                        temp = []
                        for i in end_stones:
                            temp.append((i[0], i[1]))
                        return self.rec_move(dir, count, temp, True)
                else:
                    return False
        if dir == "NW":
            if ended:
                temp = []
                for i in end_stones:
                    temp.append((i[0] - 1, i[1] - 1))
                return temp
            else:
                if (0 <= center_y - 2 <= 19):
                    if (self._board[center_y -2][center_x - 1] == " " and self._board[center_y - 2][center_x - 2] == " " and self._board[center_y - 1][center_x - 2] == " "):
                        temp = []
                        for i in end_stones:
                            #print("BEFORE: ", i)
                            temp.append((i[0] - 1, i[1] - 1))
                            #print("AFTER: ", i)
                            #print()
                        return self.rec_move(dir, count - 1, temp, False)
                    else:
                        #print("STONE DETECTED")
                        #print("END STONES:", end_stones)
                        temp = []
                        for i in end_stones:
                            temp.append((i[0], i[1]))
                        return self.rec_move(dir, count, temp, True)
                else:
                    return False
