from collections import Counter

from mesa import Agent
import random

from store import utils
from store.decisionEngine import DecisionEngine


class Client(Agent):
    MIN_PICK_LENGTH = 2
    MAX_PICK_LENGTH = 8

    def __init__(self, pos, items_to_get, model):
        super().__init__(pos, model)
        self.mind = DecisionEngine(model)
        self.x, self.y = pos
        self.pos = pos
        self.need = items_to_get
        self.have = Counter()
        self.picking = (None, 0)

    def display(self):
        return {
            "Shape": "rect",
            "text": self.need_count(),
            "w": 1,
            "h": 1,
            "Filled": "true",
            "Layer": 0,
            "x": self.x,
            "y": self.y,
            "Color": "white" if not self.picking_items() else "yellow",
            "text_color": "red"
        }

    @property
    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def picking_items(self):
        return self.picking[0] is not None

    def done(self):
        for n in self.need.most_common():
            if n[1] > 0:
                return False
        return True

    def need_count(self):
        total = 0
        for n in self.need.most_common():
            total += n[1]
        return total

    def step(self):
        self.advance()

    def advance(self):
        if self.picking_items():
            if self.picking[1] > 0:
                self.picking = (self.picking[0], self.picking[1] - 1)
            else:
                print("Client picked up an item of category {}".format(self.picking[0]))
                self.need[self.picking[0]] -= 1
                self.have[self.picking[0]] += 1
                self.picking = (None, 0)
        elif not self.using_shelves():
            moves = [pos for pos in self._possible_moves() if self.model.grid.is_cell_empty(pos)] + [self.pos]
            next_pos = self.mind.make_decision(self.pos, moves)
            assert (next_pos in moves)
            if next_pos is not self.pos:
                # print("Client moving to {} from {}".format(next_pos, self.pos))
                self.model.grid.move_agent(self, next_pos)
                self.x, self.y = self.pos
                # else:
                # print("Client is standing at {}".format(self.pos))

    def using_shelves(self):
        for n in self.neighbors:
            if hasattr(n, "category") and n.category in self.need and self.need[n.category] > 0:
                print("Client started picking an item of category {}".format(n.category))
                self.picking = (n.category, random.randrange(self.MIN_PICK_LENGTH, self.MAX_PICK_LENGTH))
                return True
        return False

    def _possible_moves(self):
        return utils.places_to_move(self.x, self.y, self.model.width, self.model.height)

    def check_out(self):
        if self.done():
            print("Agent removed")
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
