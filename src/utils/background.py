import pygame 
import random

def draw_gradient(screen, start_color, end_color):
    for y in range(screen.get_height()):
        ratio = y / screen.get_height()
        color = [
            start_color[i] + (end_color[i] - start_color[i]) * ratio
            for i in range(3)
        ]
        pygame.draw.line(screen, color, (0, y), (screen.get_width(), y))

particles = [{"pos": [random.randint(0, 800), random.randint(0, 600)], "vel": [1, -1]} for _ in range(50)]

def update_particles(screen):
    for p in particles:
        p["pos"][0] += p["vel"][0]
        p["pos"][1] += p["vel"][1]
        pygame.draw.circle(screen, (173, 216, 230), p["pos"], 3)
        if p["pos"][0] < 0 or p["pos"][0] > screen.get_width():
            p["vel"][0] *= -1
        if p["pos"][1] < 0 or p["pos"][1] > screen.get_height():
            p["vel"][1] *= -1


"""
# Định nghĩa sao băng
class Meteor:
    def __init__(self, x, y, length, color, speed):
        self.x = x
        self.y = y
        self.length = length
        self.color = color
        self.speed = speed
        self.trail = []

    def update(self):
        # Thêm vị trí hiện tại vào đường bay
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
        # Di chuyển sao băng
        self.x += self.speed
        self.y += self.speed * 0.5

    def draw(self, screen):
        # Vẽ đường bay của sao băng
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i + 1) / len(self.trail))
            pygame.draw.line(
                screen,
                (*self.color, alpha),
                pos,
                self.trail[min(i + 1, len(self.trail) - 1)],
                2
            )
        # Vẽ sao băng
        pygame.draw.line(screen, self.color, (self.x, self.y), (self.x - self.length, self.y - self.length), 4)

# Danh sách sao băng
meteors = []
for _ in range(5):
    x = random.randint(0, 800)
    y = random.randint(0, 300)
    length = random.randint(10, 50)
    color = (255, random.randint(100, 255), 0)
    speed = random.uniform(5, 10)
    meteors.append(Meteor(x, y, length, color, speed))

# Định nghĩa lớp sao chổi
class Comet:
    def __init__(self, x, y, length, color, speed):
        self.x = x
        self.y = y
        self.length = length
        self.color = color
        self.speed = speed
        self.trail = []  # Lưu vệt sáng

    def update(self):
        # Thêm vị trí hiện tại vào danh sách vệt sáng
        self.trail.append((self.x, self.y))
        if len(self.trail) > 30:  # Chỉ giữ 30 điểm gần nhất
            self.trail.pop(0)
        # Di chuyển sao chổi
        self.x += self.speed
        self.y += self.speed * 0.3

    def draw(self, screen):
        # Vẽ đuôi chổi (mờ dần)
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (1 - i / len(self.trail)))  # Độ mờ dần
            pygame.draw.circle(screen, (*self.color, alpha), pos, max(1, 8 - i // 4))

         # Vẽ đầu chổi (phần sáng chính, to hơn)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 20)  # Đầu lớn hơn
        #pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 10)  # Lõi trắng sáng

# Danh sách sao chổi
comets = []
for _ in range(3):
    x = random.randint(0, 800)
    y = random.randint(0, 300)
    length = random.randint(20, 60)
    color = (255, random.randint(150, 255), random.randint(100, 200))  # Màu tươi sáng
    speed = random.uniform(0.5, 2)
    comets.append(Comet(x, y, length, color, speed))

def draw_abstract_shapes(screen):
    # Vẽ các hình ngẫu nhiên
    for _ in range(5):  # Vẽ 5 hình ngẫu nhiên
        radius = random.randint(50, 150)  # Sử dụng random từ Python
        x = random.randint(radius, screen.get_width() - radius)
        y = random.randint(radius, screen.get_height() - radius)

        # Chọn màu ngẫu nhiên
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Vẽ hình tròn ngẫu nhiên
        pygame.draw.circle(screen, color, (x, y), radius)

def draw_wave(screen, time, color):
    points = []
    for x in range(0, screen.get_width(), 5):
        y = int(50 * math.sin((x / 50) + time) + screen.get_height() // 2)
        points.append((x, y))
    pygame.draw.lines(screen, color, False, points, 2)
"""

"""""
# Cập nhật và vẽ sao băng
for meteor in meteors:
    meteor.update()
    meteor.draw(screen)

    # Tạo sao băng mới nếu nó bay ra khỏi màn hình
    if meteor.x > 800 or meteor.y > 600:
        meteor.x = random.randint(0, 800)
        meteor.y = random.randint(0, 300)
        meteor.length = random.randint(10, 50)
        meteor.speed = random.uniform(5, 10)
        meteor.trail = []
"""
"""
# Cập nhật và vẽ sao chổi
for comet in comets:
    comet.update()
    comet.draw(screen)

    # Tạo sao chổi mới nếu nó bay ra khỏi màn hình
    if comet.x > 800 or comet.y > 600:
        comet.x = random.randint(-50, -10)  # Bắt đầu từ ngoài màn hình
        comet.y = random.randint(0, 300)
        comet.speed = random.uniform(4, 8)
        comet.trail = []
"""