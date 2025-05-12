import sys
import pygame
import time
import os
from utils import *
import pygame.gfxdraw

# Replace all font loading to use Boxing-Regular.otf
BOXING_FONT_PATH = os.path.join("fonts", "Boxing-Regular.otf")

# At the top, define the TITLE_YELLOW color for reuse
TITLE_YELLOW = (255, 255, 227)

class LoadingScreen:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.font = pygame.font.Font(BOXING_FONT_PATH, 40)
        self.scale_factor = min(self.screen_width / WINDOW_WIDTH, self.screen_height / WINDOW_HEIGHT)
    
    def get_offsets(self):
        """Calculate offsets to center the content within the screen."""
        scaled_width = WINDOW_WIDTH * self.scale_factor
        scaled_height = WINDOW_HEIGHT * self.scale_factor
        x_offset = (self.screen_width - scaled_width) // 2
        y_offset = (self.screen_height - scaled_height) // 2
        return x_offset, y_offset
    
    def show(self):
        for i in range(101):
            self.screen.fill(BLACK)
            x_offset, y_offset = self.get_offsets()
            # Remove title text from loading bar
            # Draw progress bar
            bar_width = WINDOW_WIDTH * self.scale_factor // 2
            bar_height = 30 * self.scale_factor
            bar_x = x_offset + WINDOW_WIDTH * self.scale_factor//4
            bar_y = y_offset + WINDOW_HEIGHT * self.scale_factor//2
            # Draw loading bar background in light yellow
            pygame.draw.rect(self.screen, TITLE_YELLOW, (bar_x, bar_y, bar_width, bar_height))
            # Draw loading bar progress in a slightly more saturated yellow
            pygame.draw.rect(self.screen, (255, 255, 180), (bar_x, bar_y, bar_width * (i/100), bar_height))
            # Draw loading text in light yellow
            loading_text = self.font.render(f"Loading... {i}%", True, TITLE_YELLOW)
            text_pos = (x_offset + WINDOW_WIDTH * self.scale_factor//2 - loading_text.get_width()//2,
                       bar_y + bar_height + 20)
            self.screen.blit(loading_text, text_pos)
            pygame.display.update()
            time.sleep(0.01)

class Button:
    def __init__(self, screen, text, x, y, width, height, color, hover_color, text_color=BLACK, hover_text_color=WHITE, border_color=BLACK, hover_border_color=BLACK):
        self.screen = screen
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hover_text_color = hover_text_color
        self.border_color = border_color
        self.hover_border_color = hover_border_color
        self.font = pygame.font.Font(BOXING_FONT_PATH, 24)
        self.is_hovered = False
    
    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        text_color = self.hover_text_color if self.is_hovered else self.text_color
        border_color = self.hover_border_color if self.is_hovered else self.border_color
        pygame.draw.rect(self.screen, color, self.rect)
        pygame.draw.rect(self.screen, border_color, self.rect, 2)
        text_surf = self.font.render(self.text, True, text_color)
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
        self.width = 400
        self.height = 150
        self.font = pygame.font.Font(BOXING_FONT_PATH, 28)
        self.sprites = ["Red", "Blue", "Green"]
        self.current_sprite = 0
        self.left_button_rect = pygame.Rect(0, 0, 40, 40)
        self.right_button_rect = pygame.Rect(0, 0, 40, 40)
    
    def update_layout(self):
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.center_x = self.screen_width // 2
        self.selector_x = self.center_x - self.width // 2
    
    def draw(self):
        # Center horizontally
        screen_width = self.screen.get_width()
        center_x = screen_width // 2
        selector_width = self.width
        selector_x = center_x - selector_width // 2
        y = self.y
        # Draw selector box
        box_rect = pygame.Rect(selector_x + 40, y, self.width - 80, self.height)
        pygame.draw.rect(self.screen, WHITE, box_rect, 2)
        # Draw sprite name
        text = self.font.render(self.sprites[self.current_sprite], True, WHITE)
        self.screen.blit(text, (center_x - text.get_width() // 2, y + 10))
        # Supersample the sprite preview circle
        supersample = 4
        preview_size = 80  # diameter of preview area
        surf_size = preview_size * supersample
        preview_surface = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
        sprite_color = self.get_sprite_color()
        # Draw filled and antialiased circle to preview_surface
        cx = surf_size // 2
        cy = surf_size // 2
        radius = 32 * supersample
        pygame.gfxdraw.filled_circle(preview_surface, int(cx), int(cy), int(radius), sprite_color)
        pygame.gfxdraw.aacircle(preview_surface, int(cx), int(cy), int(radius), sprite_color)
        # Downscale and blit to screen
        small_preview = pygame.transform.smoothscale(preview_surface, (preview_size, preview_size))
        piece_center_y = int(box_rect.centery + 20)
        self.screen.blit(small_preview, (center_x - preview_size // 2, piece_center_y - preview_size // 2))
        # Draw navigation arrows (no bg, just white text, vertically aligned with the box)
        arrow_font = pygame.font.Font(BOXING_FONT_PATH, 48)
        left_arrow = arrow_font.render("<", True, WHITE)
        right_arrow = arrow_font.render(">", True, WHITE)
        # Align arrows with the vertical center of the box
        arrow_gap = 24
        arrow_y = box_rect.centery - left_arrow.get_height() // 2
        left_x = box_rect.left - arrow_gap - left_arrow.get_width()
        right_x = box_rect.right + arrow_gap
        self.left_button_rect.x = left_x
        self.left_button_rect.y = arrow_y
        self.right_button_rect.x = right_x
        self.right_button_rect.y = arrow_y
        self.screen.blit(left_arrow, (left_x, arrow_y))
        self.screen.blit(right_arrow, (right_x, arrow_y))
    
    def get_sprite_color(self):
        if self.sprites[self.current_sprite] == "Red":
            return RED
        elif self.sprites[self.current_sprite] == "Blue":
            return LIGHT_BLUE
        elif self.sprites[self.current_sprite] == "Green":
            return GREEN
        return RED
    
    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.left_button_rect.collidepoint(mouse_pos):
                self.current_sprite = (self.current_sprite - 1) % len(self.sprites)
            elif self.right_button_rect.collidepoint(mouse_pos):
                self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
    
    def get_selected_sprite(self):
        return self.sprites[self.current_sprite]

class DifficultySelector:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 300
        self.height = 40
        self.font = pygame.font.Font(BOXING_FONT_PATH, 24)
        self.difficulties = ["easy", "medium", "hard", "ai_vs_ai", "user_vs_user"]
        self.buttons = []
        
        button_width = self.width // 3
        for i, diff in enumerate(self.difficulties):
            # All yellow/black scheme
            color = (255, 230, 80)
            hover_color = (255, 255, 180)
            if diff == "easy":
                label = "User vs AI (Easy)"
            elif diff == "medium":
                label = "User vs AI (Medium)"
            elif diff == "hard":
                label = "User vs AI (Hard)"
            elif diff == "ai_vs_ai":
                label = "AI vs AI"
            elif diff == "user_vs_user":
                label = "User vs User"
            else:
                label = diff.capitalize()
            self.buttons.append(Button(screen, label, x + i * button_width, y, button_width, self.height, color, hover_color, BLACK, BLACK, BLACK))
        
        self.selected = None  # Default to easy
    
    def update_layout(self):
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.center_x = self.screen_width / 2
        # Responsive button size
        self.width = int(self.screen_width * 0.22)
        self.height = int(self.screen_height * 0.07)
        self.x = self.center_x - self.width / 2
    
    def draw(self, y_start):
        self.update_layout()
        button_height = self.height
        spacing = int(self.screen_height * 0.03)
        y = y_start
        for i, button in enumerate(self.buttons):
            button.rect.width = self.width
            button.rect.height = button_height
            button.rect.x = self.center_x - button.rect.width / 2
            button.rect.y = y
            if i == self.selected:
                pygame.draw.rect(self.screen, BLACK, (button.rect.x - 2, button.rect.y - 2, button.rect.width + 4, button.rect.height + 4), 2)
            button.draw()
            y += button_height + spacing
    
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
        self.font_large = pygame.font.Font(BOXING_FONT_PATH, int(80 * self.scale_factor))
        self.font = pygame.font.Font(BOXING_FONT_PATH, int(32 * self.scale_factor))
        self.name_input = ""
        self.active = True
        self.bg_title1 = pygame.image.load(os.path.join("imgs", "bg1.jpg")).convert()
        self.bg_other = pygame.image.load(os.path.join("imgs", "bg2.jpg")).convert()
        self.bg_scroll_x = 0
        self.bg_scroll_speed = 0.46  # increased speed for smoother/faster scroll
        self.update_layout()

    def update_layout(self):
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.scale_factor = min(self.screen_width / WINDOW_WIDTH, self.screen_height / WINDOW_HEIGHT)
        self.font_large = pygame.font.Font(BOXING_FONT_PATH, int(80 * self.scale_factor))
        self.font = pygame.font.Font(BOXING_FONT_PATH, int(32 * self.scale_factor))

    def handle_resize(self, new_width, new_height):
        self.screen_width = new_width
        self.screen_height = new_height
        self.update_layout()

    def blit_centered_bg(self, img, screen, scroll_x=None):
        # For title page, use robust seamless alternating tiling of bg1 and its horizontal flip
        if hasattr(self, 'bg_title1') and img == self.bg_title1:
            if scroll_x is None:
                scroll_x = self.bg_scroll_x
            img_w, img_h = self.bg_title1.get_size()
            win_w, win_h = screen.get_size()
            scale = max(win_w / img_w, win_h / img_h)
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)
            bg1_scaled = pygame.transform.smoothscale(self.bg_title1, (new_w, new_h))
            bg1_flipped = pygame.transform.flip(bg1_scaled, True, False)
            y = (win_h - new_h) // 2
            screen.fill((0, 0, 0))
            num_tiles = (win_w // new_w) + 3
            scroll_x = scroll_x % (2 * new_w)
            for i in range(-1, num_tiles):
                img_to_blit = bg1_scaled if (i % 2 == 0) else bg1_flipped
                x = -scroll_x + i * new_w
                screen.blit(img_to_blit, (x, y))
        else:
            img_w, img_h = img.get_size()
            win_w, win_h = screen.get_size()
            scale = max(win_w / img_w, win_h / img_h)
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)
            bg_scaled = pygame.transform.smoothscale(img, (new_w, new_h))
            x = (win_w - new_w) // 2
            y = (win_h - new_h) // 2
            screen.fill((0, 0, 0))
            screen.blit(bg_scaled, (x, y))

    def fade_in_background(self, duration=1000):
        # Fade in the background from black to full opacity
        clock = pygame.time.Clock()
        steps = 30
        for alpha in range(0, 256, max(1, int(255/steps))):
            temp_surface = pygame.Surface(self.screen.get_size()).convert_alpha()
            # Always use scroll_x=0 during fade-in to avoid glitches
            self.blit_centered_bg(self.bg_title1, temp_surface, scroll_x=0)
            temp_surface.set_alpha(alpha)
            self.screen.fill((0,0,0))
            self.screen.blit(temp_surface, (0,0))
            pygame.display.update()
            clock.tick(60)

    def typewriter_text(self, text, font, color, pos, subtitle=None, subtitle_font=None, subtitle_pos=None, delay=110):
        for i in range(len(text)):
            self.blit_centered_bg(self.bg_title1, self.screen)
            # Draw the growing title
            title_surface = font.render(text[:i+1], True, color)
            self.screen.blit(title_surface, pos)
            # Draw subtitle if provided
            if subtitle and subtitle_font and subtitle_pos:
                subtitle_surface = subtitle_font.render(subtitle, True, WHITE)
                self.screen.blit(subtitle_surface, subtitle_pos)
            pygame.display.update()
            pygame.time.wait(delay)

    def fade_in_surface(self, surface, pos, bg_img, duration=600):
        # Fade in a surface by increasing its alpha
        clock = pygame.time.Clock()
        steps = 30
        for alpha in range(0, 256, int(255/steps)):
            self.blit_centered_bg(bg_img, self.screen)
            # Draw the full title (already typed)
            center_x = self.screen_width / 2
            center_y = self.screen_height / 2
            title = "connect 4our"
            title_surface = self.font_large.render(title, True, TITLE_YELLOW)
            title_pos = (center_x - title_surface.get_width() / 2, center_y - title_surface.get_height() / 2)
            # Draw previous faded-in elements
            for s, p, a in getattr(self, '_fadein_prev', []):
                s.set_alpha(255)
                self.screen.blit(s, p)
            # Draw the current surface with alpha
            surface.set_alpha(alpha)
            self.screen.blit(surface, pos)
            pygame.display.update()
            clock.tick(60)
        # Store this as faded in
        if not hasattr(self, '_fadein_prev'):
            self._fadein_prev = []
        self._fadein_prev.append((surface.copy(), pos, 255))

    def show_title_screen(self):
        # 1. Fade in the background
        self.fade_in_background(duration=1000)
        # 2. Start background scrolling and typewriter effect together
        center_x = self.screen_width / 2
        center_y = self.screen_height / 2
        title = "connect 4our"
        title_font = self.font_large
        title_color = TITLE_YELLOW
        title_surface = title_font.render(title, True, title_color)
        title_pos = (center_x - title_surface.get_width() / 2, center_y - title_surface.get_height() / 2)
        # Subtitle
        subtitle_font = pygame.font.Font(BOXING_FONT_PATH, int(self.font_large.get_height() * 0.20))
        subtitle_text = "powered by minimax alpha-beta pruning AI algorithm."
        subtitle_surface = subtitle_font.render(subtitle_text, True, WHITE)
        subtitle_y = center_y + title_surface.get_height() / 2 + 10
        subtitle_pos = (center_x - subtitle_surface.get_width() / 2, subtitle_y)
        # Click prompt
        click_font = pygame.font.Font(BOXING_FONT_PATH, int(self.font_large.get_height() * 0.18))
        click_text = "click anywhere to start"
        click_surface = click_font.render(click_text, True, WHITE)
        click_y = subtitle_y + subtitle_surface.get_height() + 80
        click_pos = (center_x - click_surface.get_width() / 2, click_y)
        # Credits
        credits_font = pygame.font.Font(BOXING_FONT_PATH, int(self.font_large.get_height() * 0.15))
        credits_text = "developed by: ibrahim - areeba - emman - amna"
        credits_surface = credits_font.render(credits_text, True, WHITE)
        credits_y = self.screen_height - credits_surface.get_height() - 30
        credits_pos = (center_x - credits_surface.get_width() / 2, credits_y)
        # 3. Animate background scroll and typewriter effect for title
        self._fadein_prev = []
        scroll_x = 0  # Start at 0, first frame after fade-in
        scroll_speed = self.bg_scroll_speed
        typewriter_done = False
        title_chars = ""
        typewriter_index = 0
        typewriter_delay = 110  # ms per char
        last_type_time = pygame.time.get_ticks()
        running = True
        clock = pygame.time.Clock()
        while running:
            now = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.handle_resize(event.w, event.h)
            # Animate background scroll
            scroll_x += scroll_speed
            self.blit_centered_bg(self.bg_title1, self.screen, scroll_x=scroll_x)
            # Animate typewriter
            if not typewriter_done and now - last_type_time > typewriter_delay:
                typewriter_index += 1
                last_type_time = now
                if typewriter_index >= len(title):
                    typewriter_done = True
            if not typewriter_done:
                title_chars = title[:typewriter_index]
                title_surface_partial = title_font.render(title_chars, True, title_color)
                self.screen.blit(title_surface_partial, title_pos)
            else:
                self.screen.blit(title_surface, title_pos)
            pygame.display.update()
            clock.tick(60)
            if typewriter_done:
                break
        # 4. Fade in subtitle, prompt, and credits one after another
        self._fadein_prev = []
        self.fade_in_surface(subtitle_surface, subtitle_pos, self.bg_title1)
        self.fade_in_surface(click_surface, click_pos, self.bg_title1)
        self.fade_in_surface(credits_surface, credits_pos, self.bg_title1)
        # 5. After all fades, keep animating background and wait for input
        waiting = True
        scroll_x = 0
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.handle_resize(event.w, event.h)
                if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                    waiting = False
            scroll_x += scroll_speed
            self.blit_centered_bg(self.bg_title1, self.screen, scroll_x=scroll_x)
            self.screen.blit(title_surface, title_pos)
            self.screen.blit(subtitle_surface, subtitle_pos)
            self.screen.blit(click_surface, click_pos)
            self.screen.blit(credits_surface, credits_pos)
            pygame.display.update()
            clock.tick(60)

    def show_name_input(self):
        name_input = ""
        active_input = True
        while True:
            center_x = self.screen_width / 2
            center_y = self.screen_height / 2
            button_width = 80 * self.scale_factor
            button_height = 32 * self.scale_factor
            spacing = 20 * self.scale_factor
            back_button = Button(self.screen, "Back", center_x - button_width - spacing/2, center_y + 60 * self.scale_factor, button_width, button_height, BLACK, WHITE, WHITE, BLACK, WHITE, BLACK)
            # Next button: yellow/black with black border
            next_button = Button(self.screen, "Next", center_x + spacing/2, center_y + 60 * self.scale_factor, button_width, button_height, (255, 230, 80), (255, 255, 180), BLACK, BLACK, BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.handle_resize(event.w, event.h)
                if back_button.is_clicked(pygame.mouse.get_pos(), event):
                    return True, False  # Go back
                if next_button.is_clicked(pygame.mouse.get_pos(), event) and name_input.strip():
                    self.name_input = name_input
                    return False, True
                if active_input and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name_input.strip():
                        self.name_input = name_input
                        return False, True
                    elif event.key == pygame.K_BACKSPACE:
                        name_input = name_input[:-1]
                    else:
                        # Restrict input so text fits in box
                        input_font = pygame.font.Font(BOXING_FONT_PATH, int(28 * self.scale_factor))
                        test_surface = input_font.render(name_input + event.unicode, True, BLACK)
                        if test_surface.get_width() < 300 * self.scale_factor - 10 and len(name_input) < 20:
                            name_input += event.unicode
            # Draw background image (other) with aspect ratio preserved
            self.blit_centered_bg(self.bg_other, self.screen)
            back_button.check_hover(pygame.mouse.get_pos())
            next_button.check_hover(pygame.mouse.get_pos())
            prompt = self.font.render("enter your name:", True, WHITE)
            self.screen.blit(prompt, (center_x - prompt.get_width() / 2, center_y - 80 * self.scale_factor))
            input_rect = pygame.Rect(center_x - 150 * self.scale_factor, center_y - 20 * self.scale_factor, 300 * self.scale_factor, 40 * self.scale_factor)
            pygame.draw.rect(self.screen, WHITE if active_input else LIGHT_GREY, input_rect)
            pygame.draw.rect(self.screen, BLACK, input_rect, 2)
            # Smaller font for input
            input_font = pygame.font.Font(BOXING_FONT_PATH, int(28 * self.scale_factor))
            name_surface = input_font.render(name_input, True, BLACK)
            self.screen.blit(name_surface, (center_x - 145 * self.scale_factor, center_y - 15 * self.scale_factor))
            if active_input and pygame.time.get_ticks() % 1000 < 500:
                cursor_pos = input_font.size(name_input)[0]
                pygame.draw.line(self.screen, BLACK, (center_x - 145 * self.scale_factor + cursor_pos, center_y - 15 * self.scale_factor), (center_x - 145 * self.scale_factor + cursor_pos, center_y - 15 * self.scale_factor + 30 * self.scale_factor), 2)
            back_button.draw()
            # Next button is only enabled if name is not empty
            if name_input.strip():
                next_button.draw()
            else:
                # Draw disabled next button (grey bg, grey text)
                pygame.draw.rect(self.screen, (180, 180, 180), next_button.rect)
                pygame.draw.rect(self.screen, BLACK, next_button.rect, 2)
                text_surf = next_button.font.render(next_button.text, True, (100, 100, 100))
                text_rect = text_surf.get_rect(center=next_button.rect.center)
                self.screen.blit(text_surf, text_rect)
            pygame.display.update()

    def show_piece_selection(self):
        sprite_selector = SpriteSelector(self.screen, 0, 0)
        center_x = self.screen_width / 2
        center_y = self.screen_height / 2
        button_width = 80 * self.scale_factor
        button_height = 32 * self.scale_factor
        spacing = 20 * self.scale_factor
        back_button = Button(self.screen, "Back", center_x - button_width - spacing/2, center_y + 100 * self.scale_factor, button_width, button_height, BLACK, WHITE, WHITE, BLACK, WHITE, BLACK)
        # Next button: yellow/black with black border
        next_button = Button(self.screen, "Next", center_x + spacing/2, center_y + 100 * self.scale_factor, button_width, button_height, (255, 230, 80), (255, 255, 180), BLACK, BLACK, BLACK)
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
                if back_button.is_clicked(mouse_pos, event):
                    return None, True, False  # Go back
                if next_button.is_clicked(mouse_pos, event):
                    return sprite_selector.get_selected_sprite(), False, True
                sprite_selector.handle_event(event, mouse_pos)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return sprite_selector.get_selected_sprite(), False, True
                if event.type == pygame.MOUSEBUTTONDOWN and sprite_selector.left_button_rect.collidepoint(mouse_pos) or sprite_selector.right_button_rect.collidepoint(mouse_pos):
                    continue
            # Draw background image (other) with aspect ratio preserved
            self.blit_centered_bg(self.bg_other, self.screen)
            # Calculate vertical layout
            prompt_font = self.font
            prompt = prompt_font.render("choose your piece:", True, WHITE)
            selector_box_height = sprite_selector.height
            confirm_font = pygame.font.Font(BOXING_FONT_PATH, int(18 * self.scale_factor))
            confirm_text = confirm_font.render("press enter to confirm", True, LIGHT_GREY)
            total_height = (prompt.get_height() + 20 + selector_box_height + 40 + button_height + 20 + confirm_text.get_height())
            start_y = (self.screen_height - total_height) / 2
            # Draw prompt
            self.screen.blit(prompt, (center_x - prompt.get_width() / 2, start_y))
            # Draw selector box and piece
            sprite_selector.y = start_y + prompt.get_height() + 20
            sprite_selector.draw()
            # Draw nav buttons
            nav_y = sprite_selector.y + selector_box_height + 40
            back_button.rect.y = nav_y
            next_button.rect.y = nav_y
            back_button.draw()
            if next_button.is_hovered or sprite_selector.get_selected_sprite():
                next_button.draw()
            else:
                pygame.draw.rect(self.screen, (180, 180, 180), next_button.rect)
                pygame.draw.rect(self.screen, BLACK, next_button.rect, 2)
                text_surf = next_button.font.render(next_button.text, True, (100, 100, 100))
                text_rect = text_surf.get_rect(center=next_button.rect.center)
                self.screen.blit(text_surf, text_rect)
            # Draw confirm text
            confirm_y = nav_y + button_height + 20
            self.screen.blit(confirm_text, (center_x - confirm_text.get_width() / 2, confirm_y))
            pygame.display.update()

    def show_difficulty_selection(self):
        difficulty_selector = DifficultySelector(self.screen, 0, 0)
        while True:
            # Draw background image (other) with aspect ratio preserved
            self.blit_centered_bg(self.bg_other, self.screen)
            center_x = self.screen_width / 2
            center_y = self.screen_height / 2
            scale_factor = self.scale_factor
            # Responsive sizes
            button_width = int(self.screen_width * 0.22)
            button_height = int(self.screen_height * 0.07)
            spacing = int(self.screen_height * 0.03)
            nav_spacing = int(self.screen_height * 0.04)
            nav_button_height = int(self.screen_height * 0.06)
            nav_button_width = int(self.screen_width * 0.13)
            # Prompt text
            prompt = self.font.render("select game mode", True, WHITE)
            prompt_height = prompt.get_height()
            # Confirm text
            confirm_font = pygame.font.Font(BOXING_FONT_PATH, int(18 * self.scale_factor))
            confirm_text = confirm_font.render("press enter to confirm", True, LIGHT_GREY)
            confirm_height = confirm_text.get_height()
            # Total height of all elements
            total_height = (
                prompt_height + spacing +
                len(difficulty_selector.buttons) * button_height + (len(difficulty_selector.buttons) - 1) * spacing +
                nav_spacing + nav_button_height +
                nav_spacing + confirm_height
            )
            start_y = (self.screen_height - total_height) / 2
            # Draw prompt
            self.screen.blit(prompt, (center_x - prompt.get_width() / 2, start_y))
            # Draw difficulty buttons
            buttons_y = start_y + prompt_height + spacing
            difficulty_selector.draw(buttons_y)
            # Draw nav buttons
            nav_y = buttons_y + len(difficulty_selector.buttons) * button_height + (len(difficulty_selector.buttons) - 1) * spacing + nav_spacing
            back_button = Button(self.screen, "Back", center_x - nav_button_width - 10, nav_y, nav_button_width, nav_button_height, BLACK, WHITE, WHITE, BLACK, WHITE, BLACK)
            # Next button: yellow/black with black border
            next_button = Button(self.screen, "Next", center_x + 10, nav_y, nav_button_width, nav_button_height, (255, 230, 80), (255, 255, 180), BLACK, BLACK, BLACK)
            mouse_pos = pygame.mouse.get_pos()
            back_button.check_hover(mouse_pos)
            next_button.check_hover(mouse_pos)
            back_button.draw()
            # Next button is only enabled if a difficulty is selected
            if difficulty_selector.selected is not None:
                next_button.draw()
            else:
                pygame.draw.rect(self.screen, (180, 180, 180), next_button.rect)
                pygame.draw.rect(self.screen, BLACK, next_button.rect, 2)
                text_surf = next_button.font.render(next_button.text, True, (100, 100, 100))
                text_rect = text_surf.get_rect(center=next_button.rect.center)
                self.screen.blit(text_surf, text_rect)
            # Draw confirm text
            self.screen.blit(confirm_text, (center_x - confirm_text.get_width() / 2, nav_y + nav_button_height + nav_spacing))
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
                if back_button.is_clicked(mouse_pos, event):
                    return None, True, False  # Go back
                if next_button.is_clicked(mouse_pos, event) and difficulty_selector.selected is not None:
                    return difficulty_selector.get_selected_difficulty(), False, True
                difficulty_selector.handle_event(event, mouse_pos)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and difficulty_selector.selected is not None:
                    return difficulty_selector.get_selected_difficulty(), False, True
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    viewing = False
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
                        if scroll_offset < max(0, len(sorted_leaderboard) - max_visible):
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
                        if scroll_offset < max(0, len(sorted_leaderboard) - max_visible):
                            scroll_offset += 1
                    if event.button == 1 or event.button == 3:
                        viewing = False
            # Draw background image (other) with aspect ratio preserved
            self.blit_centered_bg(self.bg_other, self.screen)
            # Draw semi-transparent overlay over the entire screen
            overlay_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay_surface.fill((0, 0, 0, 180))
            self.screen.blit(overlay_surface, (0, 0))
            # Title
            title = font_large.render("Leaderboard", True, GOLD)
            self.screen.blit(title, (center_x - title.get_width() / 2, 80 * scale_factor))
            # Entries (with scroll)
            y_start = 180 * scale_factor
            line_height = 40 * scale_factor
            if not sorted_leaderboard:
                no_scores = font.render("No scores yet!", True, WHITE)
                self.screen.blit(no_scores, (center_x - no_scores.get_width() / 2, y_start))
            else:
                for i, (name, score) in enumerate(sorted_leaderboard[scroll_offset:scroll_offset+max_visible]):
                    rank = f"{i+1+scroll_offset}. {name}: {score}"
                    color = GOLD if i+scroll_offset == 0 else SILVER if i+scroll_offset == 1 else BRONZE if i+scroll_offset == 2 else WHITE
                    rank_text = font.render(rank, True, color)
                    self.screen.blit(rank_text, (center_x - rank_text.get_width() / 2, y_start + i * line_height))
            # Scroll instructions
            if len(sorted_leaderboard) > max_visible:
                small_font = pygame.font.Font(BOXING_FONT_PATH, int(20 * scale_factor))
                scroll_text = small_font.render("Scroll to see more", True, LIGHT_GREY)
                self.screen.blit(scroll_text, (center_x - scroll_text.get_width() / 2, self.screen_height - 80 * scale_factor))
            # Back instruction
            back_text = small_font.render("Press any key to return", True, LIGHT_GREY)
            self.screen.blit(back_text, (center_x - back_text.get_width() / 2, self.screen_height - 40 * scale_factor))
            pygame.display.update()

    def show(self):
        # 1. Title screen
        self.show_title_screen()
        while True:
            # 2. Name input
            back, next_ = self.show_name_input()
            if back:
                self.show_title_screen()
                continue
            if not next_:
                continue
            # 3. Piece selection
            sprite, back, next_ = self.show_piece_selection()
            if back:
                continue  # Go back to name input
            if not next_:
                continue
            # 4. Difficulty selection
            difficulty, back, next_ = self.show_difficulty_selection()
            if back:
                # Go back to piece selection
                while True:
                    sprite, back2, next2 = self.show_piece_selection()
                    if back2:
                        break  # Go back to name input
                    if next2:
                        break  # Proceed to difficulty selection
                if back2:
                    continue  # Go back to name input
                # Now show difficulty again
                continue
            if not next_:
                continue
            return (self.name_input, difficulty, sprite)

class GameUI:
    def __init__(self, screen, player_name, sprite_choice, screen_width, screen_height, ai_vs_ai=False):
        self.screen = screen
        self.player_name = player_name
        self.sprite_choice = sprite_choice
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(BOXING_FONT_PATH, 36)
        self.font_small = pygame.font.Font(BOXING_FONT_PATH, 24)
        self.hover_col = 0
        self.scale_factor = min(screen_width / WINDOW_WIDTH, screen_height / WINDOW_HEIGHT)
        self.square_size = int(SQUARESIZE * self.scale_factor)
        self.radius = int(RADIUS * self.scale_factor)
        self.ai_vs_ai = ai_vs_ai
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
        # Load background image for game (now bg4)
        self.bg_game = pygame.image.load(os.path.join("imgs", "bg4.jpg")).convert()
    
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
        # Always draw the background image first
        bg = pygame.transform.smoothscale(self.bg_game, (self.screen_width, self.screen_height))
        self.screen.blit(bg, (0, 0))
        supersample = 4
        surf_w = int(self.screen_width * supersample)
        surf_h = int(self.screen_height * supersample)
        board_surface = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
        board_surface.fill((0, 0, 0, 0))
        x_offset, y_offset = self.get_offsets()
        x_offset = int(x_offset * supersample)
        y_offset = int(y_offset * supersample)
        scale_factor = self.scale_factor * supersample
        square_size = int(self.square_size * supersample)
        radius = int(self.radius * supersample)
        # Use a darker yellow/orange for the board
        BOARD_COLOR = (255, 180, 40)
        # Draw the board slots
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(board_surface, BOARD_COLOR,
                                 (x_offset + c * square_size,
                                  y_offset + r * square_size + square_size,
                                  square_size, square_size))
                cx = int(x_offset + c * square_size + square_size / 2)
                cy = int(y_offset + r * square_size + square_size + square_size / 2)
                # Draw semi-transparent holes (tempered glass look, less transparent)
                pygame.gfxdraw.filled_circle(board_surface, int(cx), int(cy), int(radius), (0, 0, 0, 180))
                pygame.gfxdraw.aacircle(board_surface, int(cx), int(cy), int(radius), (0, 0, 0, 180))
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                cx = int(x_offset + c * square_size + square_size / 2)
                cy = int(y_offset + WINDOW_HEIGHT * scale_factor - r * square_size - square_size / 2)
                if board[r][c] == PLAYER_PIECE:
                    # Increase piece size to fully cover the hole
                    pygame.gfxdraw.filled_circle(board_surface, int(cx), int(cy), int(radius) + supersample * 2, self.player_color)
                    pygame.gfxdraw.aacircle(board_surface, int(cx), int(cy), int(radius) + supersample * 2, self.player_color)
                elif board[r][c] == AI_PIECE:
                    pygame.gfxdraw.filled_circle(board_surface, int(cx), int(cy), int(radius) + supersample * 2, self.ai_color)
                    pygame.gfxdraw.aacircle(board_surface, int(cx), int(cy), int(radius) + supersample * 2, self.ai_color)
        small_surface = pygame.transform.smoothscale(board_surface, (self.screen_width, self.screen_height))
        self.screen.blit(small_surface, (0, 0))
        # Draw a semi-transparent black header bar at the top
        header_height = int(self.square_size)
        header_surface = pygame.Surface((self.screen_width, header_height), pygame.SRCALPHA)
        header_surface.fill((0, 0, 0, 180))
        self.screen.blit(header_surface, (0, 0))
        x_offset, y_offset = self.get_offsets()
        if self.ai_vs_ai:
            ai1_text = self.font_small.render("AI 1", True, self.player_color)
            ai2_text = self.font_small.render("AI 2", True, self.ai_color)
            self.screen.blit(ai1_text, (x_offset + 10, y_offset + 10))
            self.screen.blit(ai2_text, (x_offset + 30 + ai1_text.get_width(), y_offset + 10))
        else:
            player_text = self.font_small.render(f"Player: {self.player_name}", True, self.player_color)
            self.screen.blit(player_text, (x_offset + 10, y_offset + 10))
    
    def update_hover(self, x_pos):
        # Calculate centering offsets
        x_offset, y_offset = self.get_offsets()
        # Adjust x_pos for offset
        adjusted_x_pos = x_pos - x_offset
        # Show piece hover effect
        header_surface = pygame.Surface((self.screen_width, int(self.square_size)), pygame.SRCALPHA)
        header_surface.fill((0, 0, 0, 180))
        self.screen.blit(header_surface, (0, 0))
        # Draw player info and score again (since we cleared the top)
        player_text = self.font_small.render(f"Player: {self.player_name}", True, self.player_color)
        self.screen.blit(player_text, (x_offset + 10, y_offset + 10))
        # Calculate column from x position
        self.hover_col = min(max(int(adjusted_x_pos // self.square_size), 0), COLUMN_COUNT - 1)
        # Draw hover piece
        pygame.draw.circle(self.screen, self.player_color, 
                          (x_offset + self.hover_col * self.square_size + self.square_size//2, 
                           y_offset + self.square_size//2), 
                          int(self.radius))
        pygame.display.update()
    
    def draw_score(self, score):
        # Calculate centering offsets
        x_offset, y_offset = self.get_offsets()
        # User vs User mode: tuple with (score1, score2, name1, name2, color1, color2)
        if isinstance(score, tuple) and len(score) == 6:
            score1, score2, name1, name2, color1, color2 = score
            font = self.font_small
            text1 = font.render(f"{name1}: {score1}", True, RED if color1 == "Red" else LIGHT_BLUE if color1 == "Blue" else GREEN)
            text2 = font.render(f"{name2}: {score2}", True, RED if color2 == "Red" else LIGHT_BLUE if color2 == "Blue" else GREEN)
            total_width = text1.get_width() + 20 + text2.get_width()
            right_x = x_offset + WINDOW_WIDTH * self.scale_factor - total_width - 10
            self.screen.blit(text1, (right_x, y_offset + 10))
            self.screen.blit(text2, (right_x + text1.get_width() + 20, y_offset + 10))
        elif self.ai_vs_ai and isinstance(score, tuple):
            ai1_score, ai2_score = score
            ai1_text = self.font_small.render(f"AI 1: {ai1_score}", True, self.player_color)
            ai2_text = self.font_small.render(f"AI 2: {ai2_score}", True, self.ai_color)
            total_width = ai1_text.get_width() + 20 + ai2_text.get_width()
            right_x = x_offset + WINDOW_WIDTH * self.scale_factor - total_width - 10
            self.screen.blit(ai1_text, (right_x, y_offset + 10))
            self.screen.blit(ai2_text, (right_x + ai1_text.get_width() + 20, y_offset + 10))
        else:
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
            label = self.font.render("game is a Draw!", True, WHITE)
        else:
            label = self.font.render(f"{winner} wins!", True, self.player_color)
        
        self.screen.blit(label_bg, (x_offset + WINDOW_WIDTH * self.scale_factor//2 - 200 * self.scale_factor, 
                                   y_offset + WINDOW_HEIGHT * self.scale_factor//2 - 40 * self.scale_factor))
        self.screen.blit(label, (x_offset + WINDOW_WIDTH * self.scale_factor//2 - label.get_width()//2, 
                                y_offset + WINDOW_HEIGHT * self.scale_factor//2 - label.get_height()//2))
        pygame.display.update()

    def blit_centered_bg(self, img, screen):
        img_w, img_h = img.get_size()
        win_w, win_h = screen.get_size()
        scale = max(win_w / img_w, win_h / img_h)
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        bg_scaled = pygame.transform.smoothscale(img, (new_w, new_h))
        x = (win_w - new_w) // 2
        y = (win_h - new_h) // 2
        screen.fill((0, 0, 0))
        screen.blit(bg_scaled, (x, y))