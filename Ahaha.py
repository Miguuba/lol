import pygame
import os
from random import randint
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 10
BULLET_VEL = 30
MAX_BULLETS = 1000
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
POWERUP_HIT_RED = pygame.USEREVENT + 3
POWERUP_HIT_YELLOW = pygame.USEREVENT + 4


YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

COIN_IMAGE_RED = pygame.image.load(
    os.path.join('Assets', 'star.png'))
COIN_RED = pygame.transform.scale(
    COIN_IMAGE_RED, (30,30))

COIN_IMAGE_YELLOW = pygame.image.load(
    os.path.join('Assets', 'star.png'))
COIN_YELLOW = pygame.transform.scale(
    COIN_IMAGE_RED, (30, 30))

EXPLOSION_IMAGE = pygame.image.load(
    os.path.join("Assets","exp.png"))

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, coin_red, coin_yellow):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    WIN.blit(COIN_RED, (coin_red.x,coin_red.y))
    WIN.blit(COIN_YELLOW, (coin_yellow.x, coin_yellow.y))

    pygame.display.update()

def explosion(x,y):
    WIN.blit(EXPLOSION_IMAGE, (x-10, y-10))
    pygame.display.update()
    pygame.time.delay(30)

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

YELLOW_POWER = False
RED_POWER = False

def handle_powerup_red(coin_red, red):
    #if yellow touches power up, YELLOW_POWER == True

    if red.colliderect(coin_red):

        pygame.event.post(pygame.event.Event(POWERUP_HIT_RED))
  
        COIN_RED.set_alpha(0)
        #pygame.display.upgarde()
    #if red touches power up, RED_POWER == True
def handle_powerup_yellow(coin_yellow, yellow):
    if yellow.colliderect(coin_yellow):
        pygame.event.post(pygame.event.Event(POWERUP_HIT_YELLOW))
      
        print("yellow")
        COIN_YELLOW.set_alpha(0)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    coin_yellow = pygame.Rect(randint(20,430),randint(20,430), 30, 30)
    coin_red = pygame.Rect(randint(470, 880), randint(20, 430), 30, 30)

    red_bullets = []
    yellow_bullets = []


    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True

    power_red = False
    power_yellow = False

    COIN_RED.set_alpha(255)
    COIN_YELLOW.set_alpha(255)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if  event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                      

                
                if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(
                            red.x, red.y + red.height//2 - 2, 10, 5)
                        red_bullets.append(bullet)


                       #BULLET_FIRE_SOUND.play()

            

            
            if event.type == RED_HIT:# and RED_POWER == False:
                if power_red == True:
                    red_health -= 2
                else:
                    red_health -= 1

                explosion(red.x, red.y)
                #BULLET_HIT_SOUND.play()
            
            # if event.type == RED_HIT and RED_POWER == True:
            #     red_health -= 2
            #     #BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT: # and YELLOW_POWER == False:
                if power_yellow == True:
                    yellow_health -= 2
                else:
                    yellow_health -= 1
                explosion(yellow.x,yellow.y)
                #BULLET_HIT_SOUND.play()
            
            if event.type == POWERUP_HIT_RED:
                power_yellow = True
            
            if event.type == POWERUP_HIT_YELLOW:
                power_red = True



        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        handle_powerup_red(coin_red, red)
        handle_powerup_yellow(coin_yellow,yellow)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health, coin_red, coin_yellow)

        
        

    main()


if __name__ == "__main__":
    main()