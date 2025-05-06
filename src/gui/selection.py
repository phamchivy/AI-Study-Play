import pygame
from utils.button import Button  # Import Button từ utils
import sys
from gui.finger_mode import show_finger_selection
from gui.handwriting_mode import show_hand_selection
from utils.background import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT=600
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
title_font = pygame.font.Font(font_path, 30)


# Tạo các nút bấm trong menu
handwriting_button = Button("Handwriting", 270, 200, 250, 50, LIGHT_PINK, HOVER)
finger_button = Button("Finger Counting", 270, 300, 250, 50, LIGHT_PINK, HOVER)
back_button = Button("Back", 650, 500, 100, 50, LIGHT_PINK, HOVER)

# Hàm hiển thị menu chọn chế độ chơi
def show_selection(screen):
    while True:
        draw_gradient(screen, (173, 216, 230), (255, 240, 245))
        update_particles(screen)

        # Vẽ các nút

        handwriting_button.is_hovered()
        handwriting_button.draw(screen, title_font)

        finger_button.is_hovered()
        finger_button.draw(screen, title_font)

        back_button.is_hovered()
        back_button.draw(screen, title_font)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if handwriting_button.is_clicked(event):
                print("Handwriting Mode")  # Thực hiện chức năng cho nút Tập gym
                show_hand_selection(screen)
            if finger_button.is_clicked(event):
                print("Finger Counting Mode")  # Thực hiện chức năng cho nút Thử thách kéo xà
                show_finger_selection(screen)
            if back_button.is_clicked(event):
                print("Back")
                return 

        pygame.display.flip()
