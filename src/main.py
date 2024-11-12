from gui import main_menu
import pygame

def main():
    pygame.init()

    # Chạy giao diện menu chính
    main_menu.main_menu()

    # Khi người chơi chọn bắt đầu game, gọi hàm từ game.py
    # Bạn có thể thêm điều kiện hoặc các hàm khác tùy thuộc vào logic của game

if __name__ == "__main__":
    main()
