from mesa import Agent


class Cell(Agent):
    '''Represents a single ALIVE or DEAD cell in the simulation.'''

    DEAD = 0
    ALIVE = 1

    def __init__(self, pos, model):
        '''
        Create a cell, in the given state, at the given x, y position.
        '''
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state =  self.ALIVE
        self._nextState = self.state

    @property
    def isAlive(self):
        return self.state == self.ALIVE

    @property
    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def step(self):
        #for neighbor in self.neighbors:
        self.advance()
				
				

    def advance(self):
        self.x = self.x + 1
        self.y = self.y + 1
        self.model.grid.move_agent(self,((self.x+1)%self.model.width,(self.y+1)%self.model.height))
