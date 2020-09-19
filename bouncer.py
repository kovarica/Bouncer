# python3 - Bouncer is 2D game where you bounce ball of a square to destroy other sqares
# # Art by Kenney.nl / (www.kenney.nl)
import pygame. time, random
from os import path
#find path to directories
font_dir = path.join(path.dirname(__file__), 'fonts')
img_dir = path.join(path.dirname(__file__), 'imgs')
# defining constants
WIDTH = 400
HEIGHT = 550
FPS = 60
# 4000 ticks is 4 seconds
POWERUP_TIME = 4000
# defining colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255);
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHTSLATEGRAY = (119,136,153)
DARKGRAY = (169,169,169)
LIGHTSTEELBLUE = (176, 196, 222)
LIGHTSEAGREEN = (32,178,170)
CADETBLUE = (95,158,160)
MORON = (128, 0, 0)
DARKRED = (139, 0, 0)
KHAKI = (238,232,170)
SILVER = (192,192,192)
DIMGRAY = (105,105,105)
DARKBLUE = (0,0,139)
MIDNIGHTBLUE = (25,25,112)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = paddle
        self.image.set_colorkey(BLACK)
        # self.image = pygame.Surface((60, 10))
        # self.image.fill(DARKGRAY)
        self.rect = self.image.get_rect()
        self.rect.center = (round(WIDTH / 2), 540)
        self.speedx = 0
        self.powerup_started = False
        # zero is just initial number
        self.powerup_start = 0

    def powerup(self):
        self.powerup_start = pygame.time.get_ticks()
        self.powerup_started = True

    def update(self):
        self.speedx = 0
        keypressed = pygame.key.get_pressed()
        if self.powerup_started:
            if keypressed[pygame.K_LEFT]:
                self.speedx = -8
            if keypressed[pygame.K_RIGHT]:
                self.speedx = 8
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
        else:
            if keypressed[pygame.K_LEFT]:
                self.speedx = -5
            if keypressed[pygame.K_RIGHT]:
                self.speedx = 5
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH

        self.rect.x += self.speedx
        if pygame.time.get_ticks() - self.powerup_start > POWERUP_TIME:
            self.powerup_started = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.block_lives = random.choice(enemies_types)
        # self.block_color = WHITE
        # self.image.fill(self.block_color)
        if self.block_lives == 1:
            self.image = gray_brick
        elif self.block_lives == 2:
            self.image = blue_brick
        else:
            self.image = yellow_brick

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = round(x)
        self.rect.y = round(y)


    def update(self):
        if self.block_lives == 1:
            self.image = gray_brick
        if self.block_lives == 2:
            self.image = blue_brick

class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = ball
        self.image = pygame.Surface((14, 14))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, YELLOW, (7, 7), 7)
        self.rect.center = (round(x), round(y))
        self.speedx = 4
        self.speedy = 4
        self.radius = 7
        pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius, 2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top <= 0:
            self.speedy *= -1
        if self.rect.right > WIDTH:
            self.speedx *= -1
        if self.rect.left < 0:
            self.speedx *= -1

class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = powerup
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.powup_speedy = 3

    def update(self):
        self.rect.y += self.powup_speedy
        if self.rect.top > HEIGHT:
            self.kill()

def display_text_arbitraryfont(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (round(x), round(y))
    screen.blit(text_surface, text_rect)

def display_enemies(all_sprites, enemies):
    for j in range (0, 12):
        for i in range(0, 7):
            # let there be 2 pixels space between enemies
            # enemies start at x = 1, and y = 2
            enemies.add(Enemy(1 + i * 57, 2 + 30 * j))

    all_sprites.add(enemies)

def game_outro(score):
    # this will appear when you die
    global game_over
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game_loop()

        screen.fill(CADETBLUE)
        display_text_arbitraryfont('sadly you died', ka1_font2, DARKRED, WIDTH/2 , 100)
        display_text_arbitraryfont('your score was ' + str(score), ka1_font2, MORON, WIDTH/2 - 5, 200)
        display_text_arbitraryfont('press SPACE key to start again', ka1_font3, DARKBLUE, WIDTH/2, 370)


        pygame.display.flip()

def game_loop():
    # defining what variables are global
    global running
    global score
    global game_over
    # all sprites will be added to the group
    score = 0
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    ball = Ball(random.randint(player.rect.x, player.rect.x + player.rect.width / 2), random.randint(400, player.rect.y - 20))
    all_sprites.add(ball)
    display_enemies(all_sprites, enemies)

    # main loop
    while running:
        clock.tick(FPS)
        # processing events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # if ball goes bellow bottom edge you will
        if ball.rect.top > HEIGHT:
            game_over = True
            game_outro(score)

        # player collison with the ball
        if player.rect.colliderect(ball.rect):
            ball.speedy *= -1
        if player.rect.contains(ball.rect):
            ball.speedy *= -1
        # ball collision with the enemies
        # hits = pygame.sprite.spritecollide(ball, enemies, False, pygame.sprite.collide_circle)
        hits = pygame.sprite.spritecollide(ball, enemies, False)
        for hit in hits:
            if hit.block_lives == 1:
                if random.random() > 0.98:
                    powup = Powerup(hit.rect.center)
                    all_sprites.add(powup)
                    powerups.add(powup)
                hit.kill()
            else:
                hit.block_lives -= 1
            score += 1
            ball.speedy *= -1

        # ball collision with powerup
        hits = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.powerup()
        # empty sprite group is considered false
        if not enemies and ball.rect.top > 360:
            display_enemies(all_sprites, enemies)
        #update
        all_sprites.update()
        #draw/render
        screen.fill(MIDNIGHTBLUE)
        display_text_arbitraryfont('SCORE ' + str(score), ka1_font, DIMGRAY, 200, 420)
        all_sprites.draw(screen)
        pygame.display.flip()

# initialization of pygame, screen, clock, setting caption and stuff..
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bouncer')
# loading fonts
ka1_font = pygame.font.Font(path.join(font_dir, 'ka1.ttf'), 50)
# same font different size
ka1_font2 = pygame.font.Font(path.join(font_dir, 'ka1.ttf'), 28)
ka1_font3 = pygame.font.Font(path.join(font_dir, 'ka1.ttf'), 15)
# loading images
paddle = pygame.image.load(path.join(img_dir, 'paddleBlu.png')).convert()
blue_brick = pygame.image.load(path.join(img_dir,'element_blue_rectangle_glossy.png')).convert()
yellow_brick = pygame.image.load(path.join(img_dir, 'element_yellow_rectangle_glossy.png')).convert()
gray_brick = pygame.image.load(path.join(img_dir, 'element_grey_rectangle_glossy.png')).convert()
powerup = pygame.image.load(path.join(img_dir, 'powerupYellow_bolt.png')).convert()
# 1, 2, 3 coresponds to brick lives
enemies_imgs = [blue_brick, yellow_brick, gray_brick]
enemies_types = [1, 2, 3]
#global variables of very importance
score = 0
running = True
game_over = False

game_loop()
pygame.quit()
