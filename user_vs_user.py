import pygame
import sys
import datetime
from board import Board
from ui import GameUI, Button, GameMenu, BOXING_FONT_PATH
from utils import *

class UserVsUserGame:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board = Board()
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        self.ui = GameUI(screen, self.player1_name, "Red", screen_width, screen_height, ai_vs_ai=False)
        self.player1_score = 0
        self.player2_score = 0
        self.game_over = False
        self.player_moves = 0
        self.turn = 0  # 0 for player 1, 1 for player 2

    def prompt_names(self):
        # Simple prompt for both player names using the menu UI
        menu = GameMenu(self.screen, self.screen_width, self.screen_height)
        # First player
        menu.name_input = ""
        menu.active = True
        while True:
            back, next_ = menu.show_name_input()
            if next_:
                self.player1_name = menu.name_input
                break
        # Second player
        menu.name_input = ""
        menu.active = True
        while True:
            back, next_ = menu.show_name_input()
            if next_:
                self.player2_name = menu.name_input
                break
        # Update UI with player 1's name
        self.ui.player_name = self.player1_name

    def load_leaderboard(self):
        try:
            with open("user_vs_user_leaderboard.txt", "r") as file:
                leaderboard = []
                for line in file:
                    leaderboard.append(line.strip())
                return leaderboard
        except FileNotFoundError:
            return []

    def save_leaderboard(self, leaderboard):
        with open("user_vs_user_leaderboard.txt", "w") as file:
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
            self.ui.blit_centered_bg(self.ui.bg_game, self.screen)
            overlay_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay_surface.fill((0, 0, 0, 180))
            self.screen.blit(overlay_surface, (0, 0))
            title = font_large.render("User vs User Leaderboard", True, GOLD)
            self.screen.blit(title, (center_x - title.get_width() / 2, 80 * scale_factor))
            y_start = 180 * scale_factor
            line_height = 40 * scale_factor
            if not leaderboard:
                no_scores = font.render("No user vs user games yet!", True, WHITE)
                self.screen.blit(no_scores, (center_x - no_scores.get_width() / 2, y_start))
            else:
                for i, entry in enumerate(leaderboard[scroll_offset:scroll_offset+max_visible]):
                    color = GOLD if i+scroll_offset == 0 else SILVER if i+scroll_offset == 1 else BRONZE if i+scroll_offset == 2 else WHITE
                    entry_text = font.render(entry, True, color)
                    self.screen.blit(entry_text, (center_x - entry_text.get_width() / 2, y_start + i * line_height))
            if len(leaderboard) > max_visible:
                small_font = pygame.font.Font(BOXING_FONT_PATH, int(20 * scale_factor))
                scroll_text = small_font.render("Scroll to see more", True, LIGHT_GREY)
                self.screen.blit(scroll_text, (center_x - scroll_text.get_width() / 2, self.screen_height - 80 * scale_factor))
            small_font = pygame.font.Font(BOXING_FONT_PATH, int(20 * scale_factor))
            back_text = small_font.render("Press any key to return", True, LIGHT_GREY)
            self.screen.blit(back_text, (center_x - back_text.get_width() / 2, self.screen_height - 40 * scale_factor))
            pygame.display.update()

    def run(self):
        from ui import Button
        self.prompt_names()
        self.ui.player_name = self.player1_name
        started = True
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
                if self.game_over:
                    continue
                if event.type == pygame.MOUSEMOTION:
                    self.ui.update_hover(event.pos[0])
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    self.ui.update_layout()
                    x_offset, y_offset = self.ui.get_offsets()
                    board_width = self.ui.square_size * COLUMN_COUNT
                    board_height = self.ui.square_size * (ROW_COUNT + 1)
                    if (x_offset <= event.pos[0] <= x_offset + board_width and
                        y_offset + self.ui.square_size <= event.pos[1] <= y_offset + board_height):
                        adjusted_x_pos = event.pos[0] - x_offset
                        col = int(adjusted_x_pos // self.ui.square_size)
                        col = max(0, min(COLUMN_COUNT - 1, col))
                        if self.board.is_valid_location(col):
                            row = self.board.get_next_open_row(col)
                            piece = PLAYER_PIECE if self.turn == 0 else AI_PIECE
                            self.board.drop_piece(row, col, piece)
                            self.player_moves += 1
                            if self.board.winning_move(piece):
                                if self.turn == 0:
                                    self.player1_score = max(1000 - 20 * self.player_moves, 100)
                                    self.player2_score = 0
                                else:
                                    self.player1_score = 0
                                    self.player2_score = max(1000 - 20 * self.player_moves, 100)
                                self.game_over = True
                                self.ui.show_winner(self.player1_name if self.turn == 0 else self.player2_name)
                                continue
                            elif len(self.board.get_valid_locations()) == 0:
                                self.player1_score = 50
                                self.player2_score = 50
                                self.game_over = True
                                self.ui.show_winner("Draw")
                                continue
                            self.turn = 1 - self.turn
                            self.ui.player_name = self.player1_name if self.turn == 0 else self.player2_name
            self.ui.draw_board(self.board.board)
            self.ui.draw_score((self.player1_score, self.player2_score))
            if self.game_over:
                # Log result to leaderboard with timestamp, move count, and winner
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                total_moves = sum(1 for row in self.board.board.flatten() if row != 0)
                if self.player1_score > self.player2_score:
                    winner = self.player1_name
                    result_entry = f"[{now}] Winner: {self.player1_name} | Moves: {total_moves} | {self.player1_name}: {self.player1_score}, {self.player2_name}: {self.player2_score}"
                elif self.player2_score > self.player1_score:
                    winner = self.player2_name
                    result_entry = f"[{now}] Winner: {self.player2_name} | Moves: {total_moves} | {self.player2_name}: {self.player2_score}, {self.player1_name}: {self.player1_score}"
                else:
                    winner = "Draw"
                    result_entry = f"[{now}] Winner: Draw | Moves: {total_moves} | Draw: {self.player1_score}, {self.player2_score}"
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
                    self.ui.draw_score((self.player1_score, self.player2_score))
                    overlay_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                    overlay_surface.fill((0, 0, 0, 180))
                    self.screen.blit(overlay_surface, (0, 0))
                    from ui import BOXING_FONT_PATH
                    font = pygame.font.Font(BOXING_FONT_PATH, 48)
                    if self.player1_score > self.player2_score:
                        msg = f"{self.player1_name} wins!"
                        color = self.ui.player_color
                    elif self.player2_score > self.player1_score:
                        msg = f"{self.player2_name} wins!"
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
                return menu.show() 