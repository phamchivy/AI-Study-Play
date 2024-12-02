import pygame
from .sounds import *

EFFECT_SOUND_PATH = "../assets/sounds/button_click.mp3"
load_effect_sounds(EFFECT_SOUND_PATH)

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, shadow_color=(50, 50, 50)):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.shadow_color = shadow_color
        self.current_color = color

    def draw(self, screen, font):
        # Vẽ bóng
        shadow_rect = self.rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(screen, self.shadow_color, shadow_rect, border_radius=10)

        # Vẽ nút
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)

        # Vẽ viền cho nút
        pygame.draw.rect(screen, (255, 255, 255), self.rect, width=2, border_radius=10)

        # Vẽ text
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                play_effect_sound(EFFECT_SOUND_PATH)
                return True
        return False
