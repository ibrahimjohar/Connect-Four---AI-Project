import pygame
import sys
import random
from board import Board
from ai import AIPlayer
from ui import GameUI
from utils import *

class Game:
    def __init__(self, screen, player_name, difficulty, sprite_choice):
        self.screen = screen
        self.player_name = player_name
        self.difficulty = difficulty
        self.sprite_choice = sprite_choice

        self.board = Board()
        self.ui = GameUI(screen, player_name, sprite_choice)
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
        else:
            # Return to original window size
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Update UI to draw on the new screen surface
        self.ui.screen = self.screen
        
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

            # Toggle fullscreen on F11
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                self.toggle_fullscreen()
                continue

            if self.game_over:
                continue

            if event.type == pygame.MOUSEMOTION:
                self.ui.update_hover(event.pos[0])

            if event.type == pygame.MOUSEBUTTONDOWN and self.turn == PLAYER:
                col = int(event.pos[0] // SQUARESIZE)

                if self.board.is_valid_location(col):
                    row = self.board.get_next_open_row(col)
                    self.board.drop_piece(row, col, PLAYER_PIECE)

                    if self.board.winning_move(PLAYER_PIECE):
                        self.score += 100
                        self.ui.show_winner(self.player_name)
                        self.game_over = True
                        self.update_leaderboard()

                    self.turn = AI

    def ai_move(self):
        if self.turn == AI and not self.game_over:
            col = self.ai.get_move(self.board)

            if self.board.is_valid_location(col):
                row = self.board.get_next_open_row(col)
                self.board.drop_piece(row, col, AI_PIECE)

                if self.board.winning_move(AI_PIECE):
                    self.ui.show_winner("AI")
                    self.game_over = True
                    self.update_leaderboard()

                self.turn = PLAYER

    def run(self):
        while True:
            self.handle_events()
            self.ai_move()

            # Draw the game
            self.ui.draw_board(self.board.board)
            self.ui.draw_score(self.score)

            if self.game_over:
                # Wait for 3 seconds before exiting
                pygame.time.wait(3000)
                # Return to menu
                from ui import GameMenu
                menu = GameMenu(self.screen)
                player_name, difficulty, sprite = menu.show()
                self.__init__(self.screen, player_name, difficulty, sprite)

            pygame.display.update()
