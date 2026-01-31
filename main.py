#Import modules
import pygame, asyncio, random
import math

#Setting up audio clock and pygame window
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption("Plane Game")
pygame.font.init()

#Constant variables
class GameConfig:
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 800
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    SKY_BLUE = (224, 251, 252)
    PLAYER_HEIGHT = 32
    PLAYER_WIDTH = 32
    FPS = 60

class GameState:
    def __init__(self):   
    
        #Main game
        self.player_x = GameConfig.SCREEN_WIDTH / 2
        self.player_y = 725
        self.velocity = 1
        self.score = 0
        self.last_time = pygame.time.get_ticks()

        #Main game background
        self.scroll = 0
        self.grass_bg = pygame.image.load("./Assets/Tiles/Grass/BG/Grass_BG.png").convert()
        self.dirt_bg = pygame.image.load("./Assets/Tiles/Dirt/BG/DirtBg.png").convert()
        self.bg_width = self.grass_bg.get_width()
        self.bg_height = self.grass_bg.get_height()
        self.biome = 1
        self.tiles = math.ceil((GameConfig.SCREEN_HEIGHT / self.bg_height)) + 1
        self.current_screen = "menu"
        self.lives = 1
        self.score_font = pygame.font.Font("./Assets/Fonts/CabinSketch-Bold.ttf", 30)

#Obstacle generation and scrolling
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def update(self):
        self.rect.y += 5
        if self.rect.top > GameConfig.SCREEN_HEIGHT:
            self.kill()

obstacle_group = pygame.sprite.Group()

class Menu:
#Ui loading
    def __init__(self):
        self.button_gap = 20
        self._load_buttons()
        self._load_backgrounds()
        self.menu_scroll = 0
        self.cloud_group = pygame.sprite.Group()

    def _load_buttons(self):

        #Settings button
        self.setting_button = pygame.image.load("Assets/Ui/Menu/SettingsButton.png").convert_alpha()
        self.setting_button_scaled = pygame.transform.scale(self.setting_button, (250, 3750/67))
        self.setting_button_rect = self.setting_button_scaled.get_rect()
        self.setting_button_hover = pygame.transform.scale(pygame.image.load("Assets/Ui/Menu/SettingsButtonHover.png"), (250, 3750/67)).convert_alpha()
        self.setting_button_hover_rect = self.setting_button_hover.get_rect()
        self.setting_button_rect.topleft = (GameConfig.SCREEN_WIDTH / 2 - self.setting_button_rect.width / 2, GameConfig.SCREEN_HEIGHT / 2 - self.setting_button_rect.height)
        self.setting_button_hover_rect.topleft = (GameConfig.SCREEN_WIDTH / 2 - self.setting_button_hover_rect.width / 2, GameConfig.SCREEN_HEIGHT / 2 - self.setting_button_hover_rect.height)
    
        #Play button
        self.play_button = pygame.image.load("Assets/Ui/Menu/PlayButton.png").convert_alpha()
        self.play_button_scaled = pygame.transform.scale(self.play_button, (250, 3750/67))
        self.play_button_rect = self.play_button_scaled.get_rect()
        self.play_button_hover = pygame.transform.scale(pygame.image.load("Assets/Ui/Menu/PlayButtonHover.png"), (250, 3750/67)).convert_alpha()
        self.play_button_hover_rect = self.play_button_hover.get_rect()
        self.play_button_rect.topleft = (GameConfig.SCREEN_WIDTH / 2 - self.play_button_rect.width / 2, self.setting_button_rect.y - self.button_gap - self.play_button_rect.height)
        self.play_button_hover_rect.topleft = (GameConfig.SCREEN_WIDTH / 2 - self.play_button_hover_rect.width / 2, self.setting_button_rect.y - self.button_gap - self.play_button_rect.height)
        #Achievements button
        self.achievements_button = pygame.image.load("Assets/Ui/Menu/AchievementsButton.png").convert_alpha()
        self.achievements_button_scaled = pygame.transform.scale(self.achievements_button, (250, 3750/67))
        self.achievements_button_rect = self.setting_button_scaled.get_rect()
        self.achievements_button_hover = pygame.transform.scale(pygame.image.load("Assets/Ui/Menu/AchievementsButtonHover.png"), (250, 3750/67)).convert_alpha()
        self.achievements_button_hover_rect = self.setting_button_hover.get_rect()
        self.achievements_button_rect.topleft = (GameConfig.SCREEN_WIDTH / 2 - self.achievements_button_rect.width / 2, self.setting_button_rect.y + self.button_gap + self.achievements_button_rect.height)
        self.achievements_button_hover_rect.topleft = (GameConfig.SCREEN_WIDTH / 2 - self.achievements_button_hover_rect.width / 2, self.setting_button_rect.y + self.button_gap + self.achievements_button_rect.height)

    def _load_backgrounds(self):
        #Loading bg images/ assets
        #Menu Background
        self.cloud = pygame.image.load("Assets/Ui/Menu/Cloud.png").convert_alpha()
        self.cloud_rect = self.cloud.get_rect()
        self.menu_bg = pygame.image.load("Assets/Ui/Menu/Background.png").convert()
        self.menu_tiles = math.ceil((GameConfig.SCREEN_WIDTH / self.menu_bg.get_width())) + 1

    def update_scroll(self):
        self.scroll -= 2
        if abs(self.scroll) > self.menu_bg.get_width():
            self.scroll = 0
    def spawn_cloud(self):
        if random.randint(1, 60) == 50:
            new_cloud = Cloud(self.cloud)
            self.cloud_group.add(new_cloud)

class GameOver:
#Ui loading
    def __init__(self): 
        self.button_gap = 10
        self.button_gap_hover = 10
        self._load_buttons()
        self._load_backgrounds()
        self.menu_scroll = 0
        self.cloud_group = pygame.sprite.Group()

    def _load_buttons(self):

        #Settings button
    
        #Play button
        self.play_again_button = pygame.image.load("Assets/Ui/GameOver/PlayAgain.png").convert_alpha()
        self.play_again_button_scaled = pygame.transform.scale(self.play_again_button, (250, 3750/67))
        self.play_again_button_rect = self.play_again_button_scaled.get_rect()
        self.play_again_button_hover = pygame.transform.scale(pygame.image.load("Assets/Ui/GameOver/PlayAgainHover.png"), (250, 3750/67)).convert_alpha()
        self.play_again_button_hover_rect = self.play_again_button_hover.get_rect()
        self.play_again_button_rect.bottomleft = (GameConfig.SCREEN_WIDTH / 2 - self.play_again_button_rect.width / 2, GameConfig.SCREEN_HEIGHT / 2 - self.play_again_button_rect.height / 2 - self.button_gap)
        self.play_again_button_hover_rect.bottomleft = (GameConfig.SCREEN_WIDTH / 2 - self.play_again_button_hover_rect.width / 2, GameConfig.SCREEN_HEIGHT / 2 - self.play_again_button_rect.height / 2 - self.button_gap_hover)

        #Achievements button
        self.main_menu_button = pygame.image.load("Assets/Ui/GameOver/MainMenu.png").convert_alpha()
        self.main_menu_button_scaled = pygame.transform.scale(self.main_menu_button, (250, 3750/67))
        self.main_menu_button_rect = self.main_menu_button_scaled.get_rect()
        self.main_menu_button_hover = pygame.transform.scale(pygame.image.load("Assets/Ui/GameOver/MainMenuHover.png"), (250, 3750/67)).convert_alpha()
        self.main_menu_button_hover_rect = self.main_menu_button_hover.get_rect()
        self.main_menu_button_rect.bottomleft = (GameConfig.SCREEN_WIDTH / 2 -self.main_menu_button_rect.width / 2,  GameConfig.SCREEN_HEIGHT / 2 + self.play_again_button_rect.height /2 + self.button_gap)
        self.main_menu_button_hover_rect.bottomleft = (GameConfig.SCREEN_WIDTH / 2 -self.main_menu_button_hover_rect.width / 2, GameConfig.SCREEN_HEIGHT / 2 + self.main_menu_button_rect.height / 2 + self.button_gap_hover)

        #Score Button
        self.score_button = pygame.image.load("Assets/Ui/GameOver/ScoreButton.png").convert_alpha()
        self.score_button_scaled = pygame.transform.scale(self.score_button, (250, 3750/67))
        self.score_button_rect = self.score_button_scaled.get_rect()
        self.score_button_hover = pygame.transform.scale(pygame.image.load("Assets/Ui/GameOver/ScoreButtonHover.png"), (250, 3750/67)).convert_alpha()
        self.score_button_hover_rect = self.score_button_hover.get_rect()
        self.score_button_rect.bottomleft = (GameConfig.SCREEN_WIDTH / 2 - self.score_button_rect.width / 2, self.play_again_button_rect.top - self.button_gap * 2)
        self.score_button_hover_rect.bottomleft = (GameConfig.SCREEN_WIDTH / 2 -self.score_button_hover_rect.width / 2, self.play_again_button_hover_rect.top - self.button_gap_hover * 2)
        self.final_score_font = pygame.font.Font("./Assets/Fonts/CabinSketch-Bold.ttf", 28)

    def display_score(self, screen, current_score):
        score_surface = self.final_score_font.render(str(current_score), True, GameConfig.BLACK)
        score_rect = score_surface.get_rect(midright=(self.score_button_rect.right - 25, self.score_button_rect.centery))
        screen.blit(score_surface, score_rect)

    def _load_backgrounds(self):
        #Loading bg images/ assets
        #Menu Background
        self.cloud = pygame.image.load("Assets/Ui/Menu/Cloud.png").convert_alpha()
        self.cloud_rect = self.cloud.get_rect()
        self.menu_bg = pygame.image.load("Assets/Ui/Menu/Background.png").convert()
        self.menu_tiles = math.ceil((GameConfig.SCREEN_WIDTH / self.menu_bg.get_width())) + 1

    def update_scroll(self):
        self.scroll -= 2
        if abs(self.scroll) > self.menu_bg.get_width():
            self.scroll = 0
    def spawn_cloud(self):
        if random.randint(1, 60) == 50:
            new_cloud = Cloud(self.cloud)
            self.cloud_group.add(new_cloud)


#Cloud class for scrolling clouds
class Cloud(pygame.sprite.Sprite):
    def __init__(self, cloud):
        super().__init__()
        self.image = cloud
        self.rect = self.image.get_rect()
        self.rect.x = GameConfig.SCREEN_WIDTH
        self.rect.y = random.randint(0, GameConfig.SCREEN_HEIGHT - 200)
        self.speed = random.randint(2,6)
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
cloud_group = pygame.sprite.Group()

#For mediapipe
class InputManager:
    def __init__(self):
        self.move_left = False
        self.move_right = False
        self.target_x = None
    def update_from_keyboard(self):
        keys = pygame.key.get_pressed()
        self.move_left = keys[pygame.K_LEFT]
        self.move_right = keys[pygame.K_RIGHT]
    
    def update_from_mediapipe(self, normalized_x):
        self.target_x = normalized_x * GameConfig.SCREEN_WIDTH
    

#Menu music
class Music:
    menu_music = pygame.mixer.Sound("./Assets/Music/MenuMusic1.ogg")
    menu_music_playing = False
    game_music = pygame.mixer.Sound("./Assets/Music/GameMusic.ogg")
    game_music_playing = False
    game_over_music_playing = False
    game_over_music = pygame.mixer.Sound("./Assets/Music/GameOver.ogg")

async def main():
    running = True
    screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game_state = GameState()
    menu = Menu()
    game_over = GameOver()
    input_mgr = InputManager()

    #Player loading
    player = pygame.image.load("Assets/Ships/ship_0000.png").convert_alpha()
    player_rect = player.get_rect()
    player_rect.topleft = (game_state.player_x, game_state.player_y)

    #Load obstacles and sets up the last obstacle spawn var
    last_obstacle_spawn_time = pygame.time.get_ticks()
    dirt_obstacles = [pygame.transform.scale(pygame.image.load(f"Assets/Tiles/Dirt/obstacles/dirt_obstacle_{i}.png").convert_alpha(), (64, 64)) for i in range(1, 6)]
    grass_obstacles = [pygame.transform.scale(pygame.image.load(f"Assets/Tiles/Grass/obstacles/grass_obstacle_{i}.png").convert_alpha(), (64, 64)) for i in range(1, 6)]
    
    #Main game loop
    while running:

        click = False
        #Handles exiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        #Menu game state
        if game_state.current_screen == "menu":

            #Handles music
            if not Music.menu_music_playing:
                Music.menu_music.play(-1)
                Music.menu_music_playing = True
            
            menu.spawn_cloud()
            screen.fill(GameConfig.SKY_BLUE)
            menu.cloud_group.update()
            menu.cloud_group.draw(screen)

            #Scrolling mountains bg
            for i in range(0, menu.menu_tiles):
                screen.blit(menu.menu_bg, (i * menu.menu_bg.get_width() + menu.menu_scroll, 500))
            menu.menu_scroll -= 2
        
            #reset scroll
            if abs(menu.menu_scroll) > menu.menu_bg.get_width():
                menu.menu_scroll = 0

            #Play button hover and click detection / animation
            if menu.play_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(menu.play_button_hover, menu.play_button_hover_rect)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Clicked")
                    game_state.score = 0
                    game_state.current_screen = "playing"
            else:
                screen.blit(menu.play_button_scaled, menu.play_button_rect)

            #Settings button 
            if menu.setting_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(menu.setting_button_hover, menu.setting_button_hover_rect)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state.current_screen = "settings"
            else:
                screen.blit(menu.setting_button_scaled, menu.setting_button_rect)

            #Achievements button
            if menu.achievements_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(menu.achievements_button_hover, menu.achievements_button_hover_rect)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state.current_screen = "achievements"
            else:
                screen.blit(menu.achievements_button_scaled, menu.achievements_button_rect)
        
        #Settings game state
        if game_state.current_screen == "settings":
            print("settings")

        #Game over game state
        if game_state.current_screen == "game_over":

            #Handles music
            if not Music.game_over_music_playing:
                Music.game_music.fadeout(1000)
                Music.game_music_playing = False
                Music.game_over_music.play(-1)
                Music.game_over_music_playing = True
                Music.menu_music_playing = True
            
            menu.spawn_cloud()
            screen.fill(GameConfig.SKY_BLUE)
            menu.cloud_group.update()
            menu.cloud_group.draw(screen)

            #Scrolling mountains bg
            for i in range(0, menu.menu_tiles):
                screen.blit(menu.menu_bg, (i * menu.menu_bg.get_width() + menu.menu_scroll, 500))
            menu.menu_scroll -= 2
        
            #reset scroll
            if abs(menu.menu_scroll) > menu.menu_bg.get_width():
                menu.menu_scroll = 0

            #Play button hover and click detection / animation
            if game_over.play_again_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(game_over.play_again_button_hover, game_over.play_again_button_hover_rect)
                if click:
                    print("Clicked")
                    game_state.score = 0
                    game_state.current_screen = "playing"
                    Music.game_over_music_playing = False
            else:
                screen.blit(game_over.play_again_button_scaled, game_over.play_again_button_rect)
            
            if game_over.main_menu_button_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(game_over.main_menu_button_hover, game_over.main_menu_button_hover_rect)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    Music.game_over_music_playing = False
                    game_state.score = 0
                    Music.game_over_music.fadeout(1000)
                    game_state.current_screen = "menu"
            else:
                screen.blit(game_over.main_menu_button_scaled, game_over.main_menu_button_rect)
            screen.blit(game_over.score_button_scaled, game_over.score_button_rect)
            #screen.blit(game_over.score, (400, 200)
            game_over.display_score(screen, game_state.score)


        #Settings game state
        if game_state.current_screen == "settings":
            print("settings")

        #Main game
        if game_state.current_screen == "playing":

            #Turns of menu music gets time and refreshes screen
            if not Music.game_music_playing:
                Music.game_music.play(-1)
                Music.game_music_playing = True
                Music.menu_music.fadeout(1000)
                Music.menu_music_playing = False
                Music.game_over_music.fadeout(1000)
                Music.menu_music_playing = False

            screen.fill(GameConfig.SKY_BLUE)
            current_time = pygame.time.get_ticks()

            input_mgr.update_from_keyboard()

            if input_mgr.move_left and input_mgr.move_right:
                game_state.velocity = 1
            elif input_mgr.move_left:
                game_state.player_x -= game_state.velocity
                game_state.velocity += 0.15
                if game_state.velocity > 9:
                    game_state.velocity = 9
            elif input_mgr.move_right:
                game_state.player_x += game_state.velocity
                game_state.velocity += 0.15
                if game_state.velocity > 9:
                    game_state.velocity = 9
            else:
                game_state.velocity = 1

            #Biome and obstacle stuff

            #Random biome change
            if random.randint(1, 700) == 500:
                game_state.biome = random.randint(1,2)

            #Spawns new obstacle if its been more than 500 ticks
            if current_time - last_obstacle_spawn_time > 400:
                if game_state.biome == 1:
                    current_list = grass_obstacles
                else:
                    current_list = dirt_obstacles

                #Generates obstacle
                image = random.choice(current_list)
                spawn_x = random.randint(0, GameConfig.SCREEN_WIDTH - 64)
                spawn_y = -70         
                new_obstacle = Obstacle(image, spawn_x, spawn_y)
                obstacle_group.add(new_obstacle)
                last_obstacle_spawn_time = current_time

            #Player boundarys
            if game_state.player_x < 0:
                game_state.player_x = 0
            if game_state.player_x + GameConfig.PLAYER_WIDTH > GameConfig.SCREEN_WIDTH:
                game_state.player_x = GameConfig.SCREEN_WIDTH - GameConfig.PLAYER_WIDTH
            if game_state.player_y < 0:
                game_state.player_y = 0
            if game_state.player_y + GameConfig.PLAYER_HEIGHT > GameConfig.SCREEN_HEIGHT:
                game_state.player_y = GameConfig.SCREEN_HEIGHT - GameConfig.PLAYER_HEIGHT

            #Updates player pos
            player_rect.topleft = (game_state.player_x, game_state.player_y)

            #Scrolls background
            for i in range(0, game_state.tiles):
                if game_state.biome == 1:
                    screen.blit(game_state.grass_bg, (0, (i - 1) * game_state.bg_height + game_state.scroll))
                elif game_state.biome == 2:
                    screen.blit(game_state.dirt_bg, (0, (i -1) * game_state.bg_height + game_state.scroll))
            game_state.scroll += 5
            if game_state.scroll >= game_state.bg_height:
                game_state.scroll = 0

            #More obstacle stuff
            obstacle_group.update()
            obstacle_group.draw(screen)
            screen.blit(player, player_rect)
            for obstacle in obstacle_group:
                if player_rect.colliderect(obstacle.rect):
                    game_state.lives -= 1
                    if game_state.lives <1:
                        game_state.current_screen = "game_over"
                        obstacle_group.empty()
                        break
            
            #Score Handling
            current_time = pygame.time.get_ticks()
            dt = (current_time - game_state.last_time)
            game_state.last_time = current_time
            game_state.score += dt
            score_text = game_over.final_score_font.render(str(game_state.score), True, GameConfig.BLACK )
            score_text_rect = score_text.get_rect()
            score_text_rect.topleft = (590 - score_text_rect.width, 5)
            screen.blit(score_text, score_text_rect)

        
        #Flips screen and limits fps
        pygame.display.flip()
        clock.tick(GameConfig.FPS)
        await asyncio.sleep(0)

    pygame.quit()
if __name__ == "__main__":
   asyncio.run(main())