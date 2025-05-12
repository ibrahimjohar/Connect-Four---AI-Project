"""
Main entry point for the Connect Four game.
Initializes Pygame, sets up the display, and manages the game flow.
"""

import pygame
import sys
import ctypes
from game import Game
from ui import LoadingScreen, GameMenu
from utils import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from ai_vs_ai import AIVsAIGame
from user_vs_user import UserVsUserGame

def main():
    """
    Main function that initializes the game and manages the game flow.
    Handles window setup, loading screen, menu navigation, and game mode selection.
    """
    # Initialize Pygame and set up the display
    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
    pygame.display.set_caption("Connect 4")
    
    # Maximize the window using Windows API
    try:
        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.ShowWindow(hwnd, 3)  # 3 = SW_MAXIMIZE
    except Exception as e:
        print("Could not maximize window:", e)
    
    # Start with loading screen
    loading_screen = LoadingScreen(screen)
    loading_screen.show()
    
    # Show menu and get player preferences
    current_w, current_h = screen.get_size()
    menu = GameMenu(screen, current_w, current_h)
    player_name, difficulty, sprite = menu.show()
    
    # Start game based on selected mode
    if difficulty == 'ai_vs_ai':
        ai_vs_ai_game = AIVsAIGame(screen, current_w, current_h)
        result = ai_vs_ai_game.run()
        # After AI vs AI game, return to menu
        if result:
            player_name, difficulty, sprite = result
            if difficulty == 'ai_vs_ai':
                ai_vs_ai_game = AIVsAIGame(screen, current_w, current_h)
                ai_vs_ai_game.run()
            elif difficulty == 'user_vs_user':
                user_vs_user_game = UserVsUserGame(screen, current_w, current_h)
                user_vs_user_game.run()
            else:
                game = Game(screen, player_name, difficulty, sprite)
                game.run()
    elif difficulty == 'user_vs_user':
        user_vs_user_game = UserVsUserGame(screen, current_w, current_h)
        user_vs_user_game.run()
    else:
        game = Game(screen, player_name, difficulty, sprite)
        game.run()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()