import pygame
from utils.button import Button  # Import Button từ utils
from utils.sounds import *
import sys

# Khởi tạo Pygame
pygame.init()

EFFECT_SOUND_PATH = "../assets/sounds/button_click.mp3"
load_effect_sounds(EFFECT_SOUND_PATH)

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)

# Thanh trượt
class Slider:
    def __init__(self, x, y, width, height, value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = value
        self.grabbed = False

    def draw(self, screen):
        # Vẽ thanh trượt
        pygame.draw.rect(screen, GRAY, self.rect)
        # Vẽ điểm trên thanh trượt
        pos = int(self.rect.x + self.value * self.rect.width)
        pygame.draw.circle(screen, BLUE, (pos, self.rect.centery), self.rect.height // 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.grabbed = True
                play_effect_sound(EFFECT_SOUND_PATH)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION:
            if self.grabbed:
                relative_x = event.pos[0] - self.rect.x
                self.value = max(0, min(1, relative_x / self.rect.width))    

# Tạo nút và thanh trượt
font = pygame.font.Font(None, 40)
back_button = Button("Back", 650, 500, 100, 50, BLUE, GRAY)
background_slider = Slider(300, 200, 200, 20, background_volume)
effect_slider = Slider(300, 300, 200, 20, effect_volume)

# Hàm cài đặt
def settings_menu(screen):
    #global background_volume, effect_volume

    while True:
        screen.fill(BLACK)

        # Vẽ các thành phần
        back_button.is_hovered()
        back_button.draw(screen, font)
        background_slider.draw(screen)
        effect_slider.draw(screen)

        # Vẽ các nhãn
        background_text = font.render("Background Volume", True, WHITE)
        screen.blit(background_text, (50, 190))
        effect_text = font.render("Effect Volume", True, WHITE)
        screen.blit(effect_text, (50, 290))

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_button.is_clicked(event):
                return  # Quay lại menu chính

            background_slider.handle_event(event)
            effect_slider.handle_event(event)

        # Cập nhật âm lượng
        background_volume = background_slider.value
        set_background_volume(background_volume)
        effect_volume = effect_slider.value
        set_effect_volume(load_effect_sounds(EFFECT_SOUND_PATH), effect_volume)

        # Cập nhật màn hình
        pygame.display.flip()

