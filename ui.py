import sys
import pygame
import time
import os
from utils import *

class LoadingScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("CoolveticaRg-Regular", 40)
    
    def show(self):
        # Simple loading animation
        for i in range(101):
            self.screen.fill(BLACK)
            
            # Draw title
            title = self.font.render("Connect 4", True, WHITE)
            self.screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, WINDOW_HEIGHT//4))
            
            # Draw progress bar
            pygame.draw.rect(self.screen, WHITE, 
                            (WINDOW_WIDTH//4, WINDOW_HEIGHT//2, WINDOW_WIDTH//2, 30))
            pygame.draw.rect(self.screen, GREEN, 
                            (WINDOW_WIDTH//4, WINDOW_HEIGHT//2, (WINDOW_WIDTH//2) * (i/100), 30))
            
            # Draw loading text
            loading_text = self.font.render(f"Loading... {i}%", True, WHITE)
            self.screen.blit(loading_text, 
                            (WINDOW_WIDTH//2 - loading_text.get_width()//2, WINDOW_HEIGHT//2 + 50))
            
            pygame.display.update()
            time.sleep(0.01)  # Adjust for desired loading speed

class Button:
    def __init__(self, screen, text, x, y, width, height, color, hover_color):
        self.screen = screen
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont("CoolveticRg-Regular", 24)
        self.is_hovered = False
    
    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(self.screen, color, self.rect)
        pygame.draw.rect(self.screen, WHITE, self.rect, 2)  # Border
        
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.screen.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos):
            return True
        return False

class SpriteSelector:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 300
        self.height = 100
        self.font = pygame.font.SysFont("CoolveticaRg-Regular", 24)
        self.sprites = ["Red", "Blue", "Green"]
        self.current_sprite = 0
        
        self.left_button = Button(screen, "<", x, y, 30, 30, LIGHT_GREY, WHITE)
        self.right_button = Button(screen, ">", x + self.width - 30, y, 30, 30, LIGHT_GREY, WHITE)
    
    def draw(self):
        # Draw sprite preview
        # pygame.draw.rect(self.screen, WHITE, 
        #                 (self.x + 40, self.y - 10, self.width - 80, self.height))
        pygame.draw.rect(self.screen, WHITE, 
                        (self.x + 40, self.y - 0, self.width - 80, self.height), 2)
        
        # Draw sprite name
        text = self.font.render(self.sprites[self.current_sprite], True, WHITE)
        self.screen.blit(text, (self.x + self.width//2 - text.get_width()//2, self.y + 0))
        
        # Draw sprite preview circle
        sprite_color = self.get_sprite_color()
        pygame.draw.circle(self.screen, sprite_color, 
                          (self.x + self.width//2, self.y + 60), 20)
        
        # Draw navigation buttons
        self.left_button.draw()
        self.right_button.draw()
    
    def get_sprite_color(self):
        if self.sprites[self.current_sprite] == "Red":
            return RED
        elif self.sprites[self.current_sprite] == "Blue":
            return BLUE
        elif self.sprites[self.current_sprite] == "Green":
            return GREEN
        return RED
    
    def handle_event(self, event, mouse_pos):
        if self.left_button.is_clicked(mouse_pos, event):
            self.current_sprite = (self.current_sprite - 1) % len(self.sprites)
        elif self.right_button.is_clicked(mouse_pos, event):
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
        
        # Update button hover states
        self.left_button.check_hover(mouse_pos)
        self.right_button.check_hover(mouse_pos)
    
    def get_selected_sprite(self):
        return self.sprites[self.current_sprite]

class DifficultySelector:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 300
        self.height = 40
        self.font = pygame.font.SysFont("CoolveticaRg-Regular", 24)
        self.difficulties = ["easy", "medium", "hard"]
        self.buttons = []
        
        button_width = self.width // 3
        for i, diff in enumerate(self.difficulties):
            color = GREEN if diff == "easy" else YELLOW if diff == "medium" else RED
            hover_color = (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255))
            self.buttons.append(Button(screen, diff.capitalize(), 
                                      x + i * button_width, y, 
                                      button_width, self.height, 
                                      color, hover_color))
        
        self.selected = None  # Default to easy
    
    def draw(self):
        for i, button in enumerate(self.buttons):
            # Make selected button stand out
            if i == self.selected:
                pygame.draw.rect(self.screen, WHITE, 
                                (button.rect.x - 2, button.rect.y - 2, 
                                 button.rect.width + 4, button.rect.height + 4), 2)
            button.draw()
    
    def handle_event(self, event, mouse_pos):
        for i, button in enumerate(self.buttons):
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, event):
                self.selected = i
    
    def get_selected_difficulty(self):
        return self.difficulties[self.selected]

class GameMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont("CoolveticaRg-Regular", 48)
        self.font = pygame.font.SysFont("CoolveticaRg-Regular", 32)
        self.name_input = ""
        self.active = True
        
        # Create UI elements
        center_x = WINDOW_WIDTH // 2 - 150
        self.sprite_selector = SpriteSelector(screen, center_x, 300)
        self.difficulty_selector = DifficultySelector(screen, center_x, 450)
        self.start_button = Button(screen, "Start Game", center_x, 520, 300, 50, GREEN, (100, 255, 100))
        self.leaderboard_button = Button(screen, "Leaderboard", center_x, 580, 300, 50, BLUE, LIGHT_BLUE)
    
    def show(self):
        active_input = True
        
        while self.active:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Handle text input for name
                if active_input and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        active_input = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.name_input = self.name_input[:-1]
                    elif len(self.name_input) < 20:  # Limit name length
                        self.name_input += event.unicode
                
                # Handle button events
                self.sprite_selector.handle_event(event, mouse_pos)
                self.difficulty_selector.handle_event(event, mouse_pos)
                
                if self.start_button.is_clicked(mouse_pos, event):
                    if self.name_input.strip():  # Ensure name is not empty
                        self.active = False
                        return (self.name_input, 
                                self.difficulty_selector.get_selected_difficulty(),
                                self.sprite_selector.get_selected_sprite())
                
                if self.leaderboard_button.is_clicked(mouse_pos, event):
                    self.show_leaderboard()
            
            # Update hover states
            self.start_button.check_hover(mouse_pos)
            self.leaderboard_button.check_hover(mouse_pos)
            
            # Draw menu
            self.screen.fill(BLACK)
            
            # Draw title
            title = self.font_large.render("Connect 4", True, BLUE)
            self.screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 50))
            
            # Draw name input field
            name_prompt = self.font.render("Enter your name:", True, WHITE)
            self.screen.blit(name_prompt, (WINDOW_WIDTH//2 - 150, 150))
            
            pygame.draw.rect(self.screen, WHITE if active_input else LIGHT_GREY, 
                            (WINDOW_WIDTH//2 - 150, 190, 300, 40))
            pygame.draw.rect(self.screen, BLACK, 
                            (WINDOW_WIDTH//2 - 150, 190, 300, 40), 2)
            
            name_surface = self.font.render(self.name_input, True, BLACK)
            self.screen.blit(name_surface, (WINDOW_WIDTH//2 - 145, 195))
            
            # Draw cursor for text input
            if active_input and pygame.time.get_ticks() % 1000 < 500:
                cursor_pos = self.font.size(self.name_input)[0]
                pygame.draw.line(self.screen, BLACK, 
                                (WINDOW_WIDTH//2 - 145 + cursor_pos, 195),
                                (WINDOW_WIDTH//2 - 145 + cursor_pos, 195 + 30), 2)
            
            # Draw sprite selector
            sprite_text = self.font.render("Choose your piece:", True, WHITE)
            self.screen.blit(sprite_text, (WINDOW_WIDTH//2 - 150, 260))
            self.sprite_selector.draw()
            
            # Draw difficulty selector
            diff_text = self.font.render("Select difficulty:", True, WHITE)
            self.screen.blit(diff_text, (WINDOW_WIDTH//2 - 150, 410))
            self.difficulty_selector.draw()
            
            # Draw buttons
            self.start_button.draw()
            self.leaderboard_button.draw()
            
            pygame.display.update()
        
        # Default return if loop exits unexpectedly
        return (self.name_input or "Player", 
                self.difficulty_selector.get_selected_difficulty(),
                self.sprite_selector.get_selected_sprite())
    
    def show_leaderboard(self):
        try:
            with open("leaderboard.txt", "r") as file:
                leaderboard = {}
                for line in file:
                    name, score = line.strip().split(":")
                    leaderboard[name] = int(score)
        except FileNotFoundError:
            leaderboard = {}
        
        # Sort leaderboard by score (descending)
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
        
        viewing = True
        while viewing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    viewing = False
            
            self.screen.fill(BLACK)
            
            # Draw title
            title = self.font_large.render("Leaderboard", True, GOLD)
            self.screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 50))
            
            # Draw leaderboard entries
            y_pos = 150
            if not sorted_leaderboard:
                no_scores = self.font.render("No scores yet!", True, WHITE)
                self.screen.blit(no_scores, (WINDOW_WIDTH//2 - no_scores.get_width()//2, y_pos))
            else:
                for i, (name, score) in enumerate(sorted_leaderboard[:10]):  # Show top 10
                    rank = f"{i+1}. {name}: {score}"
                    color = GOLD if i == 0 else SILVER if i == 1 else BRONZE if i == 2 else WHITE
                    rank_text = self.font.render(rank, True, color)
                    self.screen.blit(rank_text, (WINDOW_WIDTH//2 - rank_text.get_width()//2, y_pos))
                    y_pos += 40
            
            # Draw back instruction
            back_text = self.font.render("Press any key to return", True, LIGHT_GREY)
            self.screen.blit(back_text, (WINDOW_WIDTH//2 - back_text.get_width()//2, WINDOW_HEIGHT - 100))
            
            pygame.display.update()

class GameUI:
    def __init__(self, screen, player_name, sprite_choice, screen_width, screen_height):
        self.screen = screen
        self.player_name = player_name
        self.sprite_choice = sprite_choice
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("CoolveticaRg-Regular", 36)
        self.font_small = pygame.font.SysFont("CoolveticaRg-Regular", 24)
        self.hover_col = 0
        
        # Map sprite choice to color
        if sprite_choice == "Red":
            self.player_color = RED
            self.ai_color = YELLOW
        elif sprite_choice == "Blue":
            self.player_color = BLUE
            self.ai_color = RED
        elif sprite_choice == "Green":
            self.player_color = GREEN
            self.ai_color = BLUE
        else:
            self.player_color = RED
            self.ai_color = YELLOW
    
    def get_offsets(self):
        """calculate offsets to center the game board."""
        x_offset = (self.screen_width - WINDOW_WIDTH) // 2
        y_offset = (self.screen_height - WINDOW_HEIGHT) // 2
        return x_offset, y_offset
    
    def draw_board(self, board):
        # Clear the screen and draw the board background
        self.screen.fill(BLACK)
        
        # Calculate centering offsets
        x_offset, y_offset = self.get_offsets()
        
        # Draw the header area
        pygame.draw.rect(self.screen, BLACK, (x_offset, y_offset, WINDOW_WIDTH, SQUARESIZE))
        
        # Draw the board slots
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                # Draw the blue grid
                pygame.draw.rect(self.screen, BLUE, 
                                (x_offset + c * SQUARESIZE, y_offset + r * SQUARESIZE + SQUARESIZE, 
                                 SQUARESIZE, SQUARESIZE))
                
                # Draw the empty slots
                pygame.draw.circle(self.screen, BLACK, 
                                  (x_offset + int(c * SQUARESIZE + SQUARESIZE/2), 
                                   y_offset + int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), 
                                  RADIUS)
        
        # Draw the pieces
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == PLAYER_PIECE:
                    pygame.draw.circle(self.screen, self.player_color, 
                                      (x_offset + int(c * SQUARESIZE + SQUARESIZE/2), 
                                       y_offset + int(WINDOW_HEIGHT - r * SQUARESIZE - SQUARESIZE/2)), 
                                      RADIUS)
                elif board[r][c] == AI_PIECE:
                    pygame.draw.circle(self.screen, self.ai_color, 
                                      (x_offset + int(c * SQUARESIZE + SQUARESIZE/2), 
                                       y_offset + int(WINDOW_HEIGHT - r * SQUARESIZE - SQUARESIZE/2)), 
                                      RADIUS)
        
        # Draw player info
        player_text = self.font_small.render(f"Player: {self.player_name}", True, self.player_color)
        self.screen.blit(player_text, (x_offset + 10, y_offset + 10))
    
    def update_hover(self, x_pos):
        # Calculate centering offsets
        x_offset, y_offset = self.get_offsets()
        
        # Adjust x_pos for offset
        adjusted_x_pos = x_pos - x_offset
        
        # Show piece hover effect
        pygame.draw.rect(self.screen, BLACK, (x_offset, y_offset, WINDOW_WIDTH, SQUARESIZE))
        
        # Draw player info and score again (since we cleared the top)
        player_text = self.font_small.render(f"Player: {self.player_name}", True, self.player_color)
        self.screen.blit(player_text, (x_offset + 10, y_offset + 10))
        
        # Calculate column from x position
        self.hover_col = min(max(adjusted_x_pos // SQUARESIZE, 0), COLUMN_COUNT - 1)
        
        # Draw hover piece
        pygame.draw.circle(self.screen, self.player_color, 
                          (x_offset + self.hover_col * SQUARESIZE + SQUARESIZE//2, 
                           y_offset + SQUARESIZE//2), 
                          RADIUS)
        
        pygame.display.update()
    
    def draw_score(self, score):
        # Calculate centering offsets
        x_offset, y_offset = self.get_offsets()
        
        score_text = self.font_small.render(f"Score: {score}", True, WHITE)
        self.screen.blit(score_text, (x_offset + WINDOW_WIDTH - score_text.get_width() - 10, y_offset + 10))
    
    def show_winner(self, winner):
        # Calculate centering offsets
        x_offset, y_offset = self.get_offsets()
        
        label_bg = pygame.Surface((400, 80))
        label_bg.set_alpha(200)  # Semi-transparent
        label_bg.fill(BLACK)
        
        if winner == "AI":
            label = self.font.render("AI wins!", True, self.ai_color)
        else:
            label = self.font.render(f"{winner} wins!", True, self.player_color)
        
        self.screen.blit(label_bg, (x_offset + WINDOW_WIDTH//2 - 200, y_offset + WINDOW_HEIGHT//2 - 40))
        self.screen.blit(label, (x_offset + WINDOW_WIDTH//2 - label.get_width()//2, 
                                y_offset + WINDOW_HEIGHT//2 - label.get_height()//2))
        pygame.display.update()