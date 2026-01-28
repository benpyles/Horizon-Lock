import pygame, asyncio, random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
PLAYER_HEIGHT = 32
PLAYER_WIDTH = 32

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

player_x = SCREEN_WIDTH / 2
player_y = 725
velocity = 1

player = pygame.image.load("kenney_pixel-shmup/Ships/ship_0000.png")
player_rect = player.get_rect()
player_rect.topleft = (player_x, player_y)

biome = 1
loaded_obstacles = []

dirt_obstacles = [pygame.transform.scale(pygame.image.load(f"kenney_pixel-shmup/Tiles/Dirt/obstacles/dirt_obstacle_{obstacle}.png"), (64, 64)) for obstacle in range(1,6)]
grass_obstacles = [pygame.transform.scale(pygame.image.load(f"kenney_pixel-shmup/Tiles/Grass/Obstacles/grass_obstacle_{obstacle}.png"), (64, 64)) for obstacle in range(1,6)]

async def main():
    global SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, SKY_BLUE, PLAYER_HEIGHT, PLAYER_WIDTH, screen, clock, running, player_x, player_y, velocity, player, player_rect, biome, dirt_obstacles, grass_obstacles, loaded_obstacles

    last_obstacle_spawn_time = pygame.time.get_ticks()

    while running:   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(SKY_BLUE)
        current_time = pygame.time.get_ticks()

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

        for obstacle in loaded_obstacles:
            obstacle[3] += 5
            obstacle[1].topleft = (obstacle[2], int(obstacle[3]))

        loaded_obstacles = [obs for obs in loaded_obstacles if obs[3] < 850]

        biome_change_chance = random.randint(1, 1000)
        if biome_change_chance == 500:
            biome = random.randint(1,2)

        if current_time - last_obstacle_spawn_time > 500:
            if biome == 1:
                image = random.choice(grass_obstacles)
            else:
                image = random.choice(dirt_obstacles)
            
            spawn_x = random.randint(0, SCREEN_WIDTH - 64)
            spawn_y = -70
            
            rect = image.get_rect()
            rect.topleft = (spawn_x, spawn_y)
            
            loaded_obstacles.append([image, rect, spawn_x, spawn_y])
            
            last_obstacle_spawn_time = current_time

        if player_x < 0:
            player_x = 0
        if player_x + PLAYER_WIDTH > SCREEN_WIDTH:
            player_x = SCREEN_WIDTH - PLAYER_WIDTH
        if player_y < 0:
            player_y = 0
        if player_y + PLAYER_HEIGHT > SCREEN_HEIGHT:
            player_y = SCREEN_HEIGHT - PLAYER_HEIGHT

        player_rect.topleft = (player_x, player_y)

        for obstacle in loaded_obstacles:
            if player_rect.colliderect(obstacle[1]):
                print("Hit!")

        screen.blit(player, player_rect)
        for obstacle in loaded_obstacles:
            screen.blit(obstacle[0], obstacle[1])
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
asyncio.run(main())