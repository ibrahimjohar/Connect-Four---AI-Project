import pygame
import sys
from game import Game
from ui import LoadingScreen, GameMenu
from utils import WINDOW_WIDTH, WINDOW_HEIGHT, FPS

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Connect 4")
    
    # Start with loading screen
    loading_screen = LoadingScreen(screen)
    loading_screen.show()
    
    # Show menu
    menu = GameMenu(screen)
    player_name, difficulty, sprite = menu.show()
    
    # Start game
    game = Game(screen, player_name, difficulty, sprite)
    game.run()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()