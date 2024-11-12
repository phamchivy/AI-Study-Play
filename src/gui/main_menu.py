import pygame
from gui.instruction import show_instructions
from gui.settings import settings_menu
from gui.selection import show_selection
from utils.button import Button  # Import Button từ utils
from utils.sounds import *
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

# Tạo các nút bấm
font = pygame.font.Font(None, 40)
select_mode_button = Button("Select mode", 300, 200, 200, 50, BLUE, GRAY)
settings_button = Button("Settings", 300, 300, 200, 50, BLUE, GRAY)
instruction_button = Button("Instruction", 300, 400, 200, 50, BLUE, GRAY)
exit_button = Button("Exit", 300, 500, 200, 50, BLUE, GRAY)

# Vòng lặp chính của menu
def main_menu():
    while True:
        screen.fill(BLACK)

        # Vẽ các nút bấm
        for button in [select_mode_button, settings_button, instruction_button, exit_button]:
            button.is_hovered()
            button.draw(screen, font)

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

# Chạy chương trình
if __name__ == "__main__" and "main.py" in sys.argv[0]:
    main_menu()
