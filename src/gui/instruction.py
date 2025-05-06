import pygame
from utils.button import Button  # Import Button từ utils
from utils.title import *
from utils.background import *
from utils.text import *
import sys

# Khởi tạo Pygame
pygame.init()

SCREEN_WIDTH = 800
font_path="../assets/fonts/Gamefont.ttf"
title_font = pygame.font.Font(font_path, 40)
back_font = pygame.font.Font(font_path, 30)

# Màu sắc
NAVY = (25, 25, 112)
LIGHT_PINK = (255, 182, 193)
HOVER= (245, 162, 173)

font = pygame.font.Font(font_path, 40)
back_button = Button("Back", 650, 500, 100, 50, LIGHT_PINK, HOVER)

# Tạo đối tượng Title
instruction_title = Title(
    text="Instruction:", 
    font=title_font, 
    color=LIGHT_PINK, 
    position=(SCREEN_WIDTH // 4.5, 70), 
    glow=True, 
    glow_color=(255, 223, 0), 
    glow_radius=15
)

# Nội dung hướng dẫn
instructions = [
    "Our game is designed to make learning fun and engaging for primary school children. It offers two interactive modes to help kids improve their math skills:",
    "1. Handwriting Mode – where children solve math problems by writing their answers directly by hand.",
    "2. Finger Counting Mode – where they use their fingers to represent and complete math operations."
]

# Hàm hiển thị hướng dẫn
def show_instructions(screen):
    while True:
        draw_gradient(screen, (173, 216, 230), (255, 240, 245))

        instruction_title.draw(screen)
        # Vẽ hướng dẫn lên màn hình
        y_pos = 60  # Vị trí bắt đầu từ trên màn hình
        show_text(screen,y_pos,instructions,SCREEN_WIDTH)
        
        back_button.is_hovered()
        back_button.draw(screen, back_font)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_button.is_clicked(event):
                return  # Trở về menu chính khi nhấn nút Back

        # Cập nhật màn hình
        pygame.display.flip()
