from ctypes import Array

#importing pygame, Sprite, and path
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *
from os import path
from state_machine import *

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
from state_machine import *
from settings import *

class PlayerIdleState(State):
    def __init__(self, player):
        self.player = player
        self.name = "idle"

    def get_state_name(self):
        return "idle"

    def enter(self):
        self.player.image.fill(WHITE)
        print('enter player idle state')

    def exit(self):
        print('exit player idle state')

    def update(self):
        # print('updating player idle state...')
        self.player.image.fill(WHITE)
        keys = pg.key.get_pressed()
        if keys[pg.K_k]:
            print('transitioning to attack state...')
            self.player.state_machine.transition("attack")
            
class PlayerMoveState(State):
    def __init__(self, player):
        self.player = player
        self.name = "move"

    def get_state_name(self):
        return "move"

    def enter(self):
        self.player.image.fill(WHITE)
        print('enter player move state')

    def exit(self):
        print('exit player move state')

    def update(self):
        # print('updating player move state...')
        self.player.image.fill(GREEN)
        keys = pg.key.get_pressed()
  
#a class Player with the argument Sprite
class Player(Sprite):
    #the arguments here are self, game, x, and y
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        #the game is set
        self.game = game
        #we have a spritesheet
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        #we load images
        self.load_images()
        #the images are being loaded
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.image.set_colorkey(BLACK)
        #the sprite is white
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        #the position of the sprite is (x,y) times tile size
        self.pos = vec(x,y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT
        #self.jumping and self.moving are set to False
        self.jumping = False
        self.moving = False
        #the last update variable is set to 0
        self.last_update = 0
        #current frame variable is set to 0
        self.current_frame = 0
        self.state_machine = StateMachine()
        self.states: Array[State] = [PlayerIdleState(self), PlayerMoveState(self)]
        self.state_machine.start_machine(self.states)

    
    def update(self):
        # print("player updating")
        self.state_machine.update()
        #you get_keys, check state, and animate
        self.get_keys()
        self.state_check()
        self.animate()
        #adjusts the positions accordingly
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.collide_with_stuff(self.game.all_mobs, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center

    #defining a function called get_keys
    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        #if conditions are created for what happens if we press w,a,s,d, or f
        #the code inside is based on how coordinates change when the object moves
        if keys[pg.K_f]:
            print('fired a projectile')
            p = Projectile(self.game, self.rect.x, self.rect.y)
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
    #defining a function called load_image
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE), 
                                self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)]
        self.moving_frames = [self.spritesheet.get_image(TILESIZE*2,0,TILESIZE, TILESIZE), 
                                self.spritesheet.get_image(TILESIZE*3,0,TILESIZE, TILESIZE)]
        #the frame is set to black
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        #the frame is set to black
        for frame in self.moving_frames:
            frame.set_colorkey(BLACK)

    #animating our sprite
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving:
            #check if now minus self.last_update is greater than 350
            if now - self.last_update > 350:
                print(now - self.last_update)
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.moving:
            #check if now minus self.last_update is greater than 350
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
                bottom = self.rect.bottom
                self.image = self.moving_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def state_check(self):
        if self.vel != vec(0,0):
            self.moving = True
        else:
            self.moving = False

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Mob":
                print("You lose")
            if str(hits[0].__class__.__name__) == "Coin":
                print("You gained speed")
                self.game.pickup_snd.play("pickup.wav")


    #update function is created with parameter self
    def update(self):
        #we are using the get_keys function on self
        self.get_keys()
        self.state_check()
        self.animate()
        #the rect center is equal to the position
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        #calling collide_with_walls function relative to x position
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        #calling collide_with_walls function relative to y position
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.centerx - self.hit_rect.centery

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

#the class Mob is created
class Mob(Sprite):
    #__init__ function is defined
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
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
            print("Your new speed is " + str(self.speed))

        hits = pg.sprite.spritecollide(self, self.game.all_coins, False)
        if hits:
            print("You gained speed")
            #the speed is increased by 10
            self.speed += 5
            print("Your new speed is " + str(self.speed))

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
            self.game.won = True

#the class Projectile is created
class Projectile(Sprite):
    #__init__ function is defined
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #Projectile is made red
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(1,0)
        self.pos = vec(x,y) * TILESIZE
        #the speed is set to 10
        self.speed = 10
        print("i'm a real projectile")
    #update function is defined
    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        print(hits)
        print(hits)
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
        self.rect.center = self.pos

    def update(self):
        pass


class EffectTrail(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE,TILESIZE), pg.SRCALPHA)
        self.alpha = 255
        self.image.fill((255,255,255,255))
        self.rect = self.image.get_rect()
        self.cd = Cooldown(10)
        self.rect.x = x
        self.rect.y = y
        # coin behavior
        self.scale_x = 32
        self.scale_y = 32
    def update(self):
        if self.alpha <= 100:
            self.kill()
        self.image.fill((255,255,255,self.alpha))
        
        if self.cd.ready():
            self.scale_x -=1
            self.scale_y -=1
            print("I'm ready")
            self.alpha -= 5
            new_image = pg.transform.scale(self.image, (self.scale_x, self.scale_y))
            self.image = new_image
    #update function is defined with parameter self
    def update(self):
        pass
