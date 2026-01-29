import pygame, asyncio, random
import math

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
PLAYER_HEIGHT = 32
PLAYER_WIDTH = 32
scroll = 0
FPS = 60
game_state = "menu"

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Plane Game")

player_x = SCREEN_WIDTH / 2
player_y = 725
velocity = 1
grass_bg = pygame.image.load("./Assets/Tiles/Grass/BG/Grass_BG.png")
dirt_bg = pygame.image.load("./Assets/Tiles/Dirt/BG/DirtBg.png")
bg_width = 600
bg_height = grass_bg.get_height()
play_button = pygame.image.load("Assets/Ui/Menu/PlayButton.png")
play_button_scaled = pygame.transform.scale(play_button, (250, 250/3))
play_button_rect = play_button_scaled.get_rect()
play_button_hover = pygame.transform.scale(play_button, (300, 300/3))
play_button_hover_rect = play_button_hover.get_rect()
play_button_rect.topleft = (SCREEN_WIDTH / 2 - play_button_rect.width / 2, SCREEN_HEIGHT / 4 - play_button_rect.height / 2)
play_button_hover_rect.topleft = (SCREEN_WIDTH / 2 - play_button_hover_rect.width / 2, SCREEN_HEIGHT / 4 - play_button_hover_rect.height / 2)
setting_button = pygame.image.load("Assets/Ui/Menu/SettingsButton.png")
setting_button_scaled = pygame.transform.scale(setting_button, (250, 250/3))
setting_button_rect = setting_button_scaled.get_rect()
setting_button_hover = pygame.transform.scale(setting_button, (300, 300/3))
setting_button_hover_rect = setting_button_hover.get_rect()
setting_button_rect.topleft = (SCREEN_WIDTH / 2 - setting_button_rect / 2)

player = pygame.image.load("Assets/Ships/ship_0000.png")
player_rect = player.get_rect()
player_rect.topleft = (player_x, player_y)

biome = 1
loaded_obstacles = []

dirt_obstacles = [pygame.transform.scale(pygame.image.load(f"Assets/Tiles/Dirt/obstacles/dirt_obstacle_{obstacle}.png"), (64, 64)) for obstacle in range(1,6)]
grass_obstacles = [pygame.transform.scale(pygame.image.load(f"Assets/Tiles/Grass/Obstacles/grass_obstacle_{obstacle}.png"), (64, 64)) for obstacle in range(1,6)]

tiles = math.ceil((SCREEN_HEIGHT / bg_height)) + 1

async def main():
    global SCREEN_HEIGHT, play_button_rect, play_button, play_button_scaled, SCREEN_WIDTH, game_state,  WHITE, SKY_BLUE, scroll, PLAYER_HEIGHT, PLAYER_WIDTH, screen, clock, running, player_x, player_y, velocity, player, player_rect, biome, dirt_obstacles, grass_obstacles, loaded_obstacles, grass_bg, dirt_bg, bg_width, bg_height

    last_obstacle_spawn_time = pygame.time.get_ticks()

    while running:   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if game_state == "menu":
            screen.fill(SKY_BLUE)
            if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(play_button_hover, play_button_hover_rect)
            else:
                screen.blit(play_button_scaled, play_button_rect)
            if setting_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(setting_button_hover, setting_button_hover_rect)
            else:
                screen.blit(setting_button_scaled, setting_button_rect)
        if game_state == "playing":
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

            for i in range(0, tiles):
                if biome == 1:
                    screen.blit(grass_bg, (0, (i - 1) * bg_height + scroll))
                elif biome == 2:
                    screen.blit(dirt_bg, (0, (i -1) * bg_height +scroll))


            scroll += 5

            if scroll >= bg_height:
                scroll = 0

            for obstacle in loaded_obstacles:
                if player_rect.colliderect(obstacle[1]):
                    print("Hit!")

            screen.blit(player, player_rect)
            for obstacle in loaded_obstacles:
                screen.blit(obstacle[0], obstacle[1])

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()
asyncio.run(main())