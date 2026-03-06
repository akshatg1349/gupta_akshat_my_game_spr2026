#is_log_enabled is a boolean that is set to False
is_log_enabled: bool = False
#we are defining a class called State
class State():
    #functions such as __init__, enter, exit, and update all need only a pass keyword
    #get_state_name just returns ""
    def __init__(self):
        pass
    def enter(self):
        pass
    def exit(self):
        pass
    def update(self):
        pass
    def get_state_name(self):
        return ""
#class StateMachine is created
class StateMachine():
    def __init__(self):
        # set up state machine with empty states and a default state
        self.current_state = State()
        # dictionary of states for easy access during transitions
        self.states = {}
        print(self.states)
    
    # takes in a list of states to initialize the state machine with, and sets the first state in the list as the default state
    def start_machine(self, init_states = [State]):
        # add states to state machine's state dictionary for easy access during transitions
        for state in init_states:
            print(state.get_state_name())
            self.states[state.get_state_name()] = state
            print(self.states)

        # set current state to first state in list of states passed into start_machine function
        self.current_state = init_states[0]
        #if is_log_enabled is True then the state machine will be starting
        if is_log_enabled:
            print('starting state machine...')

        self.current_state.enter()
        print("state machine started with state:", self.current_state.get_state_name())

    #function called update is defined with self parameter
    def update(self):
        #if self.current_state is None than there is no current state as printed
        if self.current_state == None:
            print('no current state...')
        else:
            self.current_state.update()
    #function called transition is defined      
    def transition(self, new_state_name):
        new_state: State = self.states.get(new_state_name)
        self.current_state_name = self.current_state.get_state_name()
        if new_state == None:
            print("attempting to transition to non existent state")
        elif new_state != self.current_state:
            self.current_state.exit()
            #if is_log_enabled is True than the state will be exiting
            if is_log_enabled:
                print('exiting state...')
            
            self.current_state = self.states[new_state.get_state_name()]
            #a new state will be entered here
            if is_log_enabled:
                print('entering new state...')

            self.current_state.enter()
        #attempt to transition to a new state since the current state had been ignored if is_log_enabled is True
        else:
            if is_log_enabled:
                print("attempt to transition to " + new_state_name + " ignored since it is the current state...")
    


