# Ethan Lawrence 
# Feb 12 2025
# Pygame template ver 2

import pygame
import sys
import config

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
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.TITLE)
    running = True
    # On Startup
    bullets = []
    player = Player_character([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [0, 0], (0, 0, 255), [25, 25])
    while running:
        running = handle_events()
        screen.fill(config.BLACK)
        # While Running
        player.player_input()
        player.move()

        # Spawn Bullets
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            for bullet in patterns['star']:
                bullets.append(bullet)

        for this_bullet in bullets:
            if this_bullet.move():
                print('bullet removed')
                bullets.remove(this_bullet)
        
        for this_bullet in bullets:
            for point in player.get_hurtbox():
                if this_bullet.get_hitbox().collidepoint(point):
                    if player.get_hit():
                        return True
        # Draw Objects
        for this_bullet in bullets:
            this_bullet.draw(screen)
        player.draw(screen)
        # Limit clock to FPS & Update Screen
        pygame.display.flip()
        clock.tick(config.FPS)
    pygame.quit()
    sys.exit()

# Other Functions
    
class Bullet:
    '''Object that can move that the player has dodge'''
    def __init__(self, pos, speed, color, scale):
        self.speed = speed
        self.color = color
        self.scale = scale
        self.pos = [pos[0]-(scale[0]/2), pos[1]-(scale[1]/2)]
    def move(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        if not(0 < self.pos[0] < config.WINDOW_WIDTH) or not(0 < self.pos[1] < config.WINDOW_HEIGHT):
            return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.scale[0], self.scale[1]))
    def get_hitbox(self):
        return(pygame.Rect(self.pos[0], self.pos[1], self.scale[0], self.scale[1]))
    

class Player_character:
    '''Object that represents the player'''
    def __init__(self, pos, speed, color, scale):
        self.speed = speed
        self.color = color
        self.scale = scale
        self.pos = [pos[0]-(scale[0]/2), pos[1]-(scale[1]/2)]
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
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] and keys[pygame.K_s]) or not(keys[pygame.K_w] or keys[pygame.K_s]):
            self.speed[1] = 0
        elif keys[pygame.K_w]:
            self.speed[1] = -5
        elif keys[pygame.K_s]:
            self.speed[1] = 5
        
        if (keys[pygame.K_a] and keys[pygame.K_d]) or not(keys[pygame.K_a] or keys[pygame.K_d]):
            self.speed[0] = 0
        elif keys[pygame.K_a]:
            self.speed[0] = -5
        elif keys[pygame.K_d]:
            self.speed[0] = 5
            
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
            [self.pos[0]+self.scale[0], self.pos[1]]
        ]
        return boxes
    def get_hit(self):
        if self.i_frames == 0:
            self.lives -= 1
            self.i_frames = config.FPS
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
patterns = {
    'star' : [
        Bullet([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [5, 3], (255, 0, 0), [50, 50]),
        Bullet([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [5, -3], (255, 0, 0), [50, 50]),
        Bullet([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [-5, 3], (255, 0, 0), [50, 50]),
        Bullet([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [-5, -3], (255, 0, 0), [50, 50]),

        Bullet([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [3, 5], (255, 0, 0), [50, 50]),
        Bullet([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [3, -5], (255, 0, 0), [50, 50]),
        Bullet([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [-3, 5], (255, 0, 0), [50, 50]),
        Bullet([config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2], [-3, -5], (255, 0, 0), [50, 50])
    ]
}
if __name__ == '__main__':
    clicked = False
    clock = pygame.time.Clock()
    main_menu()