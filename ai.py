import random
import math
import numpy as np

class AIPlayer:
    def __init__(self, difficulty):
        self.difficulty = difficulty  # "easy", "medium", "hard"
    
    def get_move(self, board):
        if self.difficulty == "easy":
            return self.random_move(board)
        elif self.difficulty == "medium":
            return self.monte_carlo_move(board)
        else:  # hard
            return self.minimax_move(board)
    
    def random_move(self, board):
        valid_locations = board.get_valid_locations()
        if valid_locations:
            return random.choice(valid_locations)
        return 0
    
    def monte_carlo_move(self, board):
        valid_locations = board.get_valid_locations()
        if not valid_locations:
            return 0
        
        # Run simulations for each possible move
        scores = {}
        simulations = 100  # Number of simulations per move
        
        for col in valid_locations:
            scores[col] = 0
            for _ in range(simulations):
                # Make a copy of the board
                temp_board = board.copy()
                row = temp_board.get_next_open_row(col)
                temp_board.drop_piece(row, col, 2)  # AI piece
                
                # Run a random simulation
                result = self.simulate_random_game(temp_board)
                if result == 2:  # AI wins
                    scores[col] += 1
                elif result == 0:  # Draw
                    scores[col] += 0.5
        
        # Choose the move with the highest score
        best_score = -1
        best_col = random.choice(valid_locations)
        
        for col in valid_locations:
            if scores[col] > best_score:
                best_score = scores[col]
                best_col = col
        
        return best_col
    
    def simulate_random_game(self, board):
        temp_board = board.copy()
        current_player = 1  # Start with player
        
        while not temp_board.is_terminal_node():
            valid_locations = temp_board.get_valid_locations()
            if not valid_locations:
                return 0  # Draw
            
            col = random.choice(valid_locations)
            row = temp_board.get_next_open_row(col)
            temp_board.drop_piece(row, col, current_player)
            
            if temp_board.winning_move(current_player):
                return current_player
            
            # Switch player
            current_player = 3 - current_player  # 1 -> 2, 2 -> 1
        
        return 0  # Draw
    
    def minimax_move(self, board, depth=5):
        col, _ = self.minimax(board, depth, -math.inf, math.inf, True)
        return col
    
    def minimax(self, board, depth, alpha, beta, maximizing_player):
        valid_locations = board.get_valid_locations()
        is_terminal = board.is_terminal_node()
        
        if depth == 0 or is_terminal:
            if is_terminal:
                if board.winning_move(2):  # AI wins
                    return (None, 1000000)
                elif board.winning_move(1):  # Player wins
                    return (None, -1000000)
                else:  # Draw
                    return (None, 0)
            else:  # Depth is zero
                return (None, board.score_position(2))
        
        if maximizing_player:
            value = -math.inf
            column = random.choice(valid_locations) if valid_locations else 0
            
            for col in valid_locations:
                row = board.get_next_open_row(col)
                temp_board = board.copy()
                temp_board.drop_piece(row, col, 2)
                new_score = self.minimax(temp_board, depth-1, alpha, beta, False)[1]
                
                if new_score > value:
                    value = new_score
                    column = col
                
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            
            return column, value
        
        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations) if valid_locations else 0
            
            for col in valid_locations:
                row = board.get_next_open_row(col)
                temp_board = board.copy()
                temp_board.drop_piece(row, col, 1)
                new_score = self.minimax(temp_board, depth-1, alpha, beta, True)[1]
                
                if new_score < value:
                    value = new_score
                    column = col
                
                beta = min(beta, value)
                if alpha >= beta:
                    break
            
            return column, value