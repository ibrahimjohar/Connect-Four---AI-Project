import pygame
import sys
import random
from board import Board
from ai import AIPlayer
from ui import GameUI, Button, GameMenu
from utils import *
from utils import TITLE_YELLOW

class Game:
    def __init__(self, screen, player_name, difficulty, sprite_choice):
        self.screen = screen
        self.player_name = player_name
        self.difficulty = difficulty
        self.sprite_choice = sprite_choice

        self.board = Board()
        # Store current screen dimensions
        self.screen_width = WINDOW_WIDTH
        self.screen_height = WINDOW_HEIGHT
        self.ai_vs_ai = (difficulty == 'ai_vs_ai')
        self.ui = GameUI(screen, player_name, sprite_choice, self.screen_width, self.screen_height, ai_vs_ai=self.ai_vs_ai)
        self.ai = AIPlayer('hard' if difficulty == 'ai_vs_ai' else difficulty)
        if self.ai_vs_ai:
            self.ai2 = AIPlayer('hard')
            self.ai1_score = 0
            self.ai2_score = 0
        self.game_over = False
        self.turn = random.randint(PLAYER, AI)
        self.score = 0
        self.leaderboard = self.load_leaderboard()
        # Track fullscreen state
        self.fullscreen = False
        self.player_moves = 0  # Track player moves for scoring

    def toggle_fullscreen(self):
        """
        Toggle between windowed and fullscreen mode.
        """
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            # Enter fullscreen at current display resolution
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            # Update screen dimensions
            self.screen_width, self.screen_height = self.screen.get_size()
        else:
            # Return to original window size
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.screen_width, self.screen_height = WINDOW_WIDTH, WINDOW_HEIGHT
            
        # Update UI to draw on the new screen surface
        self.ui.screen = self.screen
        self.ui.screen_width = self.screen_width
        self.ui.screen_height = self.screen_height
        
        # Recalculate scale factor and dimensions
        self.ui.scale_factor = min(self.screen_width / WINDOW_WIDTH, self.screen_height / WINDOW_HEIGHT)
        self.ui.square_size = int(SQUARESIZE * self.ui.scale_factor)
        self.ui.radius = int(RADIUS * self.ui.scale_factor)
        
        # Clear the event queue to prevent stale inputs
        pygame.event.clear()
        
        # Force a redraw of the entire screen
        self.ui.draw_board(self.board.board)
        self.ui.draw_score(self.score)
        pygame.display.flip()

    def load_leaderboard(self):
        try:
            with open("leaderboard.txt", "r") as file:
                leaderboard = {}
                for line in file:
                    name, score = line.strip().split(":")
                    leaderboard[name] = int(score)
                return leaderboard
        except FileNotFoundError:
            return {}

    def save_leaderboard(self):
        with open("leaderboard.txt", "w") as file:
            for name, score in self.leaderboard.items():
                file.write(f"{name}:{score}\n")

    def update_leaderboard(self):
        if self.player_name in self.leaderboard:
            if self.score > self.leaderboard[self.player_name]:
                self.leaderboard[self.player_name] = self.score
        else:
            self.leaderboard[self.player_name] = self.score
        self.save_leaderboard()

    def handle_events(self):
        if self.ai_vs_ai:
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
            return
        else:
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
                    continue
                if self.game_over:
                    continue
                if event.type == pygame.MOUSEMOTION:
                    self.ui.update_hover(event.pos[0])
                if event.type == pygame.MOUSEBUTTONDOWN and self.turn == PLAYER:
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
                            print(f"Player dropping piece at col: {col}")
                            row = self.board.get_next_open_row(col)
                            self.board.drop_piece(row, col, PLAYER_PIECE)
                            self.player_moves += 1  # Increment player move count
                            if self.board.winning_move(PLAYER_PIECE):
                                self.score = max(1000 - 20 * self.player_moves, 100)
                                self.ui.show_winner(self.player_name)
                                self.game_over = True
                                self.update_leaderboard()
                            elif len(self.board.get_valid_locations()) == 0:
                                self.score = 50  # Draw
                                self.ui.show_winner("Draw")
                                self.game_over = True
                                self.update_leaderboard()
                            self.turn = AI

    def ai_move(self):
        if self.turn == AI and not self.game_over:
            # Check if there are valid moves
            valid_locations = self.board.get_valid_locations()
            if not valid_locations:
                # Board is full, declare a draw
                self.score = 50  # Draw
                self.ui.show_winner("Draw")
                self.game_over = True
                self.update_leaderboard()
                return

            col = self.ai.get_move(self.board)
            if col is None or not self.board.is_valid_location(col):
                # Log error and treat as draw for safety
                print(f"AI returned invalid move: {col}. Valid locations: {valid_locations}")
                self.score = 50  # Draw
                self.ui.show_winner("Draw")
                self.game_over = True
                self.update_leaderboard()
                return

            row = self.board.get_next_open_row(col)
            self.board.drop_piece(row, col, AI_PIECE)
            print(f"AI placed piece in column {col}, row {row}")  # Debug log

            if self.board.winning_move(AI_PIECE):
                self.score = 0  # Loss
                self.ui.show_winner("AI")
                self.game_over = True
                self.update_leaderboard()
            elif len(self.board.get_valid_locations()) == 0:
                self.score = 50  # Draw
                self.ui.show_winner("Draw")
                self.game_over = True
                self.update_leaderboard()

            self.turn = PLAYER

    def run(self):
        from ui import Button, GameMenu
        started = not self.ai_vs_ai
        while True:
            self.handle_events()
            if self.ai_vs_ai and not started:
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
                    self.ui.draw_score(self.score)
                    start_button.draw()
                    pygame.display.update()
                continue
            if self.ai_vs_ai:
                if not self.game_over:
                    # AI 1 (PLAYER_PIECE)
                    col1 = self.ai.get_move(self.board)
                    if col1 is not None and self.board.is_valid_location(col1):
                        row1 = self.board.get_next_open_row(col1)
                        self.board.drop_piece(row1, col1, PLAYER_PIECE)
                        self.player_moves += 1
                        if self.board.winning_move(PLAYER_PIECE):
                            self.ai1_score = max(1000 - 20 * self.player_moves, 100)
                            self.ai2_score = 0
                            self.ui.show_winner("AI 1")
                            self.game_over = True
                            self.update_leaderboard()
                            continue
                        elif len(self.board.get_valid_locations()) == 0:
                            self.ai1_score = 50
                            self.ai2_score = 50
                            self.ui.show_winner("Draw")
                            self.game_over = True
                            self.update_leaderboard()
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
                                self.update_leaderboard()
                                continue
                            elif len(self.board.get_valid_locations()) == 0:
                                self.ai1_score = 50
                                self.ai2_score = 50
                                self.ui.show_winner("Draw")
                                self.game_over = True
                                self.update_leaderboard()
                                continue
                        pygame.display.update()
                        pygame.time.wait(1200)
            else:
                self.ai_move()

            # Draw the game
            self.ui.draw_board(self.board.board)
            if self.ai_vs_ai:
                self.ui.draw_score((self.ai1_score, self.ai2_score))
            else:
                self.ui.draw_score(self.score)

            if self.game_over:
                # Wait for 1 second before showing options
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
                            pygame.event.clear()  # Clear events after returning from leaderboard
                            continue  # Continue the button loop, don't exit
                        if menu_button.is_clicked(pygame.mouse.get_pos(), event):
                            waiting = False
                    self.screen.fill(BLACK)
                    self.ui.draw_board(self.board.board)
                    if self.ai_vs_ai:
                        self.ui.draw_score((self.ai1_score, self.ai2_score))
                    else:
                        self.ui.draw_score(self.score)
                    # Draw semi-transparent overlay over the entire screen
                    overlay_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                    overlay_surface.fill((0, 0, 0, 180))
                    self.screen.blit(overlay_surface, (0, 0))
                    # Draw the victory/loss message centered above the buttons
                    from ui import BOXING_FONT_PATH
                    font = pygame.font.Font(BOXING_FONT_PATH, 48)
                    if self.ai_vs_ai:
                        if self.board.winning_move(PLAYER_PIECE):
                            msg = "AI 1 wins!"
                            color = self.ui.player_color
                        elif self.board.winning_move(AI_PIECE):
                            msg = "AI 2 wins!"
                            color = self.ui.ai_color
                        else:
                            msg = "game is a Draw!"
                            color = (255, 255, 255)
                    else:
                        if self.board.winning_move(PLAYER_PIECE):
                            msg = f"{self.player_name} wins!"
                            color = self.ui.player_color
                        elif self.board.winning_move(AI_PIECE):
                            msg = "AI wins!"
                            color = self.ui.ai_color
                        else:
                            msg = "game is a Draw!"
                            color = (255, 255, 255)
                    label = font.render(msg, True, color)
                    # Center the label horizontally, and place it above the buttons
                    label_x = center_x - label.get_width() // 2
                    label_y = center_y - button_height - label.get_height() - 30
                    self.screen.blit(label, (label_x, label_y))
                    # Draw the buttons below the message
                    leaderboard_button.draw()
                    menu_button.draw()
                    pygame.display.update()
                # Return to menu
                current_w, current_h = self.screen.get_size()
                menu = GameMenu(self.screen, current_w, current_h)
                player_name, difficulty, sprite = menu.show()
                self.__init__(self.screen, player_name, difficulty, sprite)
            pygame.display.update()
