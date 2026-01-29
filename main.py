import pygame, asyncio, random
import math

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
SKY_BLUE = (224, 251, 252)
PLAYER_HEIGHT = 32
PLAYER_WIDTH = 32
scroll = 0
FPS = 60
game_state = "menu"
menu_scroll = 0

pygame.mixer.pre_init(44100, -16, 2, 512)
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

#Ui loading
button_gap = 20
setting_button = pygame.image.load("Assets/Ui/Menu/SettingsButton.png")
setting_button_scaled = pygame.transform.scale(setting_button, (250, 3750/67))
setting_button_rect = setting_button_scaled.get_rect()
setting_button_hover = pygame.transform.scale(pygame.image.load("Assets/Ui/Menu/SettingsButtonHover.png"), (250, 3750/67))
setting_button_hover_rect = setting_button_hover.get_rect()
setting_button_rect.topleft = (SCREEN_WIDTH / 2 - setting_button_rect.width / 2, SCREEN_HEIGHT / 2 - setting_button_rect.height)
setting_button_hover_rect.topleft = (SCREEN_WIDTH / 2 - setting_button_hover_rect.width / 2, SCREEN_HEIGHT / 2 - setting_button_hover_rect.height)
play_button = pygame.image.load("Assets/Ui/Menu/PlayButton.png")
play_button_scaled = pygame.transform.scale(play_button, (250, 3750/67))
play_button_rect = play_button_scaled.get_rect()
play_button_hover = pygame.transform.scale(pygame.image.load("Assets/Ui/Menu/PlayButtonHover.png"), (250, 3750/67))
play_button_hover_rect = play_button_hover.get_rect()
play_button_rect.topleft = (SCREEN_WIDTH / 2 - play_button_rect.width / 2, setting_button_rect.y - button_gap - play_button_rect.height)
play_button_hover_rect.topleft = (SCREEN_WIDTH / 2 - play_button_hover_rect.width / 2, setting_button_rect.y - button_gap - play_button_rect.height)
achievements_button = pygame.image.load("Assets/Ui/Menu/AchievementsButton.png")
achievements_button_scaled = pygame.transform.scale(achievements_button, (250, 3750/67))
achievements_button_rect = setting_button_scaled.get_rect()
achievements_button_hover = pygame.transform.scale(pygame.image.load("Assets/Ui/Menu/AchievementsButtonHover.png"), (250, 3750/67))
achievements_button_hover_rect = setting_button_hover.get_rect()
achievements_button_rect.topleft = (SCREEN_WIDTH / 2 - achievements_button_rect.width / 2, setting_button_rect.y + button_gap + achievements_button_rect.height)
achievements_button_hover_rect.topleft = (SCREEN_WIDTH / 2 - achievements_button_hover_rect.width / 2, setting_button_rect.y + button_gap + achievements_button_rect.height)
cloud = pygame.image.load("Assets/Ui/Menu/Cloud.png")
cloud_rect = cloud.get_rect()
menu_music = pygame.mixer.Sound("./Assets/Music/MenuMusic.wav")
menu_music_playing = False
menu_bg = pygame.image.load("Assets/Ui/Menu/Background.png").convert()
menu_tiles = math.ceil((SCREEN_WIDTH / menu_bg.get_width())) + 1

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cloud
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(0, SCREEN_HEIGHT - menu_bg.get_height())
        self.speed = random.randint(2,6)
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

cloud_group = pygame.sprite.Group()

#Player loading
player = pygame.image.load("Assets/Ships/ship_0000.png")
player_rect = player.get_rect()
player_rect.topleft = (player_x, player_y)

biome = 1
loaded_obstacles = []

dirt_obstacles = [pygame.transform.scale(pygame.image.load(f"Assets/Tiles/Dirt/obstacles/dirt_obstacle_{obstacle}.png"), (64, 64)) for obstacle in range(1,6)]
grass_obstacles = [pygame.transform.scale(pygame.image.load(f"Assets/Tiles/Grass/Obstacles/grass_obstacle_{obstacle}.png"), (64, 64)) for obstacle in range(1,6)]

tiles = math.ceil((SCREEN_HEIGHT / bg_height)) + 1

async def main():
    global SCREEN_HEIGHT, menu_scroll, menu_bg, menu_music, menu_music_playing, cloud_group, play_button_rect, cloud, cloud_rect, play_button, play_button_scaled, SCREEN_WIDTH, game_state,  WHITE, SKY_BLUE, scroll, PLAYER_HEIGHT, PLAYER_WIDTH, screen, clock, running, player_x, player_y, velocity, player, player_rect, biome, dirt_obstacles, grass_obstacles, loaded_obstacles, grass_bg, dirt_bg, bg_width, bg_height

    last_obstacle_spawn_time = pygame.time.get_ticks()

    while running:   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_state == "menu":
            if not menu_music_playing:
                menu_music.play(-1)
                menu_music_playing = True
            cloud_spawn = random.randint(1,60)
            if cloud_spawn == 50:
                new_cloud = Cloud()
                cloud_group.add(new_cloud)
            screen.fill(SKY_BLUE)
            cloud_group.update()
            cloud_group.draw(screen)
            for i in range(0, menu_tiles):
                screen.blit(menu_bg, (i * menu_bg.get_width() + scroll, 500))
            scroll -= 2

            #reset scroll
            if abs(scroll) > bg_width:
                scroll = 0

            if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(play_button_hover, play_button_hover_rect)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Clicked")
                    game_state = "playing"

            else:
                screen.blit(play_button_scaled, play_button_rect)
            if setting_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(setting_button_hover, setting_button_hover_rect)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = "settings"
            else:
                screen.blit(setting_button_scaled, setting_button_rect)
            if achievements_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(achievements_button_hover, achievements_button_hover_rect)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = "achievements"
            else:
                screen.blit(achievements_button_scaled, achievements_button_rect)
            
        if game_state == "settings":
            print("settings")

        if game_state == "playing":
            menu_music_playing = False
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