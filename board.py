import numpy as np

class Board:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.board = np.zeros((rows, columns))
    
    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece
    
    def is_valid_location(self, col):
        return col >= 0 and col < self.columns and self.board[self.rows-1][col] == 0
    
    def get_next_open_row(self, col):
        for r in range(self.rows):
            if self.board[r][col] == 0:
                return r
        return -1
    
    def winning_move(self, piece):
        # Check horizontal
        for c in range(self.columns-3):
            for r in range(self.rows):
                if (self.board[r][c] == piece and self.board[r][c+1] == piece and 
                    self.board[r][c+2] == piece and self.board[r][c+3] == piece):
                    return True
        
        # Check vertical
        for c in range(self.columns):
            for r in range(self.rows-3):
                if (self.board[r][c] == piece and self.board[r+1][c] == piece and 
                    self.board[r+2][c] == piece and self.board[r+3][c] == piece):
                    return True
        
        # Check positively sloped diagonals
        for c in range(self.columns-3):
            for r in range(self.rows-3):
                if (self.board[r][c] == piece and self.board[r+1][c+1] == piece and 
                    self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece):
                    return True
        
        # Check negatively sloped diagonals
        for c in range(self.columns-3):
            for r in range(3, self.rows):
                if (self.board[r][c] == piece and self.board[r-1][c+1] == piece and 
                    self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece):
                    return True
        
        return False
    
    def get_valid_locations(self):
        valid_locations = []
        for col in range(self.columns):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations
    
    def is_terminal_node(self):
        return (self.winning_move(1) or self.winning_move(2) or 
                len(self.get_valid_locations()) == 0)
    
    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = 1 if piece == 2 else 2
        
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2
            
        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4
            
        return score
    
    def score_position(self, piece):
        score = 0
        
        # Score center column
        center_array = [int(i) for i in list(self.board[:, self.columns//2])]
        center_count = center_array.count(piece)
        score += center_count * 3
        
        # Score horizontal
        for r in range(self.rows):
            row_array = [int(i) for i in list(self.board[r,:])]
            for c in range(self.columns-3):
                window = row_array[c:c+4]
                score += self.evaluate_window(window, piece)
        
        # Score vertical
        for c in range(self.columns):
            col_array = [int(i) for i in list(self.board[:,c])]
            for r in range(self.rows-3):
                window = col_array[r:r+4]
                score += self.evaluate_window(window, piece)
        
        # Score positive diagonal
        for r in range(self.rows-3):
            for c in range(self.columns-3):
                window = [self.board[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window, piece)
        
        # Score negative diagonal
        for r in range(self.rows-3):
            for c in range(self.columns-3):
                window = [self.board[r+3-i][c+i] for i in range(4)]
                score += self.evaluate_window(window, piece)
        
        return score
    
    def copy(self):
        new_board = Board(self.rows, self.columns)
        new_board.board = self.board.copy()
        return new_board