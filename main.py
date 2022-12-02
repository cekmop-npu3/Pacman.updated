import pygame
import sys
import random
from character import Hero, Enemy, AStar
from map_opener import Map
pygame.init()

window = pygame.display.set_mode((800, 800))
images = {'1': [pygame.image.load('images/wall.png').convert_alpha(), []]}
create_map = Map(window, 'map.txt', images)
hero = Hero(window, 'images/pacman_eating/0.png', 2, 0, [pygame.image.load(f'images/pacman_eating/{i}.png').convert_alpha() for i in range(3)], create_map.pos)
path = AStar(create_map.map)
pathes = [[(1, 1), (1, 23), (23, 23), (23, 1)], [(14, 1), (5, 6), (11, 18), (3, 23)], [(1, 6), (7, 10), (17, 1), (19, 20)]]
enemies = [Enemy(window, 'images/mob_red/0.png', 2, {i: pygame.image.load(f'images/{name}/{i}.png').convert_alpha() for i in range(-90, 270, 90)}, pos) for name, pos in zip(['mob_red', 'mob_pink'], create_map.poses)]
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: sys.exit()
            for key in (move_buttons := {pygame.K_d: 0, pygame.K_a: 180, pygame.K_w: -90, pygame.K_s: 90}):
                if event.key == key: hero.rotation = [move_buttons.get(key,0)]

    window.fill((0, 0, 0))
    pygame.display.set_caption(str(int(clock.get_fps())))
    create_map.draw()
    hero.move(create_map.map)
    random.shuffle(pathes)
    for count, enemy in enumerate(enemies):enemy.get_path(pathes[count], path); enemy.move(); enemy.draw()
    pygame.display.update()
    clock.tick(60)
