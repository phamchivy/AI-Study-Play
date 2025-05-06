import pygame
from utils.background import *
from utils.text import *
from utils.title import *
from utils.button import Button
from utils.quiz import QuizManager
from functions.hand_writing.hand_writing_func import get_drawn_digit
from db.save_db import save_handwriting_result_to_db
from db.fetch_data import fetch_hand_high_scores
import time
from datetime import datetime
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
font_path="../assets/fonts/Gamefont.ttf"
text_path="../assets/fonts/Text.ttf"
title_font = pygame.font.Font(font_path, 40)
back_font = pygame.font.Font(font_path, 30)
text_font=pygame.font.Font(text_path, 20)

# Màu sắc
NAVY = (25, 25, 112)
LIGHT_PINK = (255, 182, 193)
HOVER= (245, 162, 173)

start_button=Button("Start", 50, 500, 100, 50, LIGHT_PINK, HOVER)
back_button = Button("Back", 650, 500, 100, 50, LIGHT_PINK, HOVER)

# Tạo các nút bấm trong menu
start_challenge_button = Button("Start Game", 270, 200, 250, 50, LIGHT_PINK, HOVER)
high_scores_button = Button("High Scores", 270, 300, 250, 50, LIGHT_PINK, HOVER)
back_button = Button("Back", 650, 500, 100, 50, LIGHT_PINK, HOVER)

badge_images = [
    pygame.image.load("../assets/images/1st.png"),
    pygame.image.load("../assets/images/2nd.png"),
    pygame.image.load("../assets/images/3rd.png"),
]

# Tạo đối tượng Title
instruction_title = Title(
    text="Handwriting instruction:", 
    font=title_font, 
    color=LIGHT_PINK, 
    position=(SCREEN_WIDTH // 3.5, 70), 
    glow=True, 
    glow_color=(255, 223, 0), 
    glow_radius=15
)

# Nội dung hướng dẫn
instructions = [
    "In this mode, the game presents 10 random math problems one by one. For each problem:",
    "- There is also have key to reset (c), submit (s), escape (esc)",
    "- After submitting, the game will immediately show whether the answer is correct or incorrect, helping children learn from their mistakes and build confidence."
]

def show_handwriting_mode(screen):
    # Khởi tạo QuizManager
    quiz_manager = QuizManager()
    feedback_message = ""
    color=""
    feedback_timer = 0
    start_time = time.time()
    auto_run = True
    running = True
    while running:
        # Lấy câu hỏi hiện tại từ QuizManager
        current_question = quiz_manager.get_current_question()
        
        if current_question:
            question_text = f"Question {quiz_manager.current_index + 1}: {current_question['question']}"
        else:
            question_text = "Quiz finished! Final "

        draw_gradient(screen, (173, 216, 230), (255, 240, 245))
        y_pos = 60
        instruction_title.draw(screen)
        show_number(screen, y_pos, [question_text], SCREEN_WIDTH)
        
        # Hiển thị điểm số
        score_text = f"Score: {quiz_manager.get_score()}"
        show_number(screen, y_pos + 80, [score_text], SCREEN_WIDTH)

        start_button.is_hovered()
        start_button.draw(screen, back_font)
        back_button.is_hovered()
        back_button.draw(screen, back_font)

        # Vẽ thông báo nếu chưa quá 2 giây
        if feedback_message and time.time() - feedback_timer < 2:
            show_feedback(screen, y_pos + 150, [feedback_message], SCREEN_WIDTH,color)
        else:
            feedback_message = ""  # reset sau 2 giây

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if back_button.is_clicked(event):
                running = False
            if start_button.is_clicked(event):
                # Gọi hàm submit_answer khi người chơi nhập đáp án
                user_input = get_drawn_digit()  # Hàm giả định lấy input từ người chơi
                if quiz_manager.submit_answer(user_input):
                    print("Correct!")
                    feedback_message = "Correct!"
                    feedback_timer = time.time()
                    color= (0, 255, 0) #GREEN 
                else:
                    print("Incorrect!")
                    feedback_message = "Incorrect!"
                    feedback_timer = time.time()
                    color= (255, 0, 0) #RED 
        if auto_run and time.time() - start_time >= 1 and quiz_manager.is_finished() == False:
            user_input = get_drawn_digit() 
            if quiz_manager.submit_answer(user_input):
                print("Correct!")
                feedback_message = "Correct!"
                feedback_timer = time.time()
                color= (0, 255, 0) #GREEN 
            else:
                print("Incorrect!")
                feedback_message = "Incorrect!"
                feedback_timer = time.time()
                color= (255, 0, 0) #RED 
        if quiz_manager.is_finished():
            end_time = time.time()
            user_name = input("\nNhập tên người chơi: ")
            score = quiz_manager.get_score()
            save_handwriting_result_to_db(user_name, score, datetime.fromtimestamp(start_time), end_time)
            print("\nĐã lưu kết quả hand writing.")
            time.sleep(2)  # Cho người chơi đọc thông báo
            running = False  

# Hàm hiển thị high scores lên giao diện
def show_high_scores(screen, badge_images=None):
    scores = fetch_hand_high_scores()  # Lấy điểm từ database
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
        draw_gradient(screen, (173, 216, 230), (255, 240, 245))  # Background gradient
        update_particles(screen)  # Hiển thị các particle effects (nếu có)

        # Vẽ các nút
        back_button.is_hovered()
        back_button.draw(screen, back_font)

        # Hiển thị tiêu đề
        highscore_title.draw(screen)

        # Hiển thị từng hàng điểm
        start_y = 120
        x_offset = 100  # Vị trí ngang
        extra_spacing = 20  # Khoảng cách thêm giữa top 3 và top 4
        for idx, (user_name, score) in enumerate(scores[:10]):  # Giới hạn top 10
            # Badge và màu sắc đặc biệt cho Top 1, 2, 3
            if idx < 3:  
                badge = pygame.transform.scale(badge_images[idx], badge_size) if badge_images else None
                if badge:
                    badge_rect = badge.get_rect()
                    badge_rect.topleft = (x_offset, start_y + idx * (badge_size[1] + 20))
                    screen.blit(badge, badge_rect)
                text_x = badge_rect.right + 10 if badge else x_offset + 13  # Căn chỉnh text bên phải huy hiệu
                color = (255, 215, 0) if idx == 0 else NAVY  # Màu đặc biệt cho Top 1
                font_size = 30  # Kích thước chữ cho top 3
            else:  # Các thứ hạng khác
                color = NAVY
                font_size = 25  # Kích thước chữ cho các vị trí khác
                text_x = x_offset + 13
                badge_rect = None  # Không có badge cho Top 4 trở đi

            # Font chữ
            font = pygame.font.Font(font_path, font_size)

            # Tạo text và vị trí vẽ
            score_text = font.render(f"{user_name}: {score} score", True, color) if idx < 3 else \
                        font.render(f"{idx + 1}.   {user_name}: {score} score", True, color)
            text_rect = score_text.get_rect()

            if badge_rect:
                text_rect.midleft = (text_x, badge_rect.centery)  # Căn giữa dọc với badge
            else:
                text_rect.topleft = (text_x, start_y + idx * (font_size + 25) + (extra_spacing if idx >= 3 else 0))

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
def show_hand_selection(screen):
    while True:
        draw_gradient(screen, (173, 216, 230), (255, 240, 245))  # Background gradient
        update_particles(screen)  # Hiển thị các particle effects (nếu có)

        # Vẽ các nút
        start_challenge_button.is_hovered()
        start_challenge_button.draw(screen, back_font)

        high_scores_button.is_hovered()
        high_scores_button.draw(screen, back_font)

        back_button.is_hovered()
        back_button.draw(screen, back_font)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_challenge_button.is_clicked(event):
                print("\nStart Challenge Mode")  # Gọi hàm cho Start Challenge
                show_handwriting_mode(screen)  # Gọi hàm khi người dùng chọn "Start Challenge"

            if high_scores_button.is_clicked(event):
                print("\nHigh Scores Mode")  # Gọi hàm để hiển thị bảng điểm cao
                show_high_scores(screen,badge_images)  # Giả định bạn có hàm show_high_scores

            if back_button.is_clicked(event):
                print("\nBack")  # Trở về màn hình trước
                return  # Quay lại màn hình trước

        pygame.display.flip()  # Cập nhật màn hình
