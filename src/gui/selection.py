import pygame
from utils.button import Button  # Import Button từ utils
import sys
from gui.gym_mode import show_gym
from gui.challenge_mode import show_challenge
from functions.rehabilitation.gesture import start_gesture_game
from utils.background import *

# Hàm hiển thị menu chọn chế độ chơi
def show_selection(screen):
    
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
    recovery_button = Button("Rehabilitation", 300, 150, 200, 50,LIGHT_PINK , HOVER)
    gym_button = Button("Gym mode", 300, 250, 200, 50, LIGHT_PINK, HOVER)
    pull_up_button = Button("Challenge", 300, 350, 200, 50, LIGHT_PINK, HOVER)
    back_button = Button("Back", 650, 500, 100, 50, LIGHT_PINK, HOVER)

    while True:
        draw_gradient(screen, (173, 216, 230), (255, 240, 245))

        # Vẽ các nút
        recovery_button.is_hovered()
        recovery_button.draw(screen, title_font)

        gym_button.is_hovered()
        gym_button.draw(screen, title_font)

        pull_up_button.is_hovered()
        pull_up_button.draw(screen, title_font)

        back_button.is_hovered()
        back_button.draw(screen, title_font)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Kiểm tra khi nhấn các nút
            if recovery_button.is_clicked(event):
                print("Chọn chế độ Phục hồi chức năng")  # Thực hiện chức năng cho nút Phục hồi chức năng
                screen = pygame.display.set_mode((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                start_gesture_game(screen)
            if gym_button.is_clicked(event):
                print("Chọn chế độ Tập gym")  # Thực hiện chức năng cho nút Tập gym
                show_gym(screen)
            if pull_up_button.is_clicked(event):
                print("Chọn chế độ Thử thách kéo xà")  # Thực hiện chức năng cho nút Thử thách kéo xà
                show_challenge(screen)
            if back_button.is_clicked(event):
                print("Back")
                return 

        pygame.display.flip()

# Chạy menu chọn chế độ chơi
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chọn chế độ chơi")
    show_selection(screen)
