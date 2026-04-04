from random import *


class Board:
    def __init__(self):
        self.cellFree = [1,2,3,4,5,6,7,8,9]
        self.state = [0,0,0,0,0,0,0,0,0]
    
    def sign_to_printable(self,sign):
        if sign == 0:
            return "-"
        elif sign == 1:
            return "X"
        else:
            return "O"
    
    def print_board(self):
        print(' ' + self.sign_to_printable(self.state[0]) + ' | ' + self.sign_to_printable(self.state[1]) + ' | ' + self.sign_to_printable(self.state[2]) + '\n' +
              ' ' + self.sign_to_printable(self.state[3]) + ' | ' + self.sign_to_printable(self.state[4]) + ' | ' + self.sign_to_printable(self.state[5]) + '\n' +
              ' ' + self.sign_to_printable(self.state[6]) + ' | ' + self.sign_to_printable(self.state[7]) + ' | ' + self.sign_to_printable(self.state[8]) + ' ')
    
    def is_valid_turn(self, cell):
        if self.state[cell] == 0:
            return True
        else:
            return False

    def make_turn(self, cell, player):
        if self.is_valid_turn(cell):
            self.state[cell] = player.symbol
            return True
        return False
        
    def check_win(self,player):
        s = player.symbol
        if self.state[0] == s and self.state[1] == s and self.state[2] == s:
            return True
        elif self.state[3] == s and self.state[4] == s and self.state[5] == s:
            return True
        elif self.state[6] == s and self.state[7] == s and self.state[8] == s:
            return True
        elif self.state[0] == s and self.state[3] == s and self.state[6] == s:
            return True
        elif self.state[1] == s and self.state[4] == s and self.state[7] == s:
            return True 
        elif self.state[2] == s and self.state[5] == s and self.state[8] == s:
            return True 
        elif self.state[0] == s and self.state[4] == s and self.state[8] == s:
            return True
        elif self.state[2] == s and self.state[4] == s and self.state[6] == s:
            return True            
    
    def is_full(self):
        for i in self.state:
            if i == 0:
                return False
        return True
    
    def ai_check_win(self):
        while True:
            if self.state[0] == 1 and self.state[1] == 1:
                if self.state[2] == 0:
                    cellT = 3
                    break
            if self.state[0] == 1 and self.state[2] == 1:
                if self.state[1] == 0:
                    cellT = 2
                    break
            if self.state[1] ==1 and self.state[2] == 1:
                if self.state[0] == 0:
                    cellT = 1
                    break
            if self.state[3] == 1 and self.state[4] == 1:
                if self.state[5] == 0:
                    cellT = 6
                    break
            if self.state[3] == 1 and self.state[5] == 1:
                if self.state[4] == 0:
                    cellT = 5
                    break
            if self.state[4] == 1 and self.state[5] == 1:
                if self.state[3] == 0:
                    cellT = 4
                    break
            if self.state[6] == 1 and self.state[7] == 1:
                if self.state[8] == 0:
                    cellT = 9
                    break
            if self.state[6] == 1 and self.state[8] == 1:
                if self.state[7] == 0:
                    cellT = 8
                    break
            if self.state[7] == 1 and self.state[8] == 1:
                if self.state[6] == 0:
                    cellT = 7
                    break
            if self.state[0] == 1 and self.state[3] == 1:
                if self.state[6] == 0:
                    cellT = 7
                    break
            if self.state[0] == 1 and self.state[6] == 1:
                if self.state[3] == 0:
                    cellT = 4
                    break
            if self.state[3] == 1 and self.state[6] == 1:
                if self.state[0] == 0:
                    cellT = 1
                    break
            if self.state[1] == 1 and self.state[4] == 1:
                if self.state[7] == 0:
                    cellT = 8
                    break
            if self.state[1] == 1 and self.state[7] == 1:
                if self.state[4] == 0:
                    cellT = 5
                    break
            if self.state[4] == 1 and self.state[7] == 1:
                if self.state[1] == 0:
                    cellT = 2
                    break
            if self.state[2] == 1 and self.state[5] == 1:
                if self.state[8] == 0:
                    cellT = 9
                    break
            if self.state[2] == 1 and self.state[8] == 1:
                if self.state[5] == 0:
                    cellT = 6
                    break
            if self.state[5] == 1 and self.state[8] == 1:
                if self.state[2] == 0:
                    cellT = 3
                    break
            if self.state[0] == 1 and self.state[4] == 1:
                if self.state[8] == 0:
                    cellT = 9
                    break
            if self.state[0] == 1 and self.state[8] == 1:
                if self.state[4] == 0:
                    cellT = 5
                    break
            if self.state[4] == 1 and self.state[8] == 1:
                if self.state[0] == 0:
                    cellT = 1
                    break
            if self.state[2] == 1 and self.state[4] == 1:
                if self.state[6] == 0:
                    cellT = 7
                    break
            if self.state[2] == 1 and self.state[6] == 1:
                if self.state[4] == 0:
                    cellT = 5
                    break
            if self.state[4] ==1 and self.state[6] == 1:
                if self.state[2] == 0:
                    cellT = 3
                    break
	    
            if self.state[0] == 2 and self.state[1] == 2:
                if self.state[2] == 0:
                    cellT = 3
                    break
            if self.state[0] == 2 and self.state[2] == 2:
                if self.state[1] == 0:
                    cellT = 2
                    break
            if self.state[1] == 2 and self.state[2] == 2:
                if self.state[0] == 0:
                    cellT = 1
                    break
            if self.state[3] == 2 and self.state[4] == 2:
                if self.state[5] == 0:
                    cellT = 6
                    break
            if self.state[3] == 2 and self.state[5] == 2:
                if self.state[4] == 0:
                    cellT = 5
                    break
            if self.state[4] == 2 and self.state[5] == 2:
                if self.state[3] == 0:
                    cellT = 4
                    break
            if self.state[6] == 2 and self.state[7] == 2:
                if self.state[8] == 0:
                    cellT = 9
                    break
            if self.state[6] == 2 and self.state[8] == 2:
                if self.state[7] == 0:
                    cellT = 8
                    break
            if self.state[7] == 2 and self.state[8] == 2:
                if self.state[6] == 0:
                    cellT = 7
                    break
            if self.state[0] == 2 and self.state[3] == 2:
                if self.state[6] == 0:
                    cellT = 7
                    break
            if self.state[0] == 2 and self.state[6] == 2:
                if self.state[3] == 0:
                    cellT = 4
                    break
            if self.state[3] == 2 and self.state[6] == 2:
                if self.state[0] == 0:
                    cellT = 1
                    break
            if self.state[1] == 2 and self.state[4] == 2:
                if self.state[7] == 0:
                    cellT = 8
                    break
            if self.state[1] == 2 and self.state[7] == 2:
                if self.state[4] == 0:
                    cellT = 5
                    break
            if self.state[4] == 2 and self.state[7] == 2:
                if self.state[1] == 0:
                    cellT = 2
                    break
            if self.state[2] == 2 and self.state[5] == 2:
                if self.state[8] == 0:
                    cellT = 9
                    break
            if self.state[2] == 2 and self.state[8] == 2:
                if self.state[5] == 0:
                    cellT = 6
                    break
            if self.state[5] == 2 and self.state[8] == 2:
                if self.state[2] == 0:
                    cellT = 3
                    break
            if self.state[0] == 2 and self.state[4] == 2:
                if self.state[8] == 0:
                    cellT = 9
                    break
            if self.state[0] == 2 and self.state[8] == 2:
                if self.state[4] == 0:
                    cellT = 5
                    break
            if self.state[4] == 2 and self.state[8] == 2:
                if self.state[0] == 0:
                    cellT = 1
                    break
            if self.state[2] == 2 and self.state[4] == 2:
                if self.state[6] == 0:
                    cellT = 7
                    break
            if self.state[2] == 2 and self.state[6] == 2:
                if self.state[4] == 0:
                    cellT = 5
                    break
            if self.state[4] == 2 and self.state[6] == 2:
                if self.state[2] == 0:
                    cellT = 3
                    break
            cellT = self.cellFree[randint(0,len(self.cellFree)-1)]
            break
        return cellT
   
   
class Player:
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name


class Ki(Player):
	def __init__(self, symbol, name):
		self.symbol = symbol
		self.name = name



def one_player():
    player_b_name = str(input('Enter your name: '))
    player_a = Ki(1, 'Ai')
    player_b = Player(2, player_b_name)
    board = Board()
    active_player = player_a
    cell2=[1,2,3,4,5,6,7,8,9]
    print('\n')
    while not board.is_full():
        board.print_board()
        print('\n' + str(active_player.name) + 's turn') 
        if active_player == player_b:
            try:
            	cell = int(input("Where do you wnat to place your sign? [1-9]" ))
            except ValueError:
            	continue	    	
        else:
        	cell = board.ai_check_win()
        	
        print("cell = " + str(cell))
        cell = cell - 1
        if cell < 0 or cell > 8:
            print('Please enter a number between 1 and 9')
            continue
        if not board.make_turn(cell,active_player):
            print('invalid move')
            continue
        print('\n')
        cell = cell + 1
        board.cellFree.remove(cell)
        if board.check_win(active_player):
            board.print_board()
            print('You won! ' + str(active_player.name))
            break
        if active_player == player_a:
            active_player = player_b
        else:
            active_player = player_a
    board.print_board()
    print('Game finished')
          
def two_player():
    player_a = Player(1, 'P1')
    player_b = Player(2, 'P2')
    board = Board()
    active_player = player_a
    while not board.is_full():
        board.print_board()
        print('\n' + str(active_player.name) + 's turn')
        try:
            cell = int(input("Where do you wnat to place your sign? [1-9]" ))
        except ValueError:
            continue
        print('\n')
        cell = cell - 1
        if cell < 0 or cell > 8:
            print('Please enter a number between 1 and 9')
            continue
        if not board.make_turn(cell,active_player):
            print('invalid move')
            continue
        if board.check_win(active_player):
            board.print_board()
            print('You won! ' + str(active_player.name))
            break   
        if active_player == player_a:
            active_player = player_b
        else:
            active_player = player_a
            
            
if __name__ == '__main__':
    print ('Board:' + '\n' +
            '1 | 2 | 3' + '\n' +
            '4 | 5 | 6' + '\n' +
            '7 | 8 | 9' + '\n' + '\n')
            
    while True:
        try:
            game = int(input('How many players are playing ? (\'1\': One Player , \'2\': Two players , \'3\': Exit)'))
        except ValueError:
            continue
        if game == 1:
            one_player()
        if game == 2:
            two_player()
        if game == 3:
            break