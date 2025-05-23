# Ethan Lawrence 
# Feb 12 2025
# Pygame template ver 2

import pygame
import sys
import config
import copy
import random 

# Generic Functions
def handle_events():
    global clicked
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
    return True
def main():
    global bullets
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.TITLE)
    running = True
    pygame.mixer.init()
    pygame.mixer.music.load('main-theme.ogg')
    pygame.mixer.music.play(-1)
    # On Startup
    player = Player_character([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [0, 0], [0, 0, 255], [25, 25])
    reader = 'start'
    count = config.FPS * 2
    pattern_rounds = 0
    danger_zone = (0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    shot_location = []
    new_pattern = [[10]] # Needs a [0][0] slot, '10' is to prevent a rain or volly on r1
    time_passed = 0
    bullet_repeater = 0
    bullets = []
    while running:
        running = handle_events()
        screen.fill(config.BLACK)
        pygame.draw.rect(screen, config.DANGER_RED, danger_zone)
        # While Running
        player.player_input()
        player.move()

        time_passed += 1/config.FPS
        # Spawn Bullets
        count -= 1
        if count == 0:
            if pattern_rounds == 0:
                # New Pattern
                last_pattern = new_pattern
                while new_pattern[0][0] == last_pattern[0][0]: # this prevents duplicate rounds or simular attacks from repeating after eachother
                    new_pattern = copy.deepcopy(patterns[random.randrange(len(patterns))]) # random.randrange(len(patterns))
                pattern_rounds = new_pattern[0][0]
                count = new_pattern[0][1]
                danger_zone = new_pattern[0][2]
                if danger_zone == 'sniper':
                        danger_zone = [player.pos[0]-(player.scale[0]/2), player.pos[1]-(player.scale[1]/2), 2*player.scale[0], 2*player.scale[1]]
                        shot_location = player.pos[0]+(player.scale[0]/2), player.pos[1]+(player.scale[1]/2)
                elif danger_zone == 'rail-gun':
                    danger_zone = [0, random.randint(0, config.WINDOW_HEIGHT), config.WINDOW_WIDTH, 50]
                    shot_location = 0, danger_zone[1] + 25
                    bullet_repeater = 2
                elif danger_zone == 'comet':
                    danger_zone = (0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
                    shot_location = 'comet'
                else:
                    shot_location = []
            else:
                # Repeat Pattern
                reader = 1
                for bullet in new_pattern:
                    if reader == 1:
                        pattern_rounds -= 1
                        reader = 0
                        count = new_pattern[0][1]
                        if pattern_rounds == 0:
                            count += config.FPS/2
                        continue
                    bullets.append(Bullet(bullet[0], bullet[1], bullet[2], bullet[3], shot_location))
                    if bullet_repeater > 0:
                        bullet_repeater -= 1
                        danger_zone = new_pattern[0][2]
                    if danger_zone == 'sniper':
                        danger_zone = [player.pos[0]-(player.scale[0]/2), player.pos[1]-(player.scale[1]/2), 2*player.scale[0], 2*player.scale[1]]
                        shot_location = player.pos[0]+(player.scale[0]/2), player.pos[1]+(player.scale[1]/2)
                    elif danger_zone == 'rail-gun':
                        danger_zone = [0, random.randint(0, config.WINDOW_HEIGHT), config.WINDOW_WIDTH, 50]
                        shot_location = 0, danger_zone[1] + 25
        for this_bullet in bullets:
            if this_bullet.move():
                bullets.remove(this_bullet)
        
        for this_bullet in bullets:
            for point in player.get_hurtbox():
                if this_bullet.get_hitbox().collidepoint(point):
                    if player.get_hit():
                        return True
        # Timer
        screen.blit(pygame.font.SysFont('Arial', 40).render(f'Score: {str(int(time_passed))}', True, config.WHITE), (100, 100))
        # Draw Objects
        for this_bullet in bullets:
            this_bullet.draw(screen)
        player.draw(screen)
        # Limit clock to FPS & Update Screen
        pygame.display.flip()
        clock.tick(config.FPS)
    bullets = []
    pygame.quit()
    sys.exit()

# Other Functions
class Character:
    def __init__(self, pos, speed, color, scale):
        self.speed = speed
        if speed[0] == 'r':
            self.speed[0] = random.randint(5, 10)
        elif speed[0] == 'tr':
            self.speed[0] = 0
            while self.speed[0] == 0:
                self.speed[0] = random.randint(-10, 10)
        if speed[1] == 'r':
            self.speed[1] = random.randint(5, 10)
        elif speed[1] == 'tr':
            self.speed[1] = 0
            while self.speed[1] == 0:
                self.speed[1] = random.randint(-10, 10)
        self.color = color
        self.scale = scale
        self.pos = []
        if pos[0] == 'r':
            self.pos.append(random.randint(0, config.WINDOW_WIDTH-scale[0]))
        elif pos[0] == 'p':
            self.pos.append('placeholder')
        else:
            self.pos.append(pos[0]-(scale[0]/2))
        if pos[1] == 'r':
            self.pos.append(random.randint(0, config.WINDOW_HEIGHT-scale[1]))
        elif pos[1] == 'p':
            self.pos.append('placeholder')
        else:
            self.pos.append(pos[1]-(scale[1]/2))
class Bullet(Character):
    '''Object that can move that the player has dodge'''
    def __init__(self, pos, speed, color, scale, shot_point):
        Character.__init__(self, pos, speed, color, scale)
        if self.pos[0] == 'placeholder':
            self.pos[0] = (int(shot_point[0])-scale[0])
        if self.pos[1] == 'placeholder':
            self.pos[1] = (int(shot_point[1])-scale[1])
        if shot_point == 'comet':
            self.shot_point = shot_point
        else:
            self.shot_point = 'NA'
    def move(self):
        self.pos[0] = int(self.pos[0]) + self.speed[0]
        self.pos[1] = int(self.pos[1]) + self.speed[1]
        if not(0 < self.pos[0] < config.WINDOW_WIDTH) or not(0 < self.pos[1] < config.WINDOW_HEIGHT):
            return True
        if self.shot_point == 'comet':
            if (config.WINDOW_WIDTH/2)-100 < self.pos[0] < (config.WINDOW_WIDTH/2)+100:
                for i in range(1, 10):
                    bullets.append(Bullet([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], ['tr', 'tr'], (200, 0, 0), [10, 10], 'NA'))
                return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.scale[0], self.scale[1]))
    def get_hitbox(self):
        return(pygame.Rect(self.pos[0], self.pos[1], self.scale[0], self.scale[1]))
    

class Player_character(Character):
    '''Object that represents the player'''
    def __init__(self, pos, speed, color, scale):
        Character.__init__(self, pos, speed, color, scale)
        self.lives = 3
        self.i_frames = 0
    def move(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        if not(0 < self.pos[0] < config.WINDOW_WIDTH-self.scale[0]):
            self.pos[0] -= self.speed[0]
        if not(0 < self.pos[1] < config.WINDOW_HEIGHT-self.scale[1]):
            self.pos[1] -= self.speed[1]
    def player_input(self):
        keys_pressed = pygame.key.get_pressed()
        if (keys_pressed[pygame.K_w] and keys_pressed[pygame.K_s]) or not(keys_pressed[pygame.K_w] or keys_pressed[pygame.K_s]):
            self.speed[1] = 0
        elif keys_pressed[pygame.K_w]:
            self.speed[1] = -5
        elif keys_pressed[pygame.K_s]:
            self.speed[1] = 5
        
        if (keys_pressed[pygame.K_a] and keys_pressed[pygame.K_d]) or not(keys_pressed[pygame.K_a] or keys_pressed[pygame.K_d]):
            self.speed[0] = 0
        elif keys_pressed[pygame.K_a]:
            self.speed[0] = -5
        elif keys_pressed[pygame.K_d]:
            self.speed[0] = 5
        
        if keys_pressed[pygame.K_LSHIFT]:
            self.speed[0] *= 2
            self.speed[1] *= 2
    def draw(self, screen):
        if self.i_frames != 0:
            self.i_frames -= 1
            if self.i_frames % 10 == 0:
                pygame.draw.rect(screen, config.WHITE, (self.pos[0], self.pos[1], self.scale[0], self.scale[1]))
                return
        pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.scale[0], self.scale[1]))
        
    def get_hurtbox(self):
        boxes = [
            [self.pos[0], self.pos[1]],
            [self.pos[0], self.pos[1]+self.scale[1]],
            [self.pos[0]+self.scale[0], self.pos[1]+self.scale[1]],
            [self.pos[0]+self.scale[0], self.pos[1]],
            [self.pos[0]+(self.scale[0]/2), self.pos[1]+(self.scale[1]/2)]
        ]
        return boxes
    def get_hit(self):
        if self.i_frames == 0:
            self.lives -= 1
            self.i_frames = config.FPS * 2
            pygame.mixer.Sound('player_hit.wav').play()
            self.color[0] += 100
            self.color[1] += 100
            if self.lives == 0:
                return True
            return False



# Main menu
def main_menu():
    global clicked
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.TITLE)
    pygame.display.set_caption('Main Menu')

    font = pygame.font.SysFont('Arial', 40)
    buttons = {
        'play_button' : {},
        'quit_button' : {}
    }
    buttons['play_button']['rect'] = pygame.Rect(0, config.WINDOW_HEIGHT // 3, 200, 50)
    buttons['play_button']['rect'].centerx = config.WINDOW_WIDTH // 2
    buttons['play_button']['text'] = font.render('PLAY', True, config.WHITE)
    buttons['play_button']['text rect'] = buttons['play_button']['text'].get_rect(center=buttons['play_button']['rect'].center)

    buttons['quit_button']['rect'] = pygame.Rect(0, config.WINDOW_HEIGHT // 2, 200, 50)
    buttons['quit_button']['rect'].centerx = config.WINDOW_WIDTH // 2
    buttons['quit_button']['text'] = font.render('EXIT', True, config.WHITE)
    buttons['quit_button']['text rect'] = buttons['quit_button']['text'].get_rect(center=buttons['quit_button']['rect'].center)

    running_menu = True
    while running_menu:
        running_menu = handle_events()
        if clicked:
            if buttons['play_button']['rect'].collidepoint(pygame.mouse.get_pos()):
                clicked = False
                main()
            if buttons['quit_button']['rect'].collidepoint(pygame.mouse.get_pos()):
                clicked = False
                pygame.quit()
                sys.exit()
        screen.fill((50,50,50))
        for button in buttons: # Display Buttons
            pygame.draw.rect(screen, (100, 100, 200), buttons[button]['rect'])
            screen.blit(buttons[button]['text'], buttons[button]['text rect'])

        pygame.display.flip()
        clock.tick(config.FPS)
    pygame.quit()
    sys.exit()

# Startup
patterns = [
    # pos, speed, color, scale
    [ # Twin X
        [3, config.FPS/3, (config.WINDOW_WIDTH/2-50, config.WINDOW_HEIGHT/2-50, 100, 100)],
        ([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [5, 3], (255, 0, 0), [20, 20]),
        ([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [5, -3], (255, 0, 0), [20, 20]),
        ([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [-5, 3], (255, 0, 0), [20, 20]),
        ([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [-5, -3], (255, 0, 0), [20, 20]),

        ([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [3, 5], (255, 0, 0), [20, 20]),
        ([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [3, -5], (255, 0, 0), [20, 20]),
        ([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [-3, 5], (255, 0, 0), [20, 20]),
        ([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [-3, -5], (255, 0, 0), [20, 20])
    ],
    [ # Rain
        [10, config.FPS/10, (0, 0, config.WINDOW_WIDTH, 50)],
        (['r', 25], [0, 'r'], (0, 0, 200), [10, 25]),
        (['r', 25], [0, 'r'], (0, 0, 200), [10, 25]),
        (['r', 25], [0, 'r'], (0, 0, 200), [10, 25])
    ],
    [ # Volly
        [10, config.FPS/30, (0, 0, 50, config.WINDOW_HEIGHT)],
        ([25, 'r'], ['r', 0], (200, 200, 200), [25, 10]),
        ([25, 'r'], ['r', 0], (200, 200, 200), [25, 10]),
        ([25, 'r'], ['r', 0], (200, 200, 200), [25, 10])
    ],
    [ # Plus
        [3, config.FPS/5, (config.WINDOW_WIDTH/2-50, config.WINDOW_HEIGHT/2-50, 100, 100)],
        ([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [7, 0], (255, 0, 0), [50, 60]),
        ([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [-7, 0], (255, 0, 0), [50, 60]),
        ([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [0, -7], (255, 0, 0), [60, 50]),
        ([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [0, 7], (255, 0, 0), [60, 50])
    ],
    [ # Sniper
        [1, config.FPS, 'sniper'],
        (['p', 'p'], [10, 10], (255, 225, 0), [10, 10]),
        (['p', 'p'], [-10, 10], (255, 225, 0), [10, 10]),
        (['p', 'p'], [10, -10], (255, 225, 0), [10, 10]),
        (['p', 'p'], [-10, -10], (255, 225, 0), [10, 10]),
        
        (['p', 'p'], [10, 0], (255, 225, 0), [10, 10]),
        (['p', 'p'], [-10, 0], (255, 225, 0), [10, 10]),
        (['p', 'p'], [0, -10], (255, 225, 0), [10, 10]),
        (['p', 'p'], [-0, 10], (255, 225, 0), [10, 10])
    ],
    [ # Grass Grows
        [3, config.FPS/2, (0, config.WINDOW_HEIGHT-50, config.WINDOW_WIDTH, 50)],
        (['r', config.WINDOW_HEIGHT+(config.WINDOW_HEIGHT/2)], [0, -1], (0, 255, 0), [5, config.WINDOW_HEIGHT])
    ],
    [ # Flame Thrower
        [2, config.FPS/5, (config.WINDOW_WIDTH-50, 0, 50, config.WINDOW_HEIGHT)],
        ([config.WINDOW_WIDTH-50, 'r'], [-2, -3], (200, 50, 50), [25, 25]),
        ([config.WINDOW_WIDTH-50, 'r'], [-1, -3], (250, 50, 50), [25, 25]),
        ([config.WINDOW_WIDTH-50, 'r'], [-3, 3], (220, 220, 50), [50, 50]),
        ([config.WINDOW_WIDTH-50, 'r'], [-2, -3], (200, 50, 50), [25, 25]),
        ([config.WINDOW_WIDTH-50, 'r'], [-1, 3], (250, 50, 50), [50, 50]),
        ([config.WINDOW_WIDTH-50, 'r'], [-3, -3], (220, 220, 50), [25, 25]),
        ([config.WINDOW_WIDTH-50, 'r'], [-2, 3], (200, 50, 50), [50, 50]),
        ([config.WINDOW_WIDTH-50, 'r'], [-1, -3], (250, 50, 50), [25, 25]),
        ([config.WINDOW_WIDTH-50, 'r'], [-3, -3], (220, 220, 50), [25, 25])
    ],
    [ # Rail-Gun
        [3, config.FPS/2, 'rail-gun'],
        ([25, 'p'], [50, 0], (200, 200, 200), [100, 10])
    ],
    [ # Comet
        [1, config.FPS, 'comet'],
        ([config.WINDOW_WIDTH-50, 50], [-5, 5], (255, 0, 0), [100, 100]),
        ([50, 50], [5, 5], (255, 0, 0), [100, 100])
    ]
]
if __name__ == '__main__':
    bullets = []
    clicked = False
    clock = pygame.time.Clock()
    main_menu()