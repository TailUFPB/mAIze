import os 
import pygame as pg

def load_image(img_name, path = "/home/moises/Documents/area_tb/TAIL/RL/mAIze/assets", res = None):
    if res:
        return pg.transform.scale(pg.image.load(os.path.join(path, img_name)), res)
    else:
        return pg.image.load(os.path.join(path, img_name))