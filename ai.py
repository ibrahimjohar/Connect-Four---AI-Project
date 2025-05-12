"""
AI player module implementing the Minimax algorithm with alpha-beta pruning.
This module provides the AI logic for making moves in the Connect Four game.
"""

import random
import math
import numpy as np

class AIPlayer:
    """
    AI player class that uses the Minimax algorithm to determine optimal moves.
    Supports different difficulty levels by adjusting the search depth.
    """
    
    def __init__(self, difficulty):
        """
        Initialize the AI player with a specified difficulty level.
        
        Args:
            difficulty (str): AI difficulty level ("easy", "medium", or "hard")
        """
        self.difficulty = difficulty
    
    def get_move(self, board):
        """
        Determine the next move based on the current board state and difficulty level.
        
        Args:
            board (Board): Current game board state
            
        Returns:
            int: Column index for the AI's move
        """
        if self.difficulty == "easy":
            return self.minimax_move(board, depth=1)
        elif self.difficulty == "medium":
            return self.minimax_move(board, depth=3)
        else:  # hard
            return self.minimax_move(board, depth=5)
    
    def minimax_move(self, board, depth=5):
        """
        Get the best move using the Minimax algorithm.
        
        Args:
            board (Board): Current game board state
            depth (int): Maximum depth for the minimax search
            
        Returns:
            int: Column index for the best move
        """
        col, _ = self.minimax(board, depth, -math.inf, math.inf, True)
        return col
    
    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Implement the Minimax algorithm with alpha-beta pruning.
        
        Args:
            board (Board): Current game board state
            depth (int): Remaining search depth
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            maximizing_player (bool): True if maximizing player's turn
            
        Returns:
            tuple: (column index, score) for the best move
        """
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