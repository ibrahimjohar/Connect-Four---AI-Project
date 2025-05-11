import pygame
import sys
import random
from board import Board
from ai import AIPlayer
from ui import GameUI, Button, GameMenu
from utils import *

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
        self.ui = GameUI(screen, player_name, sprite_choice, self.screen_width, self.screen_height)
        self.ai = AIPlayer(difficulty)

        self.game_over = False
        self.turn = random.randint(PLAYER, AI)
        self.score = 0
        self.leaderboard = self.load_leaderboard()
        # Track fullscreen state
        self.fullscreen = False

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle window resize events
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
                # Only process clicks within the board area
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

                        if self.board.winning_move(PLAYER_PIECE):
                            self.score += 100
                            self.ui.show_winner(self.player_name)
                            self.game_over = True
                            self.update_leaderboard()
                        elif len(self.board.get_valid_locations()) == 0:
                            # Draw: board is full and no winner
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
                self.ui.show_winner("Draw")
                self.game_over = True
                self.update_leaderboard()
                return

            col = self.ai.get_move(self.board)
            if col is None or not self.board.is_valid_location(col):
                # Log error and treat as draw for safety
                print(f"AI returned invalid move: {col}. Valid locations: {valid_locations}")
                self.ui.show_winner("Draw")
                self.game_over = True
                self.update_leaderboard()
                return

            row = self.board.get_next_open_row(col)
            self.board.drop_piece(row, col, AI_PIECE)
            print(f"AI placed piece in column {col}, row {row}")  # Debug log

            if self.board.winning_move(AI_PIECE):
                self.ui.show_winner("AI")
                self.game_over = True
                self.update_leaderboard()
            elif len(self.board.get_valid_locations()) == 0:
                self.ui.show_winner("Draw")
                self.game_over = True
                self.update_leaderboard()

            self.turn = PLAYER

    def run(self):
        from ui import Button, GameMenu
        while True:
            self.handle_events()
            self.ai_move()

            # Draw the game
            self.ui.draw_board(self.board.board)
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
                leaderboard_button = Button(self.screen, "View Leaderboard", center_x - button_width//2, center_y - button_height - 10, button_width, button_height, BLUE, LIGHT_BLUE)
                menu_button = Button(self.screen, "Back to Menu", center_x - button_width//2, center_y + 10, button_width, button_height, GREEN, (100, 255, 100))
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
                            self.ui.scale_factor = min(event.w / WINDOW_WIDTH, event.h / WINDOW_HEIGHT)
                            self.ui.square_size = int(SQUARESIZE * self.ui.scale_factor)
                            self.ui.radius = int(RADIUS * self.ui.scale_factor)
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
                            menu = GameMenu(self.screen, self.screen_width, self.screen_height)
                            menu.show_leaderboard()
                            pygame.event.clear()  # Clear events after returning from leaderboard
                            continue  # Continue the button loop, don't exit
                        if menu_button.is_clicked(pygame.mouse.get_pos(), event):
                            waiting = False
                    self.screen.fill(BLACK)
                    self.ui.draw_board(self.board.board)
                    self.ui.draw_score(self.score)
                    leaderboard_button.draw()
                    menu_button.draw()
                    pygame.display.update()
                # Return to menu
                menu = GameMenu(self.screen, self.screen_width, self.screen_height)
                player_name, difficulty, sprite = menu.show()
                self.__init__(self.screen, player_name, difficulty, sprite)
            pygame.display.update()
