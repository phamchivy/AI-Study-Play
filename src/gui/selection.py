import pygame
from utils.button import Button  # Import Button từ utils
import sys
from gui.gym_mode import show_gym

# Hàm hiển thị menu chọn chế độ chơi
def show_selection(screen):
    # Màu sắc
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Tạo font chữ
    font = pygame.font.Font(None, 40)

    # Tạo các nút bấm trong menu
    recovery_button = Button("Phục hồi chức năng", 300, 150, 200, 50, (0, 255, 0), (100, 255, 100))
    gym_button = Button("Tập gym", 300, 250, 200, 50, (0, 0, 255), (100, 100, 255))
    pull_up_button = Button("Thử thách kéo xà", 300, 350, 200, 50, (255, 0, 0), (255, 100, 100))

    while True:
        screen.fill(BLACK)

        # Vẽ các nút
        recovery_button.is_hovered()
        recovery_button.draw(screen, font)

        gym_button.is_hovered()
        gym_button.draw(screen, font)

        pull_up_button.is_hovered()
        pull_up_button.draw(screen, font)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Kiểm tra khi nhấn các nút
            if recovery_button.is_clicked(event):
                print("Chọn chế độ Phục hồi chức năng")  # Thực hiện chức năng cho nút Phục hồi chức năng
            if gym_button.is_clicked(event):
                print("Chọn chế độ Tập gym")  # Thực hiện chức năng cho nút Tập gym
                show_gym(screen)
            if pull_up_button.is_clicked(event):
                print("Chọn chế độ Thử thách kéo xà")  # Thực hiện chức năng cho nút Thử thách kéo xà

        pygame.display.flip()

# Chạy menu chọn chế độ chơi
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chọn chế độ chơi")
    show_selection(screen)
