import pygame
from utils.button import Button  # Import Button từ utils
from utils.sounds import *
from utils.title import *
from utils.background import *
import sys

# Khởi tạo Pygame
pygame.init()

EFFECT_SOUND_PATH = "../assets/sounds/button_click.mp3"
load_effect_sounds(EFFECT_SOUND_PATH)

SCREEN_WIDTH = 800
# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
NAVY = (25, 25, 112)
LIGHT_PINK = (255, 182, 193)
HOVER= (245, 162, 173)
LIGHT_BLUE=(173, 216, 230)

font_path="../assets/fonts/Gamefont.ttf"
text_path="../assets/fonts/Text.ttf"
title_font = pygame.font.Font(font_path, 40)

settings_title = Title(
        text="Settings:", 
        font=title_font, 
        color=LIGHT_PINK, 
        position=(SCREEN_WIDTH // 4.5, 70), 
        glow=True, 
        glow_color=(255, 223, 0), 
        glow_radius=15
    )

# Thanh trượt
class Slider:
    def __init__(self, x, y, width, height, value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = value
        self.grabbed = False

    def draw(self, screen):
        # Vẽ đường dẫn của thanh trượt (mềm mại hơn)
        pygame.draw.line(screen, NAVY, 
                         (self.rect.x, self.rect.centery), 
                         (self.rect.right, self.rect.centery), 
                         6)  # Độ dày

        # Vẽ phần đã chọn của thanh trượt
        pos = int(self.rect.x + self.value * self.rect.width)
        pygame.draw.line(screen, LIGHT_BLUE, 
                         (self.rect.x, self.rect.centery), 
                         (pos, self.rect.centery), 
                         8)

        # Vẽ nút trên thanh trượt (dạng gradient)
        pygame.draw.circle(screen, (255, 255, 255), (pos, self.rect.centery), self.rect.height // 2)
        pygame.draw.circle(screen, (200, 200, 255), (pos, self.rect.centery), self.rect.height // 2 - 3)
        pygame.draw.circle(screen, BLUE, (pos, self.rect.centery), self.rect.height // 2 - 6)

        # Vẽ bóng cho nút
        pygame.draw.circle(screen, (150, 150, 200), (pos + 2, self.rect.centery + 2), self.rect.height // 2 - 4, 1)

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
font = pygame.font.Font(font_path, 30)
back_button = Button("Back", 650, 500, 100, 50, LIGHT_PINK, HOVER)
background_slider = Slider(350, 200, 200, 20, background_volume)
effect_slider = Slider(350, 300, 200, 20, effect_volume)

# Hàm cài đặt
def settings_menu(screen):
    #global background_volume, effect_volume

    while True:
        draw_gradient(screen, (173, 216, 230), (255, 240, 245))
        settings_title.draw(screen)

        # Vẽ các thành phần
        back_button.is_hovered()
        back_button.draw(screen, font)
        background_slider.draw(screen)
        effect_slider.draw(screen)

        # Vẽ các nhãn
        background_text = font.render("Background Volume", True, NAVY)
        screen.blit(background_text, (50, 190))
        effect_text = font.render("Effect Volume", True, NAVY)
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

