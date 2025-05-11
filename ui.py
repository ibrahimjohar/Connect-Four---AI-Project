import sys
import pygame
import time
import os
from utils import *

class LoadingScreen:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.font = pygame.font.SysFont("CoolveticaRg-Regular", 40)
        self.scale_factor = min(self.screen_width / WINDOW_WIDTH, self.screen_height / WINDOW_HEIGHT)
    
    def get_offsets(self):
        """Calculate offsets to center the content within the screen."""
        scaled_width = WINDOW_WIDTH * self.scale_factor
        scaled_height = WINDOW_HEIGHT * self.scale_factor
        x_offset = (self.screen_width - scaled_width) // 2
        y_offset = (self.screen_height - scaled_height) // 2
        return x_offset, y_offset
    
    def show(self):
        # Simple loading animation
        for i in range(101):
            self.screen.fill(BLACK)
            
            # Calculate offsets for centering
            x_offset, y_offset = self.get_offsets()
            
            # Draw title
            title = self.font.render("Connect 4", True, WHITE)
            title_pos = (x_offset + WINDOW_WIDTH * self.scale_factor//2 - title.get_width()//2,
                        y_offset + WINDOW_HEIGHT * self.scale_factor//4)
            self.screen.blit(title, title_pos)
            
            # Draw progress bar
            bar_width = WINDOW_WIDTH * self.scale_factor // 2
            bar_height = 30 * self.scale_factor
            bar_x = x_offset + WINDOW_WIDTH * self.scale_factor//4
            bar_y = y_offset + WINDOW_HEIGHT * self.scale_factor//2
            
            pygame.draw.rect(self.screen, WHITE, 
                            (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(self.screen, GREEN, 
                            (bar_x, bar_y, bar_width * (i/100), bar_height))
            
            # Draw loading text
            loading_text = self.font.render(f"Loading... {i}%", True, WHITE)
            text_pos = (x_offset + WINDOW_WIDTH * self.scale_factor//2 - loading_text.get_width()//2,
                       y_offset + WINDOW_HEIGHT * self.scale_factor//2 + bar_height + 20)
            self.screen.blit(loading_text, text_pos)
            
            pygame.display.update()
            time.sleep(0.01)  # Adjust for desired loading speed

class Button:
    def __init__(self, screen, text, x, y, width, height, color, hover_color):
        self.screen = screen
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont("CoolveticaRg-Regular", 24)
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
    
    def update_layout(self):
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.center_x = self.screen_width // 2
        self.selector_x = self.center_x - self.width // 2
    
    def draw(self):
        self.update_layout()
        y = self.y
        # Update button positions
        self.left_button.rect.x = self.selector_x
        self.left_button.rect.y = y
        self.right_button.rect.x = self.selector_x + self.width - 30
        self.right_button.rect.y = y
        # Draw selector box
        pygame.draw.rect(self.screen, WHITE, (self.selector_x + 40, y, self.width - 80, self.height), 2)
        # Draw sprite name
        text = self.font.render(self.sprites[self.current_sprite], True, WHITE)
        self.screen.blit(text, (self.center_x - text.get_width() // 2, y))
        # Draw sprite preview circle
        sprite_color = self.get_sprite_color()
        pygame.draw.circle(self.screen, sprite_color, (self.center_x, y + 60), 20)
        # Draw navigation buttons
        self.left_button.draw()
        self.right_button.draw()
    
    def get_sprite_color(self):
        if self.sprites[self.current_sprite] == "Red":
            return RED
        elif self.sprites[self.current_sprite] == "Blue":
            return LIGHT_BLUE
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
    
    def update_layout(self):
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.center_x = self.screen_width // 2
        self.x = self.center_x - self.width // 2
    
    def draw(self):
        self.update_layout()
        for i, button in enumerate(self.buttons):
            button.rect.x = self.x + i * (self.width // 3)
            button.rect.y = self.y
            # Make selected button stand out
            if i == self.selected:
                pygame.draw.rect(self.screen, WHITE, (button.rect.x - 2, button.rect.y - 2, button.rect.width + 4, button.rect.height + 4), 2)
            button.draw()
    
    def handle_event(self, event, mouse_pos):
        for i, button in enumerate(self.buttons):
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, event):
                self.selected = i
    
    def get_selected_difficulty(self):
        return self.difficulties[self.selected]

class GameMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scale_factor = min(screen_width / WINDOW_WIDTH, screen_height / WINDOW_HEIGHT)
        self.font_large = pygame.font.SysFont("CoolveticaRg-Regular", int(48 * self.scale_factor))
        self.font = pygame.font.SysFont("CoolveticaRg-Regular", int(32 * self.scale_factor))
        self.name_input = ""
        self.active = True
        self.update_layout()

    def update_layout(self):
        self.scale_factor = min(self.screen_width / WINDOW_WIDTH, self.screen_height / WINDOW_HEIGHT)
        self.font_large = pygame.font.SysFont("CoolveticaRg-Regular", int(48 * self.scale_factor))
        self.font = pygame.font.SysFont("CoolveticaRg-Regular", int(32 * self.scale_factor))

    def handle_resize(self, new_width, new_height):
        self.screen_width = new_width
        self.screen_height = new_height
        self.update_layout()

    def show(self):
        # 1. Title screen
        self.show_title_screen()
        # 2. Name input
        player_name = self.show_name_input()
        # 3. Piece selection
        sprite = self.show_piece_selection()
        # 4. Difficulty selection
        difficulty = self.show_difficulty_selection()
        return (player_name, difficulty, sprite)

    def show_title_screen(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.handle_resize(event.w, event.h)
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
            self.screen.fill(BLACK)
            center_x = self.screen_width / 2
            center_y = self.screen_height / 2
            title = self.font_large.render("Connect 4", True, BLUE)
            self.screen.blit(title, (center_x - title.get_width() / 2, center_y - title.get_height() / 2))
            pygame.display.update()

    def show_name_input(self):
        name_input = ""
        active_input = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.handle_resize(event.w, event.h)
                if active_input and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name_input.strip():
                        return name_input
                    elif event.key == pygame.K_BACKSPACE:
                        name_input = name_input[:-1]
                    elif len(name_input) < 20:
                        name_input += event.unicode
            self.screen.fill(BLACK)
            center_x = self.screen_width / 2
            center_y = self.screen_height / 2
            prompt = self.font.render("Enter your name:", True, WHITE)
            self.screen.blit(prompt, (center_x - prompt.get_width() / 2, center_y - 80 * self.scale_factor))
            input_rect = pygame.Rect(center_x - 150 * self.scale_factor, center_y - 20 * self.scale_factor, 300 * self.scale_factor, 40 * self.scale_factor)
            pygame.draw.rect(self.screen, WHITE if active_input else LIGHT_GREY, input_rect)
            pygame.draw.rect(self.screen, BLACK, input_rect, 2)
            name_surface = self.font.render(name_input, True, BLACK)
            self.screen.blit(name_surface, (center_x - 145 * self.scale_factor, center_y - 15 * self.scale_factor))
            if active_input and pygame.time.get_ticks() % 1000 < 500:
                cursor_pos = self.font.size(name_input)[0]
                pygame.draw.line(self.screen, BLACK, (center_x - 145 * self.scale_factor + cursor_pos, center_y - 15 * self.scale_factor), (center_x - 145 * self.scale_factor + cursor_pos, center_y - 15 * self.scale_factor + 30 * self.scale_factor), 2)
            pygame.display.update()

    def show_piece_selection(self):
        sprite_selector = SpriteSelector(self.screen, 0, 0)
        center_x = self.screen_width / 2
        center_y = self.screen_height / 2
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.handle_resize(event.w, event.h)
                    center_x = self.screen_width / 2
                    center_y = self.screen_height / 2
                    sprite_selector.update_layout()
                sprite_selector.handle_event(event, mouse_pos)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return sprite_selector.get_selected_sprite()
                if event.type == pygame.MOUSEBUTTONDOWN and sprite_selector.left_button.is_hovered or sprite_selector.right_button.is_hovered:
                    continue
            self.screen.fill(BLACK)
            prompt = self.font.render("Choose your piece:", True, WHITE)
            self.screen.blit(prompt, (center_x - prompt.get_width() / 2, center_y - 80 * self.scale_factor))
            # Center the sprite selector
            sprite_selector.y = center_y - 20
            sprite_selector.draw()
            confirm_text = self.font.render("Press Enter to confirm", True, LIGHT_GREY)
            self.screen.blit(confirm_text, (center_x - confirm_text.get_width() / 2, center_y + 80 * self.scale_factor))
            pygame.display.update()

    def show_difficulty_selection(self):
        difficulty_selector = DifficultySelector(self.screen, 0, 0)
        center_x = self.screen_width / 2
        center_y = self.screen_height / 2
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.handle_resize(event.w, event.h)
                    center_x = self.screen_width / 2
                    center_y = self.screen_height / 2
                    difficulty_selector.update_layout()
                difficulty_selector.handle_event(event, mouse_pos)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and difficulty_selector.selected is not None:
                    return difficulty_selector.get_selected_difficulty()
            self.screen.fill(BLACK)
            prompt = self.font.render("Select difficulty:", True, WHITE)
            self.screen.blit(prompt, (center_x - prompt.get_width() / 2, center_y - 80 * self.scale_factor))
            # Center the difficulty selector
            difficulty_selector.y = center_y - 20
            difficulty_selector.draw()
            confirm_text = self.font.render("Press Enter to confirm", True, LIGHT_GREY)
            self.screen.blit(confirm_text, (center_x - confirm_text.get_width() / 2, center_y + 80 * self.scale_factor))
            pygame.display.update()

    def show_leaderboard(self):
        try:
            with open("leaderboard.txt", "r") as file:
                leaderboard = {}
                for line in file:
                    name, score = line.strip().split(":")
                    leaderboard[name] = int(score)
        except FileNotFoundError:
            leaderboard = {}
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
        pygame.event.clear()  # Clear stale events before showing leaderboard
        viewing = True
        scale_factor = min(self.screen_width / WINDOW_WIDTH, self.screen_height / WINDOW_HEIGHT)
        font_large = pygame.font.SysFont("CoolveticaRg-Regular", int(48 * scale_factor))
        font = pygame.font.SysFont("CoolveticaRg-Regular", int(32 * scale_factor))
        center_x = self.screen_width / 2
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
                    font_large = pygame.font.SysFont("CoolveticaRg-Regular", int(48 * scale_factor))
                    font = pygame.font.SysFont("CoolveticaRg-Regular", int(32 * scale_factor))
                    center_x = self.screen_width / 2
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    viewing = False
            self.screen.fill(BLACK)
            # Title
            title = font_large.render("Leaderboard", True, GOLD)
            self.screen.blit(title, (center_x - title.get_width() / 2, 80 * scale_factor))
            # Entries
            y_start = 180 * scale_factor
            line_height = 40 * scale_factor
            if not sorted_leaderboard:
                no_scores = font.render("No scores yet!", True, WHITE)
                self.screen.blit(no_scores, (center_x - no_scores.get_width() / 2, y_start))
            else:
                for i, (name, score) in enumerate(sorted_leaderboard[:10]):
                    rank = f"{i+1}. {name}: {score}"
                    color = GOLD if i == 0 else SILVER if i == 1 else BRONZE if i == 2 else WHITE
                    rank_text = font.render(rank, True, color)
                    self.screen.blit(rank_text, (center_x - rank_text.get_width() / 2, y_start + i * line_height))
            # Back instruction
            back_text = font.render("Press any key to return", True, LIGHT_GREY)
            self.screen.blit(back_text, (center_x - back_text.get_width() / 2, self.screen_height - 100 * scale_factor))
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
        
        # Calculate scale factor for fullscreen
        self.scale_factor = min(screen_width / WINDOW_WIDTH, screen_height / WINDOW_HEIGHT)
        self.square_size = int(SQUARESIZE * self.scale_factor)
        self.radius = int(RADIUS * self.scale_factor)
        
        # Map sprite choice to color
        if sprite_choice == "Red":
            self.player_color = RED
            self.ai_color = YELLOW
        elif sprite_choice == "Blue":
            self.player_color = LIGHT_BLUE
            self.ai_color = RED
        elif sprite_choice == "Green":
            self.player_color = GREEN
            self.ai_color = LIGHT_BLUE
        else:
            self.player_color = RED
            self.ai_color = YELLOW
    
    def update_layout(self):
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.scale_factor = min(self.screen_width / WINDOW_WIDTH, self.screen_height / WINDOW_HEIGHT)
        self.square_size = int(SQUARESIZE * self.scale_factor)
        self.radius = int(RADIUS * self.scale_factor)
    
    def get_offsets(self):
        self.update_layout()
        scaled_width = WINDOW_WIDTH * self.scale_factor
        scaled_height = WINDOW_HEIGHT * self.scale_factor
        x_offset = (self.screen_width - scaled_width) // 2
        y_offset = (self.screen_height - scaled_height) // 2
        return x_offset, y_offset
    
    def draw_board(self, board):
        # Clear the screen and draw the board background
        self.screen.fill(BLACK)
        
        # Calculate centering offsets
        x_offset, y_offset = self.get_offsets()
        
        # Draw the header area
        pygame.draw.rect(self.screen, BLACK, (x_offset, y_offset, WINDOW_WIDTH * self.scale_factor, self.square_size))
        
        # Draw the board slots
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                # Draw the blue grid
                pygame.draw.rect(self.screen, BLUE, 
                                (x_offset + c * self.square_size, 
                                 y_offset + r * self.square_size + self.square_size, 
                                 self.square_size, self.square_size))
                
                # Draw the empty slots
                pygame.draw.circle(self.screen, BLACK, 
                                  (x_offset + int(c * self.square_size + self.square_size/2), 
                                   y_offset + int(r * self.square_size + self.square_size + self.square_size/2)), 
                                  self.radius)
        
        # Draw the pieces
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == PLAYER_PIECE:
                    pygame.draw.circle(self.screen, self.player_color, 
                                      (x_offset + int(c * self.square_size + self.square_size/2), 
                                       y_offset + int(WINDOW_HEIGHT * self.scale_factor - r * self.square_size - self.square_size/2)), 
                                      self.radius)
                elif board[r][c] == AI_PIECE:
                    pygame.draw.circle(self.screen, self.ai_color, 
                                      (x_offset + int(c * self.square_size + self.square_size/2), 
                                       y_offset + int(WINDOW_HEIGHT * self.scale_factor - r * self.square_size - self.square_size/2)), 
                                      self.radius)
        
        # Draw player info
        player_text = self.font_small.render(f"Player: {self.player_name}", True, self.player_color)
        self.screen.blit(player_text, (x_offset + 10, y_offset + 10))
    
    def update_hover(self, x_pos):
        # Calculate centering offsets
        x_offset, y_offset = self.get_offsets()
        
        # Adjust x_pos for offset
        adjusted_x_pos = x_pos - x_offset
        
        # Show piece hover effect
        pygame.draw.rect(self.screen, BLACK, (x_offset, y_offset, WINDOW_WIDTH * self.scale_factor, self.square_size))
        
        # Draw player info and score again (since we cleared the top)
        player_text = self.font_small.render(f"Player: {self.player_name}", True, self.player_color)
        self.screen.blit(player_text, (x_offset + 10, y_offset + 10))
        
        # Calculate column from x position
        self.hover_col = min(max(int(adjusted_x_pos // self.square_size), 0), COLUMN_COUNT - 1)
        
        # Draw hover piece
        pygame.draw.circle(self.screen, self.player_color, 
                          (x_offset + self.hover_col * self.square_size + self.square_size//2, 
                           y_offset + self.square_size//2), 
                          self.radius)
        
        pygame.display.update()
    
    def draw_score(self, score):
        # Calculate centering offsets
        x_offset, y_offset = self.get_offsets()
        
        score_text = self.font_small.render(f"Score: {score}", True, WHITE)
        self.screen.blit(score_text, (x_offset + WINDOW_WIDTH * self.scale_factor - score_text.get_width() - 10, y_offset + 10))
    
    def show_winner(self, winner):
        # Calculate centering offsets
        x_offset, y_offset = self.get_offsets()
        
        label_bg = pygame.Surface((400 * self.scale_factor, 80 * self.scale_factor))
        label_bg.set_alpha(200)  # Semi-transparent
        label_bg.fill(BLACK)
        
        if winner == "AI":
            label = self.font.render("AI wins!", True, self.ai_color)
        elif winner == "Draw":
            label = self.font.render("Game is a Draw!", True, WHITE)
        else:
            label = self.font.render(f"{winner} wins!", True, self.player_color)
        
        self.screen.blit(label_bg, (x_offset + WINDOW_WIDTH * self.scale_factor//2 - 200 * self.scale_factor, 
                                   y_offset + WINDOW_HEIGHT * self.scale_factor//2 - 40 * self.scale_factor))
        self.screen.blit(label, (x_offset + WINDOW_WIDTH * self.scale_factor//2 - label.get_width()//2, 
                                y_offset + WINDOW_HEIGHT * self.scale_factor//2 - label.get_height()//2))
        pygame.display.update()