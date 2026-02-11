#pygame is imported as pg
import pygame as pg

#defining a class called Map
class Map:
    #defining function __init__ with parameter self
    #we are creating data for building the map using a list
    def __init__(self, filename):
        #self.data is the list with no items
        self.data = []
        #the file name is being opened
        #open a specific file and close it with 'with'
        with open(filename, 'rt') as f:
            for line in f:
                #stripped line is appended to data
                self.data.append(line.strip())
        #the tile width is the length of self.data of 0
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data[0])
        TILESIZE = 32
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

#class Cooldown is created
class Cooldown:
    def __init__(self, time):
        #the parameters of the above function are self and time
        #the starting time is 0
        self.start_time = 0
        #the time is being set
        self.time = time
        #the start function is defined with parameter self
    def start(self):
        self.start_time = pg.time.get_ticks()
        #the function ready is defined with parameter self
    def ready(self):
        #sets current_time to pg.time.get_ticks()
        current_time = pg.time.get_ticks()
        #if the difference between current and start time are greaer than self.time
        #return True
        if current_time - self.start_time >= self.time:
            self.start()
            return True
        #otherwise return false
        return False