import pygame as pg
from pygame.locals import *

from player import Player
from grid import Grid

pg.init()
clock = pg.time.Clock()

pg.display.set_caption("rat")

SCREEN_WIDTH = 1040
SCREEN_HEIGHT = 700
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


maze = Grid(20, 20, SCREEN_WIDTH, SCREEN_HEIGHT)
rat = Player(maze)

game_running = True
while(game_running):
    screen.fill((200,200,200))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_running = False
        if event.type ==  KEYDOWN:
            if event.key == K_DOWN:
                rat.move_down()
            if event.key == K_UP:
                rat.move_up()
            if event.key == K_LEFT:
                rat.move_left()
            if event.key == K_RIGHT:
                rat.move_right()
        if event.type == MOUSEBUTTONDOWN:
            mouse_position = pg.mouse.get_pos()
            maze.set_obstacle_on_click(mouse_position[0], mouse_position[1])
    
    rat.update_player()
    maze.draw_grid(screen) 

    pg.display.update()
    clock.tick(60)
