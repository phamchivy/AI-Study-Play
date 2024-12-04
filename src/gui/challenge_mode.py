import pygame
from utils.button import Button  # Import Button từ utils
import sys
from functions.challenge.highknees_challenge import *
import sqlite3
import os
from utils.background import *
from utils.title import *
from utils.text import *

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
# Màu sắc cho các vị trí
TOP_COLORS = (255, 215, 0)  # Vàng, bạc, đồng cho top 1, 2, 3
# Kích thước font cho các vị trí
TOP_FONT_SIZES = [40, 35, 30]
DEFAULT_FONT_SIZE = 25

font_path="../assets/fonts/Gamefont.ttf"
text_path="../assets/fonts/Text.ttf"
title_font = pygame.font.Font(font_path, 30)
text_font=pygame.font.Font(text_path, 20)

# Tạo các nút bấm trong menu chính
start_challenge_button = Button("Start", 300, 150, 200, 50,LIGHT_PINK , HOVER)
highscore_button = Button("High score", 300, 250, 200, 50, LIGHT_PINK, HOVER)
back_button = Button("Back", 650, 500, 100, 50, LIGHT_PINK, HOVER)

badge_images = [
    pygame.image.load("../assets/images/1st.png"),
    pygame.image.load("../assets/images/2nd.png"),
    pygame.image.load("../assets/images/3rd.png"),
]

# Hàm lấy high scores từ cơ sở dữ liệu
def fetch_high_scores():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../db/fitness_app.db"))
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT user_name, reps FROM high_knees_results ORDER BY reps DESC LIMIT 10")
    scores = cursor.fetchall()
    conn.close()
    return scores

# Hàm hiển thị high scores lên giao diện trong vòng lặp
def show_high_scores(screen, badge_images=None):
    scores = fetch_high_scores()
    show_scores = True  # Cờ kiểm tra trạng thái hiển thị scores
    badge_size = (40, 40)  # Kích thước huy hiệu

    highscore_title = Title(
        text="High Score", 
        font=title_font, 
        color=LIGHT_PINK, 
        position=(100, 50), 
        glow=True, 
        glow_color=(255, 223, 0), 
        glow_radius=15
    )

    while show_scores:
        draw_gradient(screen, (173, 216, 230), (255, 240, 245))

        # Vẽ các nút
        back_button.is_hovered()
        back_button.draw(screen, title_font)

        # Hiển thị tiêu đề
        highscore_title.draw(screen)

        # Hiển thị từng hàng điểm
        start_y = 120
        x_offset = 100  # Vị trí ngang
        extra_spacing = 20  # Khoảng cách thêm giữa top 3 và top 4
        for idx, (user_name, reps) in enumerate(scores[:10]):  # Giới hạn top 10
            # Badge và màu sắc đặc biệt cho Top 1, 2, 3
            if idx < 3:  
                badge = pygame.transform.scale(badge_images[idx], badge_size)
                badge_rect = badge.get_rect()
                badge_rect.topleft = (x_offset, start_y + idx * (badge_size[1] + 20))
                screen.blit(badge, badge_rect)
                text_x = badge_rect.right + 10  # Căn chỉnh text bên phải huy hiệu
                color = TOP_COLORS if idx == 0 else NAVY  # Màu đặc biệt cho Top 1
                font_size = TOP_FONT_SIZES[idx]
            else:  # Các thứ hạng khác
                color = NAVY
                font_size = DEFAULT_FONT_SIZE
                text_x = x_offset + 13
                badge_rect = None  # Không có badge cho Top 4 trở đi

            # Font chữ
            font = pygame.font.Font(text_path, font_size)

            # Tạo text và vị trí vẽ
            score_text = font.render(f"{user_name}: {reps} reps", True, color) if idx < 3 else \
                        font.render(f"{idx + 1}.   {user_name}: {reps} reps", True, color)
            text_rect = score_text.get_rect()

            if badge_rect:
                text_rect.midleft = (text_x, badge_rect.centery)  # Căn giữa dọc với badge
            else:
                text_rect.topleft = (text_x, start_y + idx * (font_size + 25)+(extra_spacing if idx >= 3 else 0))

            # Vẽ chữ lên màn hình
            screen.blit(score_text, text_rect)
            # Nổi bật thêm Top 1 bằng cách vẽ viền sáng
            if idx == 0:
                glow_surface = pygame.Surface((text_rect.width + 10, text_rect.height + 10), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (255, 215, 0, 100), glow_surface.get_rect(), border_radius=15)
                screen.blit(glow_surface, (text_rect.x - 5, text_rect.y - 5))

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.is_clicked(event):  # Hoặc có thể sử dụng phím khác như K_RETURN
                show_scores = False
        pygame.display.flip()  # Cập nhật màn hình

# Hàm hiển thị menu chọn chế độ chơi
def show_challenge(screen):
    # Trang chính
    while True:
        draw_gradient(screen, (173, 216, 230), (255, 240, 245))
        update_particles(screen)
        
        # Vẽ các nút
        start_challenge_button.is_hovered()
        start_challenge_button.draw(screen, title_font)

        # Vẽ các nút
        highscore_button.is_hovered()
        highscore_button.draw(screen, title_font)

        # Vẽ các nút
        back_button.is_hovered()
        back_button.draw(screen, title_font)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Kiểm tra khi nhấn các nút
            if start_challenge_button.is_clicked(event):
                print("Start Challenge")
                high_knees_challenge(screen)

            if highscore_button.is_clicked(event):
                print("High Score")
                show_high_scores(screen,badge_images)

            if back_button.is_clicked(event):
                print("Back")
                return
        pygame.display.flip()