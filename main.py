import pygame
import sys
import ctypes
from game import Game
from ui import LoadingScreen, GameMenu
from utils import WINDOW_WIDTH, WINDOW_HEIGHT, FPS

def main():
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
    
    # Show menu
    current_w, current_h = screen.get_size()
    menu = GameMenu(screen, current_w, current_h)
    player_name, difficulty, sprite = menu.show()
    
    # Start game
    game = Game(screen, player_name, difficulty, sprite)
    game.run()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()