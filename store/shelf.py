from mesa import Agent
import random


class Shelf(Agent):
    def __init__(self, pos, category, model):
        super().__init__(pos, model)
        self.x, self.y = pos
        self.category = category

    def display(self):
        return {
            "Shape": "rect",
            "text": self.category,
            "w": 1,
            "h": 1,
            "Filled": "false",
            "Layer": 0,
            "x": self.x,
            "y": self.y,
            "Color": "black",
            "text_color": "white"
        }
    @property
    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def step(self):
        pass

    def advance(self):
        pass

