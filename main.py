import pygame
from sys import exit
from random import randint

class Button():
    def __init__(self, x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect) 
        return action


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'{current_time}', False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf,score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(varna_surf, obstacle_rect)
            else:
                screen.blit(balodis_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]    

        return obstacle_list
    else: return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True


def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 305:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pussy Cat')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 40)

game_active = True
start_time = 0
score = 0
main_menu = True

jump_sound = pygame.mixer.Sound('graphics/audio/jump.mp3')
jump_sound.set_volume(0.5)
bg_music = pygame.mixer.Sound('graphics/audio/bgmusic1.mp3')
bg_music.set_volume(0.5)
bg_music.play(loops= -1)

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
title_surface = pygame.image.load('graphics/title.png')
start_image = pygame.image.load('graphics/Buttons/start_btn.png')
exit_image = pygame.image.load('graphics/Buttons/exit_btn.png')

# score_surf = test_font.render('Score: ', False, 'Black')
# score_rect = score_surf.get_rect(center = (400,50))

#obstacles


varna_frame_1 = pygame.image.load('graphics/varna/varna1.png').convert_alpha()
varna_frame_2 = pygame.image.load('graphics/varna/varna2.png').convert_alpha()
varna_frames = [varna_frame_1, varna_frame_2]
varna_frame_index = 0
varna_surf = varna_frames[varna_frame_index]

balodis_frame_1 = pygame.image.load('graphics/balodis/balodis1.png').convert_alpha()
balodis_frame_2 = pygame.image.load('graphics/balodis/balodis2.png').convert_alpha()
balodis_frames = [balodis_frame_1, balodis_frame_2]
balodis_frame_index = 0
balodis_surf = balodis_frames[balodis_frame_index]


obstacle_rect_list = []


player_walk_1 = pygame.image.load('graphics/player/walk1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/walk2.png').convert_alpha()
player_walk_3 = pygame.image.load('graphics/player/walk3.png').convert_alpha()
player_walk_4 = pygame.image.load('graphics/player/walk4.png').convert_alpha()

player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4]
player_index = 0

player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (130,305))
player_grav = 0

player_stand = pygame.image.load('graphics/player/angry.png').convert_alpha()
player_stand = pygame.transform.scale(player_stand, (150, 150))
player_stand_rect = player_stand.get_rect(center = (400, 100))

game_name = test_font.render('Pussy Cat', False, (255,255,255))
game_name_rect = game_name.get_rect(center = (400, 200))

game_message = test_font.render('Press SPACE to run', False, (115,0,0))
game_message_rect = game_message.get_rect(center = (400, 320))

game_quit_msg = test_font.render('Press ESC to quit', False, (115,0,0))
game_quit_msg_rect = game_quit_msg.get_rect(center = (400, 360))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

varna_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(varna_animation_timer, 500)

balodis_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(balodis_animation_timer, 500)

start_btn = Button(250, 200, start_image)
exit_btn = Button(450, 200, exit_image)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 305:
                    player_grav = -21
                    jump_sound.play()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu = True


        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(varna_surf.get_rect(bottomright = (randint(900, 1100), 300)))
                else: 
                    obstacle_rect_list.append(balodis_surf.get_rect(bottomright = (randint(900, 1100), 240)))
            
            if event.type == varna_animation_timer:
                if varna_frame_index == 0: varna_frame_index = 1
                else: varna_frame_index = 0
                varna_surf = varna_frames[varna_frame_index]

            if event.type == balodis_animation_timer:
                if balodis_frame_index == 0: balodis_frame_index = 1
                else: balodis_frame_index = 0
                balodis_surf = balodis_frames[balodis_frame_index]

        

 
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        if main_menu == True:

            screen.blit(title_surface,(150,45))

            if exit_btn.draw():
                pygame.quit()
                exit()

            if start_btn.draw():
                main_menu = False

        else:

            # screen.blit(score_surf, score_rect)
            score = display_score()

            # varna_rect.x -=5
            # if varna_rect.right <= 0: varna_rect.left = 800
            # screen.blit(varna_surf,varna_rect)

            #player
            player_grav += 1
            player_rect.y += player_grav
            if player_rect.bottom >= 305: player_rect.bottom = 305
            player_animation()
            screen.blit(player_surface, player_rect)

            #obstacle movement
            obstacle_rect_list = obstacle_movement(obstacle_rect_list)

            # collisions
            game_active = collisions(player_rect, obstacle_rect_list)
        
    else:
        screen.fill((50,50,50))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (130, 300)
        player_grav = 0

        score_message = test_font.render(f'SCORE: {score}', False, (255,255,255))
        score_message_rect = score_message.get_rect(center = (400, 260))
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message, game_message_rect)
        screen.blit(game_quit_msg, game_quit_msg_rect)
                    
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)


    pygame.display.update()
    clock.tick(60)