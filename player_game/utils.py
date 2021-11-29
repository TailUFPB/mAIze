import pygame as pg
from pygame.locals import *
import os
from numpy import array

#sys.path.append(os.path.abspath(os.path.join('..')))

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
pg.init()
MENU_FONT = pg.font.SysFont('comicsans', 140)
OPTIONS_FONT = pg.font.SysFont('comicsans', 60)
SELECT_FONT = pg.font.SysFont('comicsans', 80)

RAT_IMAGE = pg.image.load(os.path.join(os.getcwd(),'assets', 'spr_rat_right.png'))

def draw_text(text, font, color, surface, x, y):
    draw_text = font.render(text, 1, color)
    if x == 8000: #Gambiarra para colocar no meio da tela
        x = SCREEN_WIDTH//2 - draw_text.get_width()/2
    if y == 8000:
        y = SCREEN_HEIGHT//2 - draw_text.get_height()/2
    
    surface.blit(draw_text, (x, y))

def main_menu(surface):

    cursor_pos = 0

    while True:
        surface.fill((0,0,0))
        
        draw_text('MAIZE', MENU_FONT, (255,255,255), surface, 8000, 50)
        draw_text('PLAY GAME', OPTIONS_FONT, (255,255,255), surface, 8000, 250)
        draw_text('OPTIONS', OPTIONS_FONT, (255,255,255), surface, 8000, 320)
        draw_text('CREDITS', OPTIONS_FONT, (255,255,255), surface, 8000, 390)

        surface.blit(RAT_IMAGE, (320, cursor_pos*70 + 235))

        pg.display.update()

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN and cursor_pos < 2:
                    cursor_pos += 1
                if event.key == pg.K_UP and cursor_pos > 0:
                    cursor_pos -= 1
                if event.key == pg.K_RETURN:
                    if cursor_pos == 0:
                        game_mode = mode_select(surface)
                        if game_mode >= 0:
                            return game_mode

                    if cursor_pos == 2:
                        credits_menu(surface)
    
    return 0

def credits_menu(surface):

    while True:
        surface.fill((0,0,0))
        
        draw_text('Tail :D', MENU_FONT, (255,255,255), surface, 8000, 100)

        pg.display.update()

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return 0

def mode_select(surface):
    
    cursor_pos = 0

    while True:
        surface.fill((0,0,0))

        surface.blit(RAT_IMAGE, (270, cursor_pos*130 + 140))
        
        draw_text('Maze maker', SELECT_FONT, (255,255,255), surface, 8000, 150)
        draw_text('Player vs AI', SELECT_FONT, (255,255,255), surface, 8000, 280)

        pg.display.update()

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return -1
                if event.key == pg.K_RETURN:
                    return cursor_pos
                if event.key == pg.K_DOWN and cursor_pos < 1:
                    cursor_pos += 1
                if event.key == pg.K_UP and cursor_pos > 0:
                    cursor_pos -= 1

def load_image(img_name, path = os.path.join(os.getcwd(),"assets"), res = None):
    if res:
        return pg.transform.scale(pg.image.load(os.path.join(path, img_name)), res)
    else:
        return pg.image.load(os.path.join(path, img_name))

def get_grid(cursor):

    grid_list = [array([   [0, 0, 2, 3, 0, 0, 0, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
                           [5, 4, 3, 3, 0, 3, 3, 3, 0, 0],
                           [3, 3, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 3, 0, 0]]).T,

            array([        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 3, 3, 3, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 3, 0, 0]]).T,

            array([        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 3, 3, 3, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 3, 0, 0]]).T,

            array([        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 3, 3, 3, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 3, 0, 0]]).T,

            array([        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 3, 3, 3, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 3, 0, 0]]).T,

            array([        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 3, 3, 3, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 3, 0, 0]]).T,

            array([        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 3, 3, 3, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 3, 0, 0]]).T,

            array([        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 3, 3, 3, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 3, 0, 0]]).T,

            array([        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 3, 3, 3, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 3, 0, 0]]).T,]

    return grid_list[cursor], grid_list[cursor]

def get_pos(cursor):

    pos_list = [(0,0),
                (0,0),
                (0,0),
                (0,0),
                (0,0),
                (0,0),
                (0,0),
                (0,0),
                (0,0),
                (0,0),]

    return pos_list[cursor][0], pos_list[cursor][1], pos_list[cursor][0], pos_list[cursor][1]
