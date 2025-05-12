"""
Utility module containing game constants, colors, and configuration settings.
This module serves as a central location for shared game parameters and settings.
"""

import pygame

# Color definitions for game elements
BLACK = (0, 0, 0)          # Background color
WHITE = (255, 255, 255)    # Text and UI elements
RED = (255, 0, 0)          # Player piece color option
GREEN = (0, 255, 0)        # Player piece color option
BLUE = (0, 0, 255)         # Base blue color
YELLOW = (255, 255, 0)     # AI piece color option
LIGHT_GREY = (200, 200, 200)  # UI elements and disabled states
LIGHT_BLUE = (100, 100, 255)  # Player piece color option
GOLD = (255, 215, 0)       # First place in leaderboard
SILVER = (192, 192, 192)   # Second place in leaderboard
BRONZE = (205, 127, 50)    # Third place in leaderboard
TITLE_YELLOW = (255, 255, 227)  # Game title color

# Game board dimensions and layout
ROW_COUNT = 6              # Number of rows in the game board
COLUMN_COUNT = 7           # Number of columns in the game board
SQUARESIZE = 100           # Size of each square in pixels
RADIUS = int(SQUARESIZE/2 - 5)  # Radius of game pieces
WINDOW_WIDTH = COLUMN_COUNT * SQUARESIZE    # Default window width
WINDOW_HEIGHT = (ROW_COUNT + 1) * SQUARESIZE  # Default window height
FPS = 60                   # Frames per second for game animation

# Game state constants
EMPTY = 0                  # Empty board position
PLAYER_PIECE = 1           # Player's piece identifier
AI_PIECE = 2              # AI's piece identifier

# Player turn constants
PLAYER = 0                 # Player's turn identifier
AI = 1                    # AI's turn identifier

# Game evaluation constants
WINDOW_LENGTH = 4          # Length of window for evaluating winning combinations

# UI constants
HEADER_HEIGHT = 30         # Height of the game header in pixels

# Base dimensions for scaling
BASE_SQUARESIZE = 100      # Base size for squares before scaling