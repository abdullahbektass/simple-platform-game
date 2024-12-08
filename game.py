import pgzrun
import random
from math import sin, cos
from pygame import Rect
import pygame

# Game settings
WIDTH = 800
HEIGHT = 600
MUSIC_ENABLED = False
score = 0

# Background images
bg_empty = pygame.image.load("assets/images/empty_bg.png")
bg_playing = pygame.image.load("assets/images/bg_playing.png")

# Scrolling background variables
bg_playing_x1 = 0
bg_playing_x2 = WIDTH
bg_scroll_speed = 4

# Sounds
pygame.mixer.init()  # Initialize the mixer
bg_music = pygame.mixer.Sound("assets/sounds/bg.wav")
bg_music.set_volume(0.5)
jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav")

# Helper function to load sprites from a sprite sheet
def load_sprites_from_sheet(sheet_path, frame_width, frame_height):
    sheet = pygame.image.load(sheet_path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()

    if sheet_width % frame_width != 0 or sheet_height % frame_height != 0:
        raise ValueError("Sprite sheet dimensions are not evenly divisible by frame size")

    sprites = []
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            rect = pygame.Rect(x, y, frame_width, frame_height)
            sprite = sheet.subsurface(rect)
            sprites.append(sprite)
    return sprites

# Load sprite sheets and define animations
frame_width = 96
frame_height = 128
hero_sprites = load_sprites_from_sheet("assets/images/hero_sheet.png", frame_width, frame_height)
danger_sprites = load_sprites_from_sheet("assets/images/danger_sheet.png", frame_width, frame_height)

# Define specific animation frames based on sprite sheet layout
hero_idle = hero_sprites[0:2]  # First two frames for idle
hero_jump = hero_sprites[7:9]  # Frames 7 and 8 for jumping
danger_run = danger_sprites[0:2]  # First and second frames for danger running

# Classes
class AnimatedSprite:
    def __init__(self, images, x, y, scale=1):
        self.images = [pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) for img in images]
        self.index = 0
        self.timer = 0
        self.x = x
        self.y = y
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()

    def animate(self):
        self.timer += 1
        if self.timer >= 10:
            self.index = (self.index + 1) % len(self.images)
            self.timer = 0

    def draw(self):
        screen.blit(self.images[self.index], (self.x, self.y))

class Hero(AnimatedSprite):
    def __init__(self, idle_images, jump_images, x, y):
        super().__init__(idle_images, x, y)
        self.idle_images = idle_images
        self.jump_images = jump_images
        self.vx = 0
        self.vy = 0
        self.grounded = False

    def update(self):
        self.vy += 0.5  # Gravity
        self.x += self.vx
        self.y += self.vy

        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.vy = 0
            self.grounded = True

        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

        # Change animation based on state
        if not self.grounded:
            self.images = self.jump_images  # Jumping animation
        else:
            self.images = self.idle_images  # Idle animation

        self.animate()

    def jump(self):
        if self.grounded:
            jump_sound.play()
            self.vy = -10
            self.grounded = False

    def move_left(self):
        self.vx = -5

    def move_right(self):
        self.vx = 5

    def stop(self):
        self.vx = 0

class Danger(AnimatedSprite):
    def __init__(self, images, x, y):
        super().__init__(images, x, y, scale=0.5)  # Reduce size by 50%
        self.vx = -4  # Increased speed
        self.passed = False  # Track if hero has jumped over

    def update(self):
        self.x += self.vx
        self.animate()

# Instances
hero = Hero(hero_idle, hero_jump, 100, HEIGHT - 150)
dangers = []
next_danger_spawn_time = random.randint(180, 300)  # Increased time interval (3-5 seconds at 60 FPS)
current_frame = 0

# Game State
game_state = "menu"

def spawn_danger():
    x = WIDTH + 50
    y = HEIGHT - 64
    dangers.append(Danger(danger_run, x, y))

def reset_game():
    global hero, dangers, next_danger_spawn_time, current_frame, game_state, score, bg_playing_x1, bg_playing_x2
    hero = Hero(hero_idle, hero_jump, 100, HEIGHT - 150)
    dangers = []
    next_danger_spawn_time = random.randint(180, 300)
    current_frame = 0
    score = 0
    bg_playing_x1 = 0
    bg_playing_x2 = WIDTH
    game_state = "playing"
    bg_music.stop()
    bg_music.play(-1)

def draw():
    screen.clear()
    if game_state == "menu" or game_state == "gameover":
        screen.blit(bg_empty, (0, 0))
        draw_menu_or_gameover()
    elif game_state == "playing":
        draw_playing_background()
        draw_game()

def update():
    global game_state, next_danger_spawn_time, current_frame
    if game_state == "playing":
        update_playing_background()
        hero.update()
        for danger in dangers[:]:
            danger.update()
            if not danger.passed and hero.x > danger.x + danger.width:
                global score
                score += 1
                danger.passed = True
            if danger.x + danger.width < 0:
                dangers.remove(danger)

        check_collisions()

        # Spawn danger at random intervals
        current_frame += 1
        if current_frame >= next_danger_spawn_time:
            spawn_danger()
            current_frame = 0
            next_danger_spawn_time = random.randint(180, 300)

def draw_menu_or_gameover():
    if game_state == "menu":
        screen.draw.text("Main Menu", center=(WIDTH // 2, 100), fontsize=50, color="brown")
        screen.draw.text("1 or SPACE: Start Game", center=(WIDTH // 2, 200), fontsize=30, color="brown")
        screen.draw.text("2: Toggle Music", center=(WIDTH // 2, 250), fontsize=30, color="brown")
        screen.draw.text("3: Exit", center=(WIDTH // 2, 300), fontsize=30, color="brown")
    elif game_state == "gameover":
        screen.draw.text("Game Over! Press SPACE to Restart", center=(WIDTH // 2, 100), fontsize=50, color="brown")
        screen.draw.text(f"Your Score: {score}", center=(WIDTH // 2, 200), fontsize=40, color="brown")

def draw_playing_background():
    screen.blit(bg_playing, (bg_playing_x1, 0))
    screen.blit(bg_playing, (bg_playing_x2, 0))

def update_playing_background():
    global bg_playing_x1, bg_playing_x2
    bg_playing_x1 -= bg_scroll_speed
    bg_playing_x2 -= bg_scroll_speed

    if bg_playing_x1 + WIDTH <= 0:
        bg_playing_x1 = bg_playing_x2 + WIDTH
    if bg_playing_x2 + WIDTH <= 0:
        bg_playing_x2 = bg_playing_x1 + WIDTH

def draw_game():
    hero.draw()
    for danger in dangers:
        danger.draw()
    screen.draw.text(f"Score: {score}", center=(WIDTH // 2, 50), fontsize=40, color="brown")

def check_collisions():
    global game_state
    for danger in dangers:
        if Rect(hero.x, hero.y, hero.width, hero.height).colliderect(Rect(danger.x, danger.y, danger.width, danger.height)):
            game_state = "gameover"
            bg_music.stop()

# Music toggle
def toggle_music():
    global MUSIC_ENABLED
    if MUSIC_ENABLED:
        bg_music.stop()
    else:
        bg_music.play(-1)
    MUSIC_ENABLED = not MUSIC_ENABLED

# Event handling
def on_key_down(key):
    global game_state
    if game_state == "menu":
        if key == keys.K_1 or key == keys.SPACE:
            reset_game()
        elif key == keys.K_2:
            toggle_music()
        elif key == keys.K_3:
            exit()
    elif game_state == "playing":
        if key == keys.SPACE:
            hero.jump()
        elif key == keys.LEFT:
            hero.move_left()
        elif key == keys.RIGHT:
            hero.move_right()
    elif game_state == "gameover":
        if key == keys.SPACE:
            reset_game()

def on_key_up(key):
    if game_state == "playing":
        if key in (keys.LEFT, keys.RIGHT):
            hero.stop()

pgzrun.go()
