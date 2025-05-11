import pygame
import sys
import random
from board import Board
from ui import GameUI, Button, GameMenu
from utils import *
from ai import AIPlayer
import datetime

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

    def load_leaderboard(self):
        try:
            with open("ai_vs_ai_leaderboard.txt", "r") as file:
                leaderboard = []
                for line in file:
                    leaderboard.append(line.strip())
                return leaderboard
        except FileNotFoundError:
            return []

    def save_leaderboard(self, leaderboard):
        with open("ai_vs_ai_leaderboard.txt", "w") as file:
            for entry in leaderboard:
                file.write(f"{entry}\n")

    def update_leaderboard(self, result_entry):
        leaderboard = self.load_leaderboard()
        leaderboard.append(result_entry)
        # Sort by the highest score in the entry (extract numbers and sort)
        def extract_score(entry):
            import re
            scores = [int(s) for s in re.findall(r": (\d+)", entry)]
            return max(scores) if scores else 0
        leaderboard.sort(key=extract_score, reverse=True)
        self.save_leaderboard(leaderboard)

    def show_leaderboard(self):
        leaderboard = self.load_leaderboard()
        # Display like the user leaderboard, but with AI names and scores
        pygame.event.clear()
        viewing = True
        scale_factor = min(self.screen_width / WINDOW_WIDTH, self.screen_height / WINDOW_HEIGHT)
        font_large = pygame.font.Font(BOXING_FONT_PATH, int(48 * scale_factor))
        font = pygame.font.Font(BOXING_FONT_PATH, int(32 * scale_factor))
        center_x = self.screen_width / 2
        scroll_offset = 0
        max_visible = 10
        while viewing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.screen_width = event.w
                    self.screen_height = event.h
                    scale_factor = min(self.screen_width / WINDOW_WIDTH, self.screen_height / WINDOW_HEIGHT)
                    font_large = pygame.font.Font(BOXING_FONT_PATH, int(48 * scale_factor))
                    font = pygame.font.Font(BOXING_FONT_PATH, int(32 * scale_factor))
                    center_x = self.screen_width / 2
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if scroll_offset < max(0, len(leaderboard) - max_visible):
                            scroll_offset += 1
                    if event.key == pygame.K_UP:
                        if scroll_offset > 0:
                            scroll_offset -= 1
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        viewing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll up
                        if scroll_offset > 0:
                            scroll_offset -= 1
                    if event.button == 5:  # Scroll down
                        if scroll_offset < max(0, len(leaderboard) - max_visible):
                            scroll_offset += 1
                    if event.button == 1 or event.button == 3:
                        viewing = False
            # Draw background image (other) with aspect ratio preserved
            self.ui.blit_centered_bg(self.ui.bg_game, self.screen)
            # Draw semi-transparent overlay over the entire screen
            overlay_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay_surface.fill((0, 0, 0, 180))
            self.screen.blit(overlay_surface, (0, 0))
            # Title
            title = font_large.render("AI vs AI Leaderboard", True, GOLD)
            self.screen.blit(title, (center_x - title.get_width() / 2, 80 * scale_factor))
            # Entries (with scroll)
            y_start = 180 * scale_factor
            line_height = 40 * scale_factor
            if not leaderboard:
                no_scores = font.render("No AI vs AI games yet!", True, WHITE)
                self.screen.blit(no_scores, (center_x - no_scores.get_width() / 2, y_start))
            else:
                for i, entry in enumerate(leaderboard[scroll_offset:scroll_offset+max_visible]):
                    color = GOLD if i+scroll_offset == 0 else SILVER if i+scroll_offset == 1 else BRONZE if i+scroll_offset == 2 else WHITE
                    entry_text = font.render(entry, True, color)
                    self.screen.blit(entry_text, (center_x - entry_text.get_width() / 2, y_start + i * line_height))
            # Scroll instructions
            if len(leaderboard) > max_visible:
                small_font = pygame.font.Font(BOXING_FONT_PATH, int(20 * scale_factor))
                scroll_text = small_font.render("Scroll to see more", True, LIGHT_GREY)
                self.screen.blit(scroll_text, (center_x - scroll_text.get_width() / 2, self.screen_height - 80 * scale_factor))
            # Back instruction
            small_font = pygame.font.Font(BOXING_FONT_PATH, int(20 * scale_factor))
            back_text = small_font.render("Press any key to return", True, LIGHT_GREY)
            self.screen.blit(back_text, (center_x - back_text.get_width() / 2, self.screen_height - 40 * scale_factor))
            pygame.display.update()

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
                # Log result to AI vs AI leaderboard with timestamp, move count, and winner
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                total_moves = sum(1 for row in self.board.board.flatten() if row != 0)
                if self.board.winning_move(PLAYER_PIECE):
                    winner = "AI 1"
                    result_entry = f"[{now}] Winner: AI 1 | Moves: {total_moves} | AI 1: {self.ai1_score}, AI 2: {self.ai2_score}"
                elif self.board.winning_move(AI_PIECE):
                    winner = "AI 2"
                    result_entry = f"[{now}] Winner: AI 2 | Moves: {total_moves} | AI 2: {self.ai2_score}, AI 1: {self.ai1_score}"
                else:
                    winner = "Draw"
                    result_entry = f"[{now}] Winner: Draw | Moves: {total_moves} | Draw: {self.ai1_score}, {self.ai2_score}"
                self.update_leaderboard(result_entry)
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
                            self.show_leaderboard()
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