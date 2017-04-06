from mesa import Agent
import numpy as np


class Exit(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.x, self.y = pos
        self.pos = pos

    def display(self):
        return {
            "Shape": "rect",
            "w": 1,
            "h": 1,
            "Filled": "true",
            "Layer": 0,
            "x": self.x,
            "y": self.y,
            "Color": "purple",
            "text_color": "red"
        }

    @property
    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def step(self):
        pass

    def advance(self):
        pass

    def check_out(self):
        pass
