import os
import sys

import pygame
from pygame.locals import *
import requests


map_zoom = 10
map_ll = '30.315831,59.939090'
map_l = 'map'
map_key = ''
map_request = f"https://static-maps.yandex.ru/1.x/?z={map_zoom}&ll={map_ll}&l={map_l}"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)


def new_map():

    params = {
        "ll": f"{map_ll.split(',')[0]},{map_ll.split(',')[1]}",
        "l": map_l,
        'z': map_zoom
    }
    print(params)
    
    response = requests.get("http://static-maps.yandex.ru/1.x/", params=params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))


map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            os.remove(map_file)
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if map_zoom < 19:
                    map_zoom += 1
                    new_map()
            elif event.key == pygame.K_PAGEDOWN:
                if map_zoom > 1:
                    map_zoom -= 1
                    new_map()
            elif event.key == pygame.K_RIGHT:
                a = map_ll.split(',')[0]
                b = map_ll.split(',')[1]
                if float(a) + 1 < 180:
                    map_ll = f'{float(a) + 1},{b}'
                    new_map()
            elif event.key == pygame.K_LEFT:
                a = map_ll.split(',')[0]
                b = map_ll.split(',')[1]
                if float(a) - 1 > 0:
                    map_ll = f'{float(a) - 1},{b}'
                    new_map()
            elif event.key == pygame.K_DOWN:
                a = map_ll.split(',')[0]
                b = map_ll.split(',')[1]
                if float(b) - 1 > -85:
                    map_ll = f'{a},{float(b) - 1}'
                    new_map()
            elif event.key == pygame.K_UP:
                a = map_ll.split(',')[0]
                b = map_ll.split(',')[1]
                if float(b) + 1 < 85:
                    map_ll = f'{a},{float(b) + 1}'
                    new_map()
    pygame.display.flip()

