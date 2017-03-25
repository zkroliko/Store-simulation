from mesa import Agent
import random

from store import utils
from store.client import Client


class Entrance(Agent):

    PROBABILITY = 0.1

    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.x, self.y = pos
        self.pos = pos
        self.display = {
            "Shape": "rect",
            "w": 1,
            "h": 1,
            "Filled": "true",
            "Layer": 0,
            "x": self.x,
            "y": self.y,
            "Color": "blue",
        }

    @property
    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def step(self):
        if random.random() < self.PROBABILITY:
            self.create_client()

    def advance(self):
        pass

    def create_client(self):
        positions = [pos for pos in self._places_to_create() if self.model.grid.is_cell_empty(pos)]
        if len(positions) > 0:
            pos = random.choice(positions)
            cell = Client(pos, self.model)
            self.model.grid.place_agent(cell, cell.pos)
            self.model.schedule.add(cell)
            print("Client entered at {}".format(pos))
        else:
            print("Entrance blocked at ({},{})".format(self.x, self.y))

    def _places_to_create(self):
        return utils.places_to_move(self.x, self.y, self.model.width, self.model.height)
