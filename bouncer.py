# python3 - Bouncer is 2D game where you bounce ball of a square to destroy other sqares

import pygame. time, random

# defining constants
WIDTH = 600
HEIGHT = 450
FPS = 60

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

# initialization of pygame, screen, clock, setting caption and stuff..
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bouncer')
running = True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (round(WIDTH / 2), 400)
        self.speedx = 0
    
    def update(self):
        self.speedx = 0
        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_LEFT]:
            self.speedx = -5
        if keypressed[pygame.K_RIGHT]:
            self.speedx = 5
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        self.rect.x += self.speedx

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 15))
        self.rect = self.image.get_rect()
        self.rect.x = round(x)
        self.rect.y = round(y)
        self.block_color = random.choice(enemies_types) 
        self.image.fill(self.block_color)
        if self.block_color == WHITE:
            self.lives = 1
        elif self.block_color == RED:
            self.lives = 2
        else:
            self.lives = 3 
    def update(self):
        if self.lives == 1:
            self.image.fill(WHITE)
        if self.lives == 2: 
            self.image.fill(RED)
        if self.lives == 3: 
            self.image.fill(BLUE)
        
class Ball(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((14, 14))
        self.image.fill(WHITE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, RED, (7, 7), 7)
        self.rect.center = (round(x), round(y))
        self.speedx = 3
        self.speedy = 3
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

def game_loop():
    # defining what variables are global
    global running

    # all sprites will be added to the group 
    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    ball = Ball(random.randint(player.rect.x, player.rect.x + player.rect.width / 2), random.randint(300, player.rect.y - 20))
    all_sprites.add(ball)
    enemies = pygame.sprite.Group()

    for j in range (0, 12):
        for i in range(0, 11):
            # let there be 2 pixels space between enemies
            # enemies start at x = 15, and y = 20
            enemies.add(Enemy(15 + i * 52, 20 + 17 * j))

    all_sprites.add(enemies)

    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # if ball goes bellow bottom edge you will
        if ball.rect.top > HEIGHT:
            running = False
        # player collison with the ball
        if player.rect.colliderect(ball.rect):
            ball.speedy *= -1 
        # ball collision with the enemies
        hits = pygame.sprite.spritecollide(ball, enemies, False, pygame.sprite.collide_circle)
        for hit in hits:
            if hit.lives == 1: 
                hit.kill()
            else:
                hit.lives -= 1
                
            ball.speedy *= -1
        #update
        all_sprites.update()
        #draw/render
        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()
    
enemies_types = [WHITE, RED, BLUE]
game_loop()
pygame.quit()