#importing pygame
import pygame

#Set up constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)

#Setup pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

#Key variables
player_x = 75
player_y = SCREEN_HEIGHT / 2

velocity = 1

#Load Assets and set character
player = pygame.image.load("kenney_pixel-shmup/Ships/ship_0000.png")
player_rect = player.get_rect()
player = pygame.transform.rotate(player, 90)
player_rect.topleft = (player_x, player_y)

#Game loop
while running:   
    #Handles quiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Fill screen to wipe the last frame
    screen.fill(SKY_BLUE)

    #Player movement
    keypress = pygame.key.get_pressed()
    if keypress[pygame.K_UP]:
        player_y -= velocity
        velocity += 0.5
    elif keypress[pygame.K_DOWN]:
        player_y += velocity
        velocity += 0.5
    else:
        velocity = 1

    #Player Boundarys
    if player_y >= 600:
        player_y = 600
    elif player_y <= 0:
        player_y = 0

    #Rendering
    player_rect.topleft = (player_x, player_y)
    screen.blit(player, player_rect)
    pygame.display.flip()

    clock.tick(60) #limit fps to 60

pygame.quit()