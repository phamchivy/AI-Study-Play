import pygame
from utils.button import Button  # Import Button từ utils
import sys
from functions.gym.squat_evaluation import evaluate_squat_pose
from functions.gym.deadlift_evaluation import evaluate_deadlift_pose
from functions.gym.pushup_evaluation import evaluate_pushup_pose
import cv2

# Hàm hiển thị menu chọn chế độ chơi
def show_gym(screen):
    # Màu sắc
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Tạo font chữ
    font = pygame.font.Font(None, 40)

    # Tạo các nút bấm trong menu chính
    recovery_button = Button("Squat", 300, 150, 200, 50, (0, 255, 0), (100, 255, 100))
    gym_button = Button("Deadlift", 300, 250, 200, 50, (0, 0, 255), (100, 100, 255))
    pull_up_button = Button("Chống đẩy", 300, 350, 200, 50, (255, 0, 0), (255, 100, 100))

    # Trang chính
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
                print("Squat")
                evaluate_squat_pose()
                # Tắt Pygame trước khi chuyển sang chế độ Squat
                #run_squat()
            if gym_button.is_clicked(event):
                print("Deadlift")  # Thực hiện chức năng cho nút Deadlift
                evaluate_deadlift_pose()
            if pull_up_button.is_clicked(event):
                print("Chống đẩy")  # Thực hiện chức năng cho nút Chống đẩy
                evaluate_pushup_pose()

        pygame.display.flip()

"""
# Hàm chạy chế độ Squat
def run_squat():
    if evaluate_squat_pose() :
    # Khởi động lại Pygame và quay lại menu chính
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Chọn chế độ chơi")
        show_gym(screen)  # Quay lại menu chính
"""


# Chạy menu chọn chế độ chơi
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Chọn chế độ chơi")
    show_gym(screen)
