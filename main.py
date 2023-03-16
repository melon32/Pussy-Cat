import pygame
from sys import exit
from random import randint

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


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Cat Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 40)
game_active = True
start_time = 0
score = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# score_surf = test_font.render('Score: ', False, 'Black')
# score_rect = score_surf.get_rect(center = (400,50))

#obstacles
varna_surf = pygame.image.load('graphics/varna/varna1.png').convert_alpha()
balodis_surf = pygame.image.load('graphics/balodis/balodis1.png').convert_alpha()

obstacle_rect_list = []

player_surface = pygame.image.load('graphics/player/player1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))
player_grav = 0

player_stand = pygame.image.load('graphics/player/angry.png').convert_alpha()
player_stand = pygame.transform.scale(player_stand, (150, 150))
player_stand_rect = player_stand.get_rect(center = (400, 100))

game_name = test_font.render('Cat Runner', False, (255,255,255))
game_name_rect = game_name.get_rect(center = (400, 200))

game_message = test_font.render('Press space to run', False, (115,0,0))
game_message_rect = game_message.get_rect(center = (400, 350))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos)and player_rect.bottom >= 300:
                    player_grav = -21

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_grav = -21
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(varna_surf.get_rect(bottomright = (randint(900, 1100), 300)))
            else: 
                obstacle_rect_list.append(balodis_surf.get_rect(bottomright = (randint(900, 1100), 240)))

 
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        # screen.blit(score_surf, score_rect)
        score = display_score()

        # varna_rect.x -=5
        # if varna_rect.right <= 0: varna_rect.left = 800
        # screen.blit(varna_surf,varna_rect)

        #player
        player_grav += 1
        player_rect.y += player_grav
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collisions
        game_active = collisions(player_rect, obstacle_rect_list)
        
    else:
        screen.fill((50,50,50))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_grav = 0

        score_message = test_font.render(f'SCORE: {score}', False, (255,255,255))
        score_message_rect = score_message.get_rect(center = (400, 270))
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message, game_message_rect)
                    
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)

    # 2:50:54