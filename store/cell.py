from mesa import Agent
import random


class Cell(Agent):

    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.x, self.y = pos

    @property
    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def step(self):
        #for neighbor in self.neighbors:
        self.advance()

    def advance(self):
        self.x = self.x + random.randint(-1,1)
        self.y = self.y + random.randint(-1,1)
        self.model.grid.move_agent(self,((self.x+1)%self.model.width,(self.y+1)%self.model.height))
