import pygame
from utils.button import Button  # Import Button từ utils
import sys

# Hàm hiển thị hướng dẫn
def show_instructions(screen):
    # Màu sắc
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Tạo font chữ
    font = pygame.font.Font(None, 40)

    # Nội dung hướng dẫn
    instructions = [
        "Hướng dẫn chơi game:",
        "1. Sử dụng camera để nhận diện dáng.",
        "2. Thực hiện các động tác theo hướng dẫn.",
        "3. Hoàn thành tất cả các cấp độ để chiến thắng.",
        "4. Nhấn 'ESC' để trở về menu chính."
    ]

    while True:
        screen.fill(BLACK)

        font = pygame.font.Font(None, 40)
        back_button = Button("Back", 300, 500, 200, 50, (0, 0, 255), (100, 100, 100))

        # Vẽ hướng dẫn lên màn hình
        for i, line in enumerate(instructions):
            text_surface = font.render(line, True, WHITE)
            screen.blit(text_surface, (50, 50 + i * 50))
        
        back_button.is_hovered()
        back_button.draw(screen, font)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_button.is_clicked(event):
                return  # Trở về menu chính khi nhấn nút Back

        # Cập nhật màn hình
        pygame.display.flip()
