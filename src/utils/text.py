import pygame
from utils.button import Button  # Import Button từ utils
from utils.title import *
from utils.background import *
import sys

# Hàm để chia văn bản thành nhiều dòng
def wrap_text(text, font, max_width):
    words = text.split(' ')  # Chia đoạn văn bản thành các từ
    lines = []
    current_line = words[0]  # Dòng hiện tại bắt đầu bằng từ đầu tiên

    for word in words[1:]:
        test_line = current_line + ' ' + word  # Tạo dòng thử với từ tiếp theo
        width, _ = font.size(test_line)  # Kiểm tra độ dài dòng thử

        if width <= max_width:  # Nếu dòng thử không quá rộng
            current_line = test_line  # Tiếp tục thêm từ vào dòng hiện tại
        else:
            lines.append(current_line)  # Nếu quá rộng, lưu dòng hiện tại và bắt đầu dòng mới
            current_line = word  # Dòng mới bắt đầu từ từ này

    lines.append(current_line)  # Thêm dòng cuối cùng
    return lines

def show_text(screen,y_pos,instructions,SCREEN_WIDTH):
    text_path="../assets/fonts/Text.ttf"
    text_font=pygame.font.Font(text_path, 20)
    NAVY = (25, 25, 112)
    for i, instruction  in enumerate(instructions):
        wrapped_lines = wrap_text(instruction, text_font, SCREEN_WIDTH - SCREEN_WIDTH // 5.5)
    # Vẽ từng dòng sau khi đã chia
        for line in wrapped_lines:
            text_surface = text_font.render(line, True, NAVY)
            # Căn chỉnh văn bản theo vị trí ngang và dọc
            x_pos = SCREEN_WIDTH // 6 # Căn từ SCREEN_WIDTH // 6
            y_pos += 50        # Cách nhau 50px cho mỗi dòng
            screen.blit(text_surface, (x_pos, y_pos))