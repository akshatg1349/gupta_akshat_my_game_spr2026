#game engine using template from Chris Bradfield's "Making Games with Python and Pygame"
#Main file responsible for game loop including input, update, and draw methods
'''
Main file responsible for game loop including update, input, and draw methods
'''
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from utils import *
vec = pg.math.Vector2

#import settings

#the game class will be instantiated in order to run the game
class Game:
    def __init__(self):
        pg.init()
        #setting up pygame screen using tuple value for width and height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        #setting up the title
        pg.display.set_caption(TITLE)
        #making a Clock class
        self.clock = pg.time.Clock()
        #the game will be running and playing
        self.running = True
        self.playing = True
        #self.load_data()
        #the cooldown is set to 5000 milliseconds
        self.game_cooldown = Cooldown(5000)
        #the cooldown is going to start
        self.game_cooldown.start()
        self.game_cooldown.ready()


    #a method is a function tied to a Class
    #load_data is defined
    def load_data(self):
        self.game_dir = path.dirname(__file__)
        #a map is being created
        self.map = Map(path.join(self.game_dir, 'level1.txt'))
        print('data is loaded')

    #function 'new' is defined
    def new(self):
        #the dad is being loaded
        self.load_data()
        #sprites, walls, and mobs are being created
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        #A player, mob, and coin are being added on the screen
        #self.player = Player(self, 15, 15)
        #self.mob = Mob(self, 4, 4)
        #self.coin = Coin(self, 4, 4)
        #self.wall = Wall(self, 4, 4)
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    #call class constructor without assigning variable...when
                    self.wall = Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    self.mob = Mob(self, col, row)
                if tile == 'C':
                    self.coin = Coin(self, col, row)
        self.run()
    #function run is defined
    def run(self):
        #check if game is running
        while self.running:
            #checking for FPS/1000 or seconds
            self.dt = self.clock.tick(FPS) / 1000
            #calling events, update, and draw
            self.events()
            self.update()
            self.draw()

    #function events is defined
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                #check if the game is playing
                if self.playing:
                    #the game is not playing
                    self.playing = False
                #the game is not running
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                #mouse input is received
                print("i can get mouse input")
                print(event.pos)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_k:
                    #keys are being pressed
                    print("i can determine when keys are pressed")
            if event.type == pg.KEYUP:
                if event.key == pg.K_k:
                    #keys are being relased
                    print("i can determine when keys are released")
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_w:
            #         self.player.rect.y += 5
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_a:
            #         self.player.rect.x -= 5
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_s:
            #         self.player.rect.y -= 5
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_d:
            #         self.player.rect.x += 5

    #function quit is created
    def quit(self):
        pass
    #function update is created
    def update(self):
        self.all_sprites.update()

    def draw(self):
        #the screen becomes blue
        self.screen.fill(BLUE)
        #The Hello World text is printed
        self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
        # self.draw_text(str(self.game_cooldown.time), 24, WHITE, WIDTH/2, HEIGHT/.5)
        self.draw_text(str(self.game_cooldown.ready()), 24, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text(str(self.player.pos), 24, WHITE, WIDTH/2, HEIGHT-TILESIZE*3)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    #the function draw_text is created with certain parameters
    def draw_text(self, text, size, color, x, y):
        #we have a font
        font_name = pg.font.match_font('arial')
        #we have a font size
        font = pg.font.Font(font_name, size)
        #we have text surface
        text_surface = font.render(text, True, color)
        #we have text_rect
        text_rect = text_surface.get_rect()
        #text_rect.midtop is based on x and y positions
        text_rect.midtop = (x,y)
        #self.scree.blit has two parameters, text_surface and text_rect
        self.screen.blit(text_surface, text_rect)
        
#if __name = "__main__" and creating a variable g
if __name__ == "__main__":
    g = Game()

while g.running:
    g.new()
#calling quit to quit the game
pg.quit()