import os
import sys

import pygame
import pygame_gui
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
    response = requests.get("http://static-maps.yandex.ru/1.x/", params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    with open(map_file, "wb") as file:
        file.write(response.content)


map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((720, 500))
manager = pygame_gui.UIManager((720, 500))
button_map = pygame_gui.elements.UIButton(  # схема
    relative_rect=pygame.Rect(610, 50, 100, 30),
    text="Схема",
    manager=manager
)
button_sat = pygame_gui.elements.UIButton(  # спутник
    relative_rect=pygame.Rect(610, 100, 100, 30),
    text="Спутник",
    manager=manager
)
button_skl = pygame_gui.elements.UIButton(  # гибрид
    relative_rect=pygame.Rect(610, 150, 100, 30),
    text="Гибрид",
    manager=manager
)
clock = pygame.time.Clock()
while True:
    time_delta = clock.tick(60) / 1000.0
    screen.fill((255, 255, 255))  # белый фон
    screen.blit(pygame.image.load(map_file), (0, 50))
    for event in pygame.event.get():
        if event.type == QUIT:
            os.remove(map_file)
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                map_zoom += 1
                new_map()
            elif event.key == pygame.K_PAGEDOWN:
                map_zoom -= 1
                new_map()
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_map:
                    map_l = "map"
                if event.ui_element == button_sat:
                    map_l = "sat"
                if event.ui_element == button_skl:
                    map_l = "skl"
                new_map()
        manager.process_events(event)
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()
