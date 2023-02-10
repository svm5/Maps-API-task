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
    pygame.display.flip()

