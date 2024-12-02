import pygame

class Title:
    def __init__(self, text, font, color, position, glow=False, glow_color=None, glow_radius=10):
        """
        Khởi tạo tiêu đề.
        :param text: Nội dung tiêu đề.
        :param font: Đối tượng font của pygame.
        :param color: Màu chữ tiêu đề (RGB tuple).
        :param position: Vị trí trung tâm của tiêu đề (tuple: (x, y)).
        :param glow: Hiệu ứng phát sáng (True/False).
        :param glow_color: Màu ánh sáng (RGB tuple).
        :param glow_radius: Bán kính hiệu ứng phát sáng.
        """
        self.text = text
        self.font = font
        self.color = color
        self.position = position
        self.glow = glow
        self.glow_color = glow_color if glow_color else color
        self.glow_radius = glow_radius

    def draw(self, screen):
        """
        Vẽ tiêu đề lên màn hình với hiệu ứng đổ bóng và chữ sáng đẹp.
        :param screen: Màn hình pygame.
        """
        # Tạo hiệu ứng đổ bóng
        shadow_offset = (3, 3)  # Độ lệch của bóng
        shadow_color = (50, 50, 50)  # Màu bóng tối
        shadow_surface = self.font.render(self.text, True, shadow_color)
        shadow_rect = shadow_surface.get_rect(center=(self.position[0] + shadow_offset[0],
                                                    self.position[1] + shadow_offset[1]))
        screen.blit(shadow_surface, shadow_rect)

        # Vẽ tiêu đề chính
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=self.position)
        screen.blit(text_surface, text_rect)