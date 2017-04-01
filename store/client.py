from collections import Counter

from mesa import Agent
import random

from store import utils
from store.decisionEngine import DecisionEngine


class Client(Agent):

    def __init__(self, pos, items_to_get, model):
        super().__init__(pos, model)
        self.mind = DecisionEngine(model)
        self.x, self.y = pos
        self.pos = pos
        self.need = items_to_get
        self.have = Counter()
        self.display = {
            "Shape": "rect",
            "text": str(len(self.need)),
            "w": 1,
            "h": 1,
            "Filled": "false",
            "Layer": 0,
            "x": self.x,
            "y": self.y,
            "Color": "white",
            "text_color": "red"
        }

    @property
    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def step(self):
        # for neighbor in self.neighbors:
        self.advance()

    def advance(self):
        moves = [pos for pos in self._possible_moves() if self.model.grid.is_cell_empty(pos)] + [self.pos]
        next_pos = self.mind.make_decision(self.pos, moves)
        assert(next_pos in moves)
        if next_pos is not self.pos:
            print("Client moving to {} from {}".format(next_pos, self.pos))
            self.model.grid.move_agent(self, next_pos)
            self.x, self.y = self.pos
        # else:
            # print("Client is standing at {}".format(self.pos))

    def _possible_moves(self):
        return utils.places_to_move(self.x, self.y, self.model.width, self.model.height)

    def check_out(self):
        print("Agent removed")
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)
