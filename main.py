#importing pygame
import pygame, asyncio

#Set up constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
PLAYER_HEIGHT = 32
PLAYER_WIDTH = 32

#Setup pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

#Key variables
player_x = SCREEN_WIDTH / 2
player_y = 725
velocity = 1

#Load Assets and set character
player = pygame.image.load("kenney_pixel-shmup/Ships/ship_0000.png")
player_rect = player.get_rect()
#player = pygame.transform.rotate(player, 90)
player_rect.topleft = (player_x, player_y)

async def main():
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
        if keypress[pygame.K_LEFT] and keypress[pygame.K_RIGHT]:
            velocity = 1
        if keypress[pygame.K_LEFT]:
            player_x -= velocity
            velocity += 0.15
            if velocity > 9:
                velocity = 9

        elif keypress[pygame.K_RIGHT]:
            player_x += velocity
            velocity += 0.15
            if velocity > 9:
                velocity = 9

        else:
            velocity = 1

        #Player Boundarys
        if player_x < 0:
            player_x = 0
        if player_x + PLAYER_WIDTH > SCREEN_WIDTH:
            player_x = SCREEN_WIDTH - PLAYER_WIDTH
        if player_y < 0:
            player_y = 0
        if player_y + PLAYER_HEIGHT > SCREEN_HEIGHT:
            player_y = SCREEN_HEIGHT - PLAYER_HEIGHT

        #Rendering
        player_rect.topleft = (player_x, player_y)
        screen.blit(player, player_rect)
        pygame.display.flip()

        clock.tick(60) #limit fps to 60
        await asyncio.sleep(0)

    pygame.quit()
asyncio.run(main())    