#importing pygame and Sprite
import pygame as pg
from pygame.sprite import Sprite
from settings import *

#vec is given a specific value pg.math.Vector2
vec = pg.math.Vector2

#a class Player with the argument Sprite
class Player(Sprite):
    #the arguments here are self, game, x, and y
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #the sprite is white
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        #the position of the sprite is (x,y) times tile size
        self.pos = vec(x,y) * TILESIZE
    #the player's position is being updated
    #it is moving to the right by 1 pixel every time

    #defining a function called get_keys
    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        #if conditions are created for what happens if we press w,a,s,or d
        #the code inside is based on how coordinates change when the object moves
        if keys[pg.K_a]:
            self.vel.x = -2 * PLAYER_SPEED
        if keys[pg.K_w]:
            self.vel.y = -2 * PLAYER_SPEED
        if keys[pg.K_s]:
            self.vel.y = 2 * PLAYER_SPEED
        if keys[pg.K_d]:
            self.vel.x = 2 * PLAYER_SPEED
        #velocity is multiplied by 0.7071
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
    #update function is created with parameter self
    def update(self):
        self.get_keys()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
#the class Mob is created
class Mob(Sprite):
    #__init__ function is defined
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #Mob is made red
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(1,0)
        self.pos = vec(x,y) * TILESIZE
        #the speed is set to 5
        self.speed = 5
    #update function is defined
    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            print("collided")
        
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.pos.y += TILESIZE
        self.pos += self.speed * self.vel
        self.rect.center = self.pos
#class Coin is being created
class Coin(Sprite):
    # function __init__ is defined with parameters self, game, x, and y
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #the coin is yellow
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        #its position is based on x and y positions and tile size
        self.pos = vec(x,y) * TILESIZE
    #update function is defined with parameter self
    def update(self):
        pass
#class Wall is being created
class Wall(Sprite):
    #function __init__ is defined
    def __init__(self, game, x, y):
        #the groups have all sprites and all walls
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        #self.game is set to game
        self.game = game
        #self.image is based on tile size
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #The wall color is green
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        #the velocity is set to vec(0,0)
        self.vel = vec(0,0)
        #the position is based on x, y, and tile size
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
    #function update is defined
    def update(self):
        pass