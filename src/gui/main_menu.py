import pygame
from gui.instruction import show_instructions
from gui.settings import settings_menu
from gui.selection import show_selection
from utils.button import Button  # Import Button từ utils
from utils.sounds import *
from utils.title import Title
from utils.background import *
import sys

# Khởi tạo Pygame
pygame.init()

load_background_sounds()
play_background_music()

# Kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pose Estimation Game")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
LIGHT_PINK = (255, 182, 193)
HOVER= (245, 162, 173)

# Tạo các nút bấm
font_path="../assets/fonts/Gamefont.ttf"
button_font = pygame.font.Font(font_path, 30)
title_font=pygame.font.Font(font_path, 50)
select_mode_button = Button("Select mode", 300, 200, 200, 50, LIGHT_PINK, HOVER)
settings_button = Button("Settings", 300, 300, 200, 50, LIGHT_PINK, HOVER)
instruction_button = Button("Instruction", 300, 400, 200, 50, LIGHT_PINK, HOVER)
exit_button = Button("Exit", 300, 500, 200, 50, LIGHT_PINK, HOVER)

# Tạo đối tượng Title
menu_title = Title(
    text="Pose Estimation", 
    font=title_font, 
    color=LIGHT_PINK, 
    position=(SCREEN_WIDTH // 2, 120), 
    glow=True, 
    glow_color=(255, 223, 0), 
    glow_radius=15
)

# Vòng lặp chính của menu
def main_menu():
    while True:
        draw_gradient(screen, (173, 216, 230), (255, 240, 245))
        update_particles(screen)

        menu_title.draw(screen)

        # Vẽ các nút bấm
        for button in [select_mode_button, settings_button, instruction_button, exit_button]:
            button.is_hovered()
            button.draw(screen, button_font)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Kiểm tra xem nút nào được nhấp
            if select_mode_button.is_clicked(event):
                print("Select mode clicked")
                show_selection(screen)
                # Ở đây bạn có thể chuyển sang giao diện chơi game
            if instruction_button.is_clicked(event):
                print("Instruction clicked")
                show_instructions(screen)
                # Ở đây bạn có thể chuyển sang giao diện cài đặt
            if settings_button.is_clicked(event):
                print("Settings clicked")
                settings_menu(screen)
                # Ở đây bạn có thể chuyển sang giao diện cài đặt
            if exit_button.is_clicked(event):
                print("Exit clicked")
                pygame.quit()
                sys.exit()

        # Cập nhật màn hình
        pygame.display.flip()
