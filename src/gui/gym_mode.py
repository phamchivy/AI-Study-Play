import pygame
from utils.button import Button  # Import Button từ utils
import sys
from functions.gym.squat_evaluation import show_squat
from functions.gym.deadlift_evaluation import show_deadlift
from functions.gym.pushup_evaluation import show_pushup
from utils.background import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT=600
# Màu sắc
NAVY = (25, 25, 112)
LIGHT_PINK = (255, 182, 193)
HOVER= (245, 162, 173)
LIGHT_BLUE=(173, 216, 230)

font_path="../assets/fonts/Gamefont.ttf"
title_font = pygame.font.Font(font_path, 30)

# Hàm hiển thị menu chọn chế độ chơi
def show_gym(screen):
    # Tạo các nút bấm trong menu chính
    recovery_button = Button("Squat", 300, 150, 200, 50, LIGHT_PINK, HOVER)
    deadlift_button = Button("Deadlift", 300, 250, 200, 50, LIGHT_PINK, HOVER)
    push_up_button = Button("Push up", 300, 350, 200, 50, LIGHT_PINK, HOVER)
    back_button = Button("Back", 650, 500, 100, 50, LIGHT_PINK, HOVER)

    # Trang chính
    while True:
        draw_gradient(screen, (173, 216, 230), (255, 240, 245))
        update_particles(screen)

        # Vẽ các nút
        recovery_button.is_hovered()
        recovery_button.draw(screen, title_font)

        deadlift_button.is_hovered()
        deadlift_button.draw(screen, title_font)

        push_up_button.is_hovered()
        push_up_button.draw(screen, title_font)

        back_button.is_hovered()
        back_button.draw(screen, title_font)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Kiểm tra khi nhấn các nút
            if recovery_button.is_clicked(event):
                print("Squat")
                show_squat(screen)
                # Tắt Pygame trước khi chuyển sang chế độ Squat
            if deadlift_button.is_clicked(event):
                print("Deadlift")  # Thực hiện chức năng cho nút Deadlift
                show_deadlift(screen)
            if push_up_button.is_clicked(event):
                print("Push up")  # Thực hiện chức năng cho nút Chống đẩy
                show_pushup(screen)
            if back_button.is_clicked(event):
                return

        pygame.display.flip()
