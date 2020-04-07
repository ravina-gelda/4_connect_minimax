import numpy as np
DEPTH=2


class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.tree_explored = 0

    def inside_board(self,row_index,col_index,y_offset,x_offset):
        if row_index+y_offset < 0 or row_index+y_offset > 5:
            return False
        if col_index+x_offset < 0 or col_index+x_offset > 6:
            return False
        return True
        
    def terminal_state(self,board):
        '''
        Find if there are more than 4 adjecent ststes of the same player or not,
        return True if success in the game
        '''
        row_index = 5
        col_index = 0
        num_adjacent = 0
        offsets = [(-1,-1),(0,-1),(1,-1),(1,0)]
        for row_index in range(5,0,-1):
            for col_index in range(6):
                if board[row_index][col_index]==self.player_number:
                    for offset in offsets:
                        num_adjacent = 1
                        
                        x_offset = offset[0]
                        y_offset = offset[1]
                        while board[row_index+y_offset][col_index+x_offset]==self.player_number:
                            
                            num_adjacent = num_adjacent+1
                            x_offset = x_offset + offset[0]
                            y_offset = y_offset + offset[1]
                            if not self.inside_board(row_index,col_index,y_offset,x_offset):
                                break
                        if num_adjacent >= 4:
                            return True
        return False

    def actions(self,board):
        '''
        Find out empty cells for valid actions
        return list of empty cells(cells with 0)
        '''
        actions = []
        for col in range(len(board[0])-1,0,-1):
            row = 5
            while board[row][col]!=0 and row>0:
                row = row - 1
            if board[row][col]==0:
                actions.append((row,col))
        return actions

    def result(self,board,action,number):
        '''
        new_board resulting from hypothetically taking a move from all the valid moves
        '''
        new_board = np.zeros([6,7]).astype(np.uint8)
        for row_index in range(len(board)):
            if row_index != action[0]:
                new_board[row_index] = board[row_index]
            else:
                new_row = []
                for col_index in range(len(board[0])):
                    if col_index != action[1]:
                        new_row.append(board[row_index][col_index])
                    else:
                        new_row.append(number)
                new_board[row_index] = new_row
        return new_board

    def min_value(self,board,alpha,beta,depth):
        '''
        Implemented min_value method from alpha_beta serach algorithm
        '''
        self.tree_explored+=1
        print("tree_explored=", self.tree_explored)
        print("in min_value with board: \n"+str(board))
        if self.terminal_state(board) or depth>=DEPTH:
            ret = (self.evaluation_function(board,self.player_number)-self.evaluation_function(board,(self.player_number*2)%3),3)
            return ret 
        util_val = 1000000
        move = 0
        move_pair = (move,util_val)
        actions = self.actions(board)
        for action in actions: 
            action_util_val = self.max_value(self.result(board,action,(self.player_number*2)%3),alpha,beta,depth+1)[0]
            if action_util_val < util_val:
                move = action[1]
                
           
            util_val=min(util_val,action_util_val) 
            if util_val<alpha:
                return (util_val,move)
            beta = min(beta,util_val)
            move_pair = (util_val,move)
        
        return move_pair
    
    def max_value(self,board,alpha,beta,depth):
        '''
        implemented max_value method from alpha-beta serach algorithm
        '''
        self.tree_explored+=1
        print("tree_explored=",self.tree_explored)
        print("in max_value with board "+str(board))
        if self.terminal_state(board) or depth>=DEPTH:
            ret = (self.evaluation_function(board,self.player_number)-self.evaluation_function(board,(self.player_number*2)%3),4)
            
            return ret 
        util_val = -1000000
        move = 0
        move_pair = (move,util_val)
        actions = self.actions(board)
        for action in actions: 
            
            action_util_val = self.min_value(self.result(board,action,self.player_number),alpha,beta,depth+1)[0]
            if action_util_val > util_val:
                move = action[1]
            util_val = max(util_val,action_util_val) 
            if util_val > beta:
                return (util_val,move)
            alpha = max(alpha,util_val)
            move_pair = (util_val,move)
        return move_pair
        
    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm
        This will play against either itself or a human player
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them
        RETURNS:
        The 0 based index of the column that represents the next move
        """
       
        alpha = 0
        beta = 0
        depth = 1
        move = self.max_value(board,alpha,beta,depth)
        return move[1]

    def probability(self,board,action,actions):
        '''
        Equal probability of all the valid actions
        '''
        return int(1/len(actions))
    
    def exp_value(self,board,layer):
        '''

        '''
        util_val = 0
        actions = self.actions(board) 
        for action in actions:
            p = self.probability(board,action,actions)
            print(self.value(self.result(board,action,(self.player_number*2)%3),True,layer+1))
            util_val = util_val + p*self.value(self.result(board,action,(self.player_number*2)%3),True,layer+1)[0]
        return util_val
    
    def max_value_expectimax(self,board,layer):
        util_val = -1000000
        actions = self.actions(board)
        move = 2
        for action in actions:
            if self.value(self.result(board,action,self.player_number),False,layer+1) > util_val:
                move = action[1]
            util_val = max(util_val,self.value(self.result(board,action,self.player_number),False,layer+1))
        return (util_val,move)
    
    def value(self,board,isMax,layer):
        if self.terminal_state(board) or layer >= 5:
            if isMax:
                return (self.evaluation_function(board,self.player_number)-self.evaluation_function(board,(self.player_number*2)%3),2)
            else:
                return self.evaluation_function(board,self.player_number)-self.evaluation_function(board,(self.player_number*2)%3)
        if isMax:
            return self.max_value_expectimax(board,layer)
        else:
            return self.exp_value(board,layer)
    
    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.
        This will play against the random player, who chooses any valid move
        with equal probability
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them
        RETURNS:
        The 0 based index of the column that represents the next move
        """
        return self.value(board,True,0)[1]



    def evaluation_function(self, board,player_num):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled2
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them
        RETURNS:
        The utility value for the current board
        """
        row_index = 5
        col_index = 0
        num_adjacent = 0
        max_adjacent = 0
        score = 0
        offsets = [(-1,-1),(-1,0),(-1,1),(0,1)]
        for row_index in range(5,0,-1):
            for col_index in range(6): 
                if board[row_index][col_index]==player_num:
		                for offset in offsets:
                                    num_adjacent = 1
                                    x_offset = offset[0] 
                                    y_offset = offset[1]
                                    while self.inside_board(row_index,col_index,y_offset,x_offset) and (board[row_index+y_offset][col_index+x_offset]==player_num or board[row_index+y_offset][col_index+x_offset]==0):
                                        num_adjacent = num_adjacent+1
                                        x_offset = x_offset + offset[0]
                                        y_offset = y_offset + offset[1]
                                        max_adjacent = max(max_adjacent,num_adjacent)
                                    score = score + max_adjacent**2
        
        return score 


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them
        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them
        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move