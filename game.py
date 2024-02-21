import pygame
import os
pygame.font.init()
pygame.mixer.init()

width, height = 900, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Game")

white = (255, 255, 255)
black = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

VEL = 5
BULLET_VEL = 12
MAX_BULLETS = 3
FPS = 60
BORDER = pygame.Rect(width/2, 0, 10, height)

BULLETHITSOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLETFIRESOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTHFONT = pygame.font.SysFont('comicsans', 40)
winnerFont = pygame.font.SysFont('comicsans', 100)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

spaceshipWidth, spaceshipHeight = 55, 40
yellowSpaceshipImage = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
yellowSpaceship = pygame.transform.rotate(pygame.transform.scale(yellowSpaceshipImage, (spaceshipWidth, spaceshipHeight)), 90)
redSpaceshipImage = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
redSpaceship = pygame.transform.rotate(pygame.transform.scale(redSpaceshipImage, (spaceshipWidth, spaceshipHeight)), 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (width, height))

def yellowMovement(keys, yellow):
    if keys[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if keys[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys[pygame.K_s] and yellow.y + VEL + yellow.height < height-15:
        yellow.y += VEL

def redMovement(keys, red):
    if keys[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys[pygame.K_RIGHT] and red.x + VEL + red.width < width:
        red.x += VEL
    if keys[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys[pygame.K_DOWN] and red.y + VEL + red.height < height-15:
        red.y += VEL

def bulletHandler(yellowBullets, redBullets, yellow, red):
    for b in yellowBullets:
        b.x += BULLET_VEL
        if red.colliderect(b):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellowBullets.remove(b)
            print('red collide')
        if b.x > width:
            yellowBullets.remove(b)

    for b in redBullets:
        b.x -= BULLET_VEL
        if yellow.colliderect(b):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            redBullets.remove(b)
            print('yellow collide')
        if b.x < 0:
            redBullets.remove(b)

def draw(red, yellow, rBullets, yBullets, redHealth, yellowHealth):
    win.blit(SPACE, (0, 0))
    pygame.draw.rect(win, black, BORDER)

    redHealthText = HEALTHFONT.render("Health: %s" % (redHealth), 1, white)
    yellowHealthText = HEALTHFONT.render("Health: %s" % (yellowHealth), 1, white)
    win.blit(redHealthText, (width - redHealthText.get_width() - 10, 10))
    win.blit(yellowHealthText, (10, 10))
    
    win.blit(yellowSpaceship, (yellow.x, yellow.y))
    win.blit(redSpaceship, (red.x, red.y))

    for b in rBullets:
        pygame.draw.rect(win, RED, b)

    for b in yBullets:
        pygame.draw.rect(win, YELLOW, b)
        
    pygame.display.update()

def draw_winner(text):
    drawText = winnerFont.render(text, 1, white)
    win.blit(drawText, (width/2 - drawText.get_width()/2, drawText.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)
    
def main():
    red = pygame.Rect(700, 300, spaceshipWidth, spaceshipHeight)
    yellow = pygame.Rect(100, 300, spaceshipWidth, spaceshipHeight)

    redBullets, yellowBullets = [], []
    redHealth, yellowHealth = 10, 10
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LMETA and len(yellowBullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2 -2.5, 10, 5)
                    yellowBullets.append(bullet)
                    BULLETFIRESOUND.play()

                if e.key == pygame.K_RMETA and len(redBullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height/2 -2.5, 10, 5)
                    redBullets.append(bullet)
                    BULLETFIRESOUND.play()

            if e.type == RED_HIT:
                redHealth -= 1
                BULLETHITSOUND.play()

            if e.type == YELLOW_HIT:
                yellowHealth -= 1
                BULLETHITSOUND.play()

        winnerText = ''
        if redHealth <= 0:
            winnerText = 'Yellow wins!'

        if yellowHealth <= 0:
            winnerText = 'Red wins!'

        if winnerText != '':
            draw_winner(winnerText)
            break

        keysPressed = pygame.key.get_pressed()
        yellowMovement(keysPressed, yellow)
        redMovement(keysPressed, red)

        bulletHandler(yellowBullets, redBullets, yellow, red)
        
        draw(red, yellow, redBullets, yellowBullets, redHealth, yellowHealth)
    pygame.quit()

main()
