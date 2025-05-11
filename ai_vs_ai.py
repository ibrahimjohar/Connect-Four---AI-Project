import pygame
import sys
import random
from board import Board
from ui import GameUI, Button, GameMenu
from utils import *
from ai import AIPlayer

class RandomizedAIPlayer(AIPlayer):
    def minimax(self, board, depth, alpha, beta, maximizing_player):
        valid_locations = board.get_valid_locations()
        is_terminal = board.is_terminal_node()
        if depth == 0 or is_terminal:
            if is_terminal:
                if board.winning_move(2):
                    return (None, 1000000)
                elif board.winning_move(1):
                    return (None, -1000000)
                else:
                    return (None, 0)
            else:
                return (None, board.score_position(2))
        if maximizing_player:
            value = -float('inf')
            best_cols = []
            for col in valid_locations:
                row = board.get_next_open_row(col)
                temp_board = board.copy()
                temp_board.drop_piece(row, col, 2)
                new_score = self.minimax(temp_board, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    best_cols = [col]
                elif new_score == value:
                    best_cols.append(col)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return (random.choice(best_cols), value)
        else:
            value = float('inf')
            best_cols = []
            for col in valid_locations:
                row = board.get_next_open_row(col)
                temp_board = board.copy()
                temp_board.drop_piece(row, col, 1)
                new_score = self.minimax(temp_board, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    best_cols = [col]
                elif new_score == value:
                    best_cols.append(col)
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return (random.choice(best_cols), value)

class AIVsAIGame:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board = Board()
        self.ui = GameUI(screen, "AI 1", "Red", screen_width, screen_height, ai_vs_ai=True)
        self.ai1 = RandomizedAIPlayer("hard")
        self.ai2 = RandomizedAIPlayer("hard")
        self.ai1_score = 0
        self.ai2_score = 0
        self.game_over = False
        self.player_moves = 0

    def run(self):
        from ui import Button
        started = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.screen_width = event.w
                    self.screen_height = event.h
                    self.ui.screen = self.screen
                    self.ui.screen_width = event.w
                    self.ui.screen_height = event.h
                    self.ui.update_layout()
            if not started:
                # Show a 'Start Game' button in the center
                button_width = 300
                button_height = 80
                screen_width = self.screen.get_width()
                screen_height = self.screen.get_height()
                center_x = screen_width // 2
                center_y = screen_height // 2
                start_button = Button(self.screen, "Start Game", center_x - button_width//2, center_y - button_height//2, button_width, button_height, (255, 230, 80), (255, 255, 180), BLACK, BLACK, BLACK)
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.VIDEORESIZE:
                            self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                            self.screen_width = event.w
                            self.screen_height = event.h
                            self.ui.screen = self.screen
                            self.ui.screen_width = event.w
                            self.ui.screen_height = event.h
                            self.ui.update_layout()
                            screen_width = self.screen.get_width()
                            screen_height = self.screen.get_height()
                            center_x = screen_width // 2
                            center_y = screen_height // 2
                            start_button.rect.x = center_x - button_width//2
                            start_button.rect.y = center_y - button_height//2
                        start_button.check_hover(pygame.mouse.get_pos())
                        if start_button.is_clicked(pygame.mouse.get_pos(), event):
                            waiting = False
                            started = True
                    self.ui.draw_board(self.board.board)
                    self.ui.draw_score((self.ai1_score, self.ai2_score))
                    start_button.draw()
                    pygame.display.update()
                continue
            if not self.game_over:
                # AI 1 (PLAYER_PIECE)
                col1 = self.ai1.get_move(self.board)
                if col1 is not None and self.board.is_valid_location(col1):
                    row1 = self.board.get_next_open_row(col1)
                    self.board.drop_piece(row1, col1, PLAYER_PIECE)
                    self.player_moves += 1
                    if self.board.winning_move(PLAYER_PIECE):
                        self.ai1_score = max(1000 - 20 * self.player_moves, 100)
                        self.ai2_score = 0
                        self.ui.show_winner("AI 1")
                        self.game_over = True
                        continue
                    elif len(self.board.get_valid_locations()) == 0:
                        self.ai1_score = 50
                        self.ai2_score = 50
                        self.ui.show_winner("Draw")
                        self.game_over = True
                        continue
                pygame.display.update()
                pygame.time.wait(1200)
                # AI 2 (AI_PIECE)
                if not self.game_over:
                    col2 = self.ai2.get_move(self.board)
                    if col2 is not None and self.board.is_valid_location(col2):
                        row2 = self.board.get_next_open_row(col2)
                        self.board.drop_piece(row2, col2, AI_PIECE)
                        if self.board.winning_move(AI_PIECE):
                            self.ai1_score = 0
                            self.ai2_score = max(1000 - 20 * self.player_moves, 100)
                            self.ui.show_winner("AI 2")
                            self.game_over = True
                            continue
                        elif len(self.board.get_valid_locations()) == 0:
                            self.ai1_score = 50
                            self.ai2_score = 50
                            self.ui.show_winner("Draw")
                            self.game_over = True
                            continue
                    pygame.display.update()
                    pygame.time.wait(1200)
            self.ui.draw_board(self.board.board)
            self.ui.draw_score((self.ai1_score, self.ai2_score))
            if self.game_over:
                pygame.time.wait(1000)
                # Show buttons: View Leaderboard, Back to Menu
                button_width = 300
                button_height = 60
                screen_width = self.screen.get_width()
                screen_height = self.screen.get_height()
                center_x = screen_width // 2
                center_y = screen_height // 2
                leaderboard_button = Button(self.screen, "View Leaderboard", center_x - button_width//2, center_y - button_height - 10, button_width, button_height, BLACK, WHITE, WHITE, BLACK)
                menu_button = Button(self.screen, "Back to Menu", center_x - button_width//2, center_y + 10, button_width, button_height, TITLE_YELLOW, (255, 255, 180), BLACK, BLACK)
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.VIDEORESIZE:
                            self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                            self.screen_width = event.w
                            self.screen_height = event.h
                            self.ui.screen = self.screen
                            self.ui.screen_width = event.w
                            self.ui.screen_height = event.h
                            self.ui.update_layout()
                            screen_width = self.screen.get_width()
                            screen_height = self.screen.get_height()
                            center_x = screen_width // 2
                            center_y = screen_height // 2
                            leaderboard_button.rect.x = center_x - button_width//2
                            leaderboard_button.rect.y = center_y - button_height - 10
                            menu_button.rect.x = center_x - button_width//2
                            menu_button.rect.y = center_y + 10
                        leaderboard_button.check_hover(pygame.mouse.get_pos())
                        menu_button.check_hover(pygame.mouse.get_pos())
                        if leaderboard_button.is_clicked(pygame.mouse.get_pos(), event):
                            current_w, current_h = self.screen.get_size()
                            menu = GameMenu(self.screen, current_w, current_h)
                            menu.show_leaderboard()
                            pygame.event.clear()
                            continue
                        if menu_button.is_clicked(pygame.mouse.get_pos(), event):
                            waiting = False
                    self.screen.fill(BLACK)
                    self.ui.draw_board(self.board.board)
                    self.ui.draw_score((self.ai1_score, self.ai2_score))
                    # Draw semi-transparent overlay over the entire screen
                    overlay_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                    overlay_surface.fill((0, 0, 0, 180))
                    self.screen.blit(overlay_surface, (0, 0))
                    from ui import BOXING_FONT_PATH
                    font = pygame.font.Font(BOXING_FONT_PATH, 48)
                    if self.board.winning_move(PLAYER_PIECE):
                        msg = "AI 1 wins!"
                        color = self.ui.player_color
                    elif self.board.winning_move(AI_PIECE):
                        msg = "AI 2 wins!"
                        color = self.ui.ai_color
                    else:
                        msg = "game is a Draw!"
                        color = (255, 255, 255)
                    label = font.render(msg, True, color)
                    label_x = center_x - label.get_width() // 2
                    label_y = center_y - button_height - label.get_height() - 30
                    self.screen.blit(label, (label_x, label_y))
                    leaderboard_button.draw()
                    menu_button.draw()
                    pygame.display.update()
                # Return to menu
                current_w, current_h = self.screen.get_size()
                menu = GameMenu(self.screen, current_w, current_h)
                player_name, difficulty, sprite = menu.show()
                return (player_name, difficulty, sprite) 