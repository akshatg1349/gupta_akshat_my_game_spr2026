#pygame is being imported as pg
import pygame as pg

#settng up pygame
WIDTH = 800
HEIGHT = 600
TITLE = "My cool game"
FPS = 60
TILESIZE = 32

#player values
PLAYER_SPEED = 200
PLAYER_HIT_RECT = pg.Rect(0,0,TILESIZE,TILESIZE)

#Color values
#tuple storing RGB values
BLUE = (0,0,255)
WHITE = (255,255,255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0,255,0)
