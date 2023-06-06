import pygame
import random as rd

pygame.init()
# Screen Variables
width = 1600
height = 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("BOB")


# X wing properties
img_file = pygame.image.load('Xwing.png')
img_file.convert()
img_size = (width // 16, height // 9)
xwing = pygame.transform.rotate(pygame.transform.scale(img_file, img_size), 270)
position_rect = xwing.get_rect()
position_rect.center = (width // 8, height // 2)
enemyx_wing = pygame.transform.rotate(pygame.transform.scale(img_file, img_size), 90)
# Background
# space = pygame.image.load('space.png')
# space.convert()

# Sound FX
music = pygame.mixer.Sound('Dark Forest OST Ambient.mp3')
music.play()
laser_sound = pygame.mixer.Sound('Laser Gun - Sound Effect.mp3')

# Timer
obs_timer = pygame.USEREVENT + 1
spawn_time = 3000
pygame.time.set_timer(obs_timer, spawn_time)
# Variables
white = (255, 255, 255)
red = (255, 0, 0)
teal = (0, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
player_vel = 15
enemy_vel = 2
enemy_list = []
bullet_vel = 20
max_bullets = 4
bullets = []
bullet_list = []
enemy_bullets = []
FPS = 90
clock = pygame.time.Clock()
txt = pygame.font.Font(None, 50)
game_active = True


def handle_keys(rect):
    key = pygame.key.get_pressed()

    # if key[pygame.K_a] and rect.x > 0:
    #     rect.x -= player_vel
    # if key[pygame.K_d] and rect.x < width - img_size[0]:
    #     rect.x += player_vel
    if key[pygame.K_w] and rect.y > 0:
        rect.y -= player_vel
    if key[pygame.K_s] and rect.y < height - img_size[1]:
        rect.y += player_vel


def fire_bullets(bul):
    for i in bul:
        i.x += bullet_vel
        pygame.draw.rect(screen, red, i)
        if i[0] >= width + width/10:
            bul.remove(i)


def end_game():
    screen.fill(black)
    end_score = txt.render(f'Score: {current_time}', False, teal)
    end_score_rect = end_score.get_rect(center=(width//2, height//2))
    screen.blit(end_score, end_score_rect)
    pygame.display.flip()


def score():
    global current_time
    current_time = str(int(pygame.time.get_ticks()/100))
    score_surf = txt.render(current_time, False, teal)
    score_rect = score_surf.get_rect(topleft=(10, 10))
    screen.blit(score_surf, score_rect)


def enemy_spawn():
    global game_active
    global enemy_list
    for i in enemy_list:
        i.x -= enemy_vel
        screen.blit(enemyx_wing, i)
        if i[0] < 0 - img_size[0]:
            # enemy_list.remove(i)
            game_active = False
        for y in bullets:
            if i.colliderect(y):
                bullets.remove(y)
                enemy_list.remove(i)
        if i.colliderect(position_rect):
            game_active = False


# Game Start info
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and len(bullet_list) % 2 == 0: # and len(bullets) < max_bullets:
            bullet = pygame.Rect(position_rect.x + 50, position_rect.y + 3, 50, 2)
            bullets.append(bullet)
            bullet_list.append(bullet)
            laser_sound.play()
        elif event.type == pygame.MOUSEBUTTONDOWN and len(bullet_list) % 2 == 1: # and len(bullets) < max_bullets:
            bullet = pygame.Rect(position_rect.x + 50, position_rect.y + 95, 50, 2)
            bullets.append(bullet)
            bullet_list.append(bullet)
            laser_sound.play()
        if event.type == obs_timer:
            random_y = rd.randint(100, height - 100)
            enemy_rect = enemyx_wing.get_rect(center=(width + 100, random_y))
            enemy_list.append(enemy_rect)
            if enemy_vel < 20:
                enemy_vel *= 1.02
            print(f'Enemy Velocity: {enemy_vel}\nSpawn Time: {spawn_time}')
            if spawn_time > 600:
                spawn_time = int(spawn_time / 1.05)
                pygame.time.set_timer(obs_timer, spawn_time)

    if game_active:
        # Display Settings
        screen.fill(black)
        handle_keys(position_rect)
        screen.blit(xwing, position_rect)
        enemy_spawn()
        fire_bullets(bullets)
        score()
        pygame.display.flip()
        clock.tick(FPS)
    else:
        end_game()
# Loop End
