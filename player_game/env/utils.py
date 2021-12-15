import pygame as pg
from pygame.locals import *
import os
from numpy import array

# sys.path.append(os.path.abspath(os.path.join('..')))

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
pg.init()
MENU_FONT = pg.font.SysFont("arial", 140)
OPTIONS_FONT = pg.font.SysFont("arial", 60)
SKINS_FONT = pg.font.SysFont("arial", 40)
SELECT_FONT = pg.font.SysFont("arial", 80)


def load_image(img_name, path=os.path.join(os.getcwd(), "assets"), res=None):
    if res:
        return pg.transform.scale(pg.image.load(os.path.join(path, img_name)), res)
    else:
        return pg.image.load(os.path.join(path, img_name))


RAT_IMAGE = load_image("spr_rat_right.png")
RAT_DOWN = load_image("spr_rat_down.png", res=(200, 200))
RAT_MISTERY = load_image("spr_mistery_rat.png", res=(200, 200))
REMY_DOWN = load_image("spr_remy_down.png", res=(200, 200))
CACHORRO_DOWN = load_image("spr_cachorro_down.png", res=(200, 200))


def draw_text(text, font, color, surface, x, y):
    draw_text = font.render(text, 1, color)
    if x == 8000:  # Gambiarra para colocar no meio da tela
        x = SCREEN_WIDTH // 2 - draw_text.get_width() / 2
    if y == 8000:
        y = SCREEN_HEIGHT // 2 - draw_text.get_height() / 2

    surface.blit(draw_text, (x, y))


def main_menu(surface, skin):

    cursor_pos = 0

    while True:
        surface.fill((0, 0, 0))

        draw_text("MAIZE", MENU_FONT, (255, 255, 255), surface, 8000, 50)
        draw_text("PLAY GAME", OPTIONS_FONT, (255, 255, 255), surface, 8000, 250)
        draw_text("EXTRAS", OPTIONS_FONT, (255, 255, 255), surface, 8000, 350)

        surface.blit(RAT_IMAGE, (320, cursor_pos * 100 + 235))

        pg.display.update()

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN and cursor_pos < 1:
                    cursor_pos += 1
                if event.key == pg.K_UP and cursor_pos > 0:
                    cursor_pos -= 1
                if event.key == pg.K_RETURN:
                    if cursor_pos == 0:
                        game_mode = mode_select(surface)
                        if game_mode >= 0:
                            return game_mode, skin

                    elif cursor_pos == 1:
                        skin = extras_menu(surface)

    return 0


def extras_menu(surface):

    cursor_pos = 0

    while True:
        surface.fill((0, 0, 0))

        draw_text("TUTORIAL", OPTIONS_FONT, (255, 255, 255), surface, 8000, 50)
        draw_text("SKINS", OPTIONS_FONT, (255, 255, 255), surface, 8000, 8000)
        draw_text("CREDITS", OPTIONS_FONT, (255, 255, 255), surface, 8000, 350)

        surface.blit(RAT_IMAGE, (320, cursor_pos * 100 + 135))

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
                        tutorial_menu(surface)
                    elif cursor_pos == 1:
                        return skins_menu(surface)
                    elif cursor_pos == 2:
                        credits_menu(surface)

                elif event.key == pg.K_ESCAPE:
                    return 0

    return 0


def tutorial_menu(surface):
    pass


def skins_menu(surface):
    cursor_pos = 0

    dog_guilherme = True

    file1 = open("player_game/levels.txt", "r")
    levels_completed = file1.readlines()
    file1.close()

    for i in levels_completed:
        if i == "0\n":
            dog_guilherme = False

    while True:
        surface.fill((0, 0, 0))

        draw_text("SELECT A SKIN", SELECT_FONT, (255, 255, 255), surface, 8000, 50)

        if cursor_pos == 0:
            draw_text("RATATAIL", SKINS_FONT, (138, 3, 3), surface, 112, 350)
            draw_text("REMY", SKINS_FONT, (255, 255, 255), surface, 445, 350)

            if not dog_guilherme:
                draw_text("?", SKINS_FONT, (255, 255, 255), surface, 790, 350)
            else:
                draw_text("CACHORRO", SKINS_FONT, (255, 255, 255), surface, 680, 350)
                draw_text(
                    "DE GUILHERME", SKINS_FONT, (255, 255, 255), surface, 645, 390
                )

        elif cursor_pos == 1:
            draw_text("RATATAIL", SKINS_FONT, (255, 255, 255), surface, 112, 350)
            draw_text("REMY", SKINS_FONT, (138, 3, 3), surface, 445, 350)

            if not dog_guilherme:
                draw_text("?", SKINS_FONT, (255, 255, 255), surface, 790, 350)
            else:
                draw_text("CACHORRO", SKINS_FONT, (255, 255, 255), surface, 680, 350)
                draw_text(
                    "DE GUILHERME", SKINS_FONT, (255, 255, 255), surface, 645, 390
                )

        elif cursor_pos == 2:
            draw_text("RATATAIL", SKINS_FONT, (255, 255, 255), surface, 112, 350)
            draw_text("REMY", SKINS_FONT, (255, 255, 255), surface, 445, 350)

            if not dog_guilherme:
                draw_text("?", SKINS_FONT, (138, 3, 3), surface, 790, 350)
            else:
                draw_text("CACHORRO", SKINS_FONT, (138, 3, 3), surface, 680, 350)
                draw_text("DE GUILHERME", SKINS_FONT, (138, 3, 3), surface, 645, 390)

        surface.blit(RAT_DOWN, (100, 140))
        surface.blit(REMY_DOWN, (400, 140))

        if not dog_guilherme:
            surface.blit(RAT_MISTERY, (700, 140))
        else:
            surface.blit(CACHORRO_DOWN, (700, 140))

        pg.display.update()

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT and cursor_pos < 2:
                    cursor_pos += 1
                if event.key == pg.K_LEFT and cursor_pos > 0:
                    cursor_pos -= 1
                if event.key == pg.K_RETURN and (
                    cursor_pos < 2 or dog_guilherme == True
                ):
                    return cursor_pos
                elif event.key == pg.K_ESCAPE:
                    return 0

    return 0


def credits_menu(surface):

    while True:
        surface.fill((0, 0, 0))

        draw_text("Tail :D", MENU_FONT, (255, 255, 255), surface, 8000, 100)

        pg.display.update()

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return 0


def mode_select(surface):

    cursor_pos = 0

    while True:
        surface.fill((0, 0, 0))

        surface.blit(RAT_IMAGE, (270, cursor_pos * 130 + 140))

        draw_text("Maze maker", SELECT_FONT, (255, 255, 255), surface, 8000, 150)
        draw_text("Player vs AI", SELECT_FONT, (255, 255, 255), surface, 8000, 280)

        pg.display.update()

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return -1
                if event.key == pg.K_RETURN:
                    return cursor_pos
                if event.key == pg.K_DOWN and cursor_pos < 1:
                    cursor_pos += 1
                if event.key == pg.K_UP and cursor_pos > 0:
                    cursor_pos -= 1


def load_image(img_name, path=os.path.join(os.getcwd(), "assets"), res=None):
    if res:
        return pg.transform.scale(pg.image.load(os.path.join(path, img_name)), res)
    else:
        return pg.image.load(os.path.join(path, img_name))


def get_grid(cursor):

    grid_list = [
        # 0 OK
        array(
            [
                [3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [3, 0, 3, 2, 0, 3, 0, 0, 3, 0],
                [3, 0, 3, 0, 0, 3, 0, 0, 3, 0],
                [3, 0, 3, 3, 0, 3, 0, 0, 3, 0],
                [3, 0, 3, 0, 0, 3, 3, 0, 3, 0],
                [3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [3, 0, 3, 0, 3, 3, 0, 0, 3, 0],
                [3, 0, 3, 0, 0, 3, 0, 3, 3, 0],
                [3, 0, 3, 0, 0, 3, 0, 0, 3, 0],
                [3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
            ]
        ),
        # 1 OK
        array(
            [
                [0, 0, 0, 0, 0, 0, 3, 3, 3, 0],
                [0, 3, 3, 3, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 3, 3, 3, 0, 3],
                [3, 0, 3, 3, 3, 3, 0, 0, 0, 3],
                [0, 0, 0, 0, 1, 3, 0, 0, 0, 3],
                [0, 3, 0, 0, 0, 3, 2, 3, 0, 3],
                [0, 0, 0, 3, 0, 3, 3, 3, 0, 3],
                [0, 0, 3, 3, 0, 0, 0, 0, 0, 0],
                [0, 3, 3, 0, 0, 0, 3, 3, 3, 0],
                [0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
            ]
        ).T,
        # 2 OK
        array(
            [
                [0, 3, 0, 3, 0, 3, 0, 3, 0, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 0, 3, 0, 3, 0, 3, 0, 3],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
                [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 0, 3, 0, 3, 0, 3, 0, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        ).T,
        # 3 OK
        array(
            [
                [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                [0, 0, 0, 0, 3, 0, 0, 0, 3, 0],
                [0, 0, 3, 3, 3, 3, 3, 0, 0, 2],
                [0, 3, 3, 0, 0, 0, 3, 3, 3, 3],
                [0, 3, 0, 0, 3, 0, 0, 0, 3, 0],
                [0, 0, 0, 3, 0, 0, 3, 0, 3, 0],
                [0, 0, 3, 0, 0, 3, 3, 0, 3, 0],
                [0, 3, 0, 0, 3, 3, 0, 0, 3, 0],
                [3, 0, 0, 3, 3, 0, 0, 3, 3, 0],
                [3, 1, 3, 3, 0, 0, 0, 0, 0, 0],
            ]
        ).T,
        # 4 OK
        array(
            [
                [0, 2, 3, 0, 0, 0, 0, 0, 0, 3],
                [0, 3, 0, 3, 3, 3, 0, 3, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
                [0, 3, 0, 0, 3, 3, 0, 0, 3, 0],
                [0, 3, 0, 3, 0, 0, 3, 0, 3, 0],
                [0, 3, 0, 0, 0, 0, 3, 0, 0, 0],
                [0, 3, 3, 3, 3, 3, 0, 0, 3, 0],
                [3, 0, 0, 0, 0, 0, 0, 0, 3, 0],
                [0, 3, 3, 3, 3, 3, 3, 3, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            ]
        ).T,
        # 5 OK
        array(
            [
                [3, 0, 0, 0, 0, 0, 3, 0, 2, 3],
                [0, 3, 0, 0, 3, 0, 0, 0, 3, 0],
                [0, 0, 3, 0, 0, 3, 3, 3, 0, 0],
                [3, 0, 0, 3, 0, 0, 3, 0, 0, 3],
                [0, 3, 0, 3, 0, 0, 0, 0, 3, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 3, 3],
                [0, 3, 0, 3, 0, 0, 3, 0, 0, 3],
                [0, 0, 3, 3, 0, 0, 3, 3, 0, 0],
                [0, 3, 3, 3, 0, 0, 3, 3, 3, 0],
                [3, 3, 3, 3, 1, 0, 3, 3, 3, 3],
            ]
        ).T,
        # 6 OK
        array(
            [
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 0, 3, 3, 3, 3, 3, 0, 0],
                [0, 3, 0, 0, 0, 0, 0, 3, 3, 0],
                [0, 0, 3, 3, 0, 3, 3, 3, 3, 0],
                [0, 3, 3, 3, 0, 3, 0, 2, 3, 0],
                [0, 0, 0, 0, 3, 3, 0, 3, 3, 0],
                [0, 3, 3, 3, 3, 3, 0, 3, 0, 0],
                [0, 3, 0, 0, 0, 0, 0, 3, 3, 0],
                [0, 3, 0, 3, 3, 3, 3, 3, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        ).T,
        # 7 OK,
        array(
            [
                [0, 3, 3, 0, 3, 0, 3, 0, 3, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [3, 3, 0, 3, 3, 0, 3, 3, 0, 3],
                [3, 0, 0, 3, 0, 0, 0, 3, 0, 0],
                [2, 3, 0, 3, 0, 3, 0, 3, 0, 0],
                [0, 0, 3, 0, 0, 3, 0, 3, 0, 3],
                [0, 3, 0, 3, 0, 3, 0, 0, 3, 3],
                [0, 0, 0, 0, 0, 3, 0, 0, 0, 3],
                [3, 3, 3, 3, 0, 3, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 3, 3, 0, 0, 0],
            ]
        ).T,
        # 8 OK
        array(
            [
                [0, 3, 3, 3, 3, 3, 3, 0, 0, 1],
                [0, 3, 0, 0, 0, 0, 3, 0, 0, 0],
                [0, 3, 0, 3, 3, 3, 3, 0, 3, 3],
                [0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
                [0, 3, 0, 3, 0, 0, 3, 3, 3, 0],
                [0, 3, 0, 3, 0, 0, 0, 0, 3, 0],
                [0, 3, 0, 3, 0, 0, 0, 3, 3, 0],
                [0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
                [0, 3, 0, 3, 3, 0, 3, 3, 3, 0],
                [0, 3, 0, 2, 3, 3, 3, 0, 0, 0],
            ]
        ),
    ]

    return grid_list[cursor]


def get_pos(cursor):

    pos_list = [
        (0, 9),
        (4, 4),
        (5, 5),
        (1, 9),
        (9, 9),
        (4, 9),
        (0, 0),
        (9, 1),
        (0, 9),
    ]

    return (
        pos_list[cursor][0],
        pos_list[cursor][1],
        pos_list[cursor][0],
        pos_list[cursor][1],
    )
