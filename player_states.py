#we are importing from state_machine and settings
from state_machine import *
from settings import *
#the class PlayerIdleState is defined with parameter State
class PlayerIdleState(State):
    #function __init__ is defined with parameters self and player
    def __init__(self, player):
        #self.player will equal player
        self.player = player
        #the self.name is set to "idle"
        self.name = "idle"
    #defining a function called get_state_name with one parameter self
    def get_state_name(self):
        #"idle" is always returned from this function
        return "idle"
    #defining a function called enter with one parameter self
    def enter(self):
        #the player image is set to white
        self.player.image.fill(WHITE)
        print('enter player idle state')
    #defining a function called exit with parameter self
    def exit(self):
        print('exit player idle state')
    #defining update function with parameter self
    def update(self):
        # print('updating player idle state...')
        self.player.image.fill(WHITE)
        keys = pg.key.get_pressed()
        # if keys[pg.K_k]:
        #     print('transitioning to attack state...')
        #     self.player.state_machine.transition("attack")
#new class called PlayerMoveState with parameter State      
class PlayerMoveState(State):
    #defining __init__ with self and player as parameters
    def __init__(self, player):
        #self.player is set to player
        self.player = player
        #self.name is set to "move"
        self.name = "move"
    #defining get_state_name function and returning the string "move"
    def get_state_name(self):
        return "move"
    #defining the enter function with a parameter self
    def enter(self):
        self.player.image.fill(WHITE)
        print('enter player move state')
    #defining the exit function with a parameter self
    def exit(self):
        print('exit player move state')
    #defining a function called update
    def update(self):
        # print('updating player move state...')
        self.player.image.fill(GREEN)
        #keys is based on the keys pressed
        keys = pg.key.get_pressed()
  