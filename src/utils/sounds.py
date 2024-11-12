import pygame

# Khởi tạo mixer
pygame.mixer.init()

# Đường dẫn âm thanh
BACKGROUND_MUSIC_PATH = "../assets/sounds/background_sound.wav"

# Biến quản lý âm lượng
background_volume = 0.5
effect_volume = 0.5

# Hàm để quản lý âm thanh
def load_background_sounds():
    pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
    pygame.mixer.music.set_volume(background_volume)

def load_effect_sounds(EFFECT_SOUND_PATH):
    effect_sound = pygame.mixer.Sound(EFFECT_SOUND_PATH)
    effect_sound.set_volume(effect_volume)
    return effect_sound

def play_background_music():
    pygame.mixer.music.play(-1)  # Phát nhạc nền lặp lại

def stop_background_music():
    pygame.mixer.music.stop()

def play_effect_sound(EFFECT_SOUND_PATH):
    effect_sound = load_effect_sounds(EFFECT_SOUND_PATH)
    effect_sound.play()  # Phát âm thanh hiệu ứng

def set_background_volume(volume):
    global background_volume
    background_volume = volume
    pygame.mixer.music.set_volume(volume)

def set_effect_volume(effect_sound, volume):
    global effect_volume
    effect_volume = volume
    effect_sound.set_volume(volume)
