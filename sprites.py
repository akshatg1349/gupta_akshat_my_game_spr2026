#importing pygame and Sprite
import pygame as pg
from pygame.sprite import Sprite
from settings import *

#vec is given a specific value pg.math.Vector2
vec = pg.math.Vector2

#defining a function where two items are colliding
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)
#this function checks for x and y collision in sequence and sets the position based on collision direction
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        #a variable hits is declared to say how many hits a sprite went through
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            #if hits[0].rect.centerx is greater than sprite.hit_rect.centerx
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                '''then we set the x position of the sprite to hits[0].rect.left minus
                sprite.hit_rect.width / 2
                '''
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
                if hits[0].rect.centerx < sprite.hit_rect.centerx:
                    #the collision happens in the right
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        #a variable hits is declared to say how many hits a sprite went through
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            print("collided with wall from y dir")
            #ifhits[0].rect.centery is greater than sprite.hit_rect.centerx
            if hits[0].rect.centery > sprite.hit_rect.centery:
                '''then we set the y position of the sprite to hits[0].rect.top minus
            sprite.hit_rect.width / 2
            '''
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                #the collision happens in the bottom
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

#a class Player with the argument Sprite
class Player(Sprite):
    #the arguments here are self, game, x, and y
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.player_group
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #the sprite is white
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        #the position of the sprite is (x,y) times tile size
        self.pos = vec(x,y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT


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
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.centerx - self.hit_rect.centery
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
        #the speed is set to 10
        self.speed = 10
    #update function is defined
    def update(self):

        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            print("collided")
            #the speed is subtracted by 1
            self.speed -= 1

        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.pos.y += TILESIZE
            self.pos += self.speed * self.vel
            self.rect.center = self.pos

        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.pos.y += TILESIZE
        self.pos += self.speed * self.vel
        self.rect.center = self.pos

        if self.pos.y >= HEIGHT:
            print("You Win!")
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
        self.rect.center = self.pos
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
        self.image = game.wall_img
        #self.image is based on tile size
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        #The wall color is green
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        #the velocity is set to vec(0,0)
        self.vel = vec(0,0)
        #the position is based on x, y, and tile size
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
    #function update is defined
    def update(self):
        pass
