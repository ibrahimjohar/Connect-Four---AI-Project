import random
import math
import numpy as np

class AIPlayer:
    def __init__(self, difficulty):
        self.difficulty = difficulty  # "easy", "medium", "hard"
    
    def get_move(self, board):
        if self.difficulty == "easy":
            return self.minimax_move(board, depth=1)
        elif self.difficulty == "medium":
            return self.minimax_move(board, depth=3)
        else:  # hard
            return self.minimax_move(board, depth=5)
    
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