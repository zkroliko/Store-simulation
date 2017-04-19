from collections import Counter

from mesa import Agent

from store import utils
from store.decisionEngine import DecisionEngine
from store.exitAction import ExitAction
from store.pickAction import PickAction


class Client(Agent):
    MIN_PICK_LENGTH = 2
    MAX_PICK_LENGTH = 8

    def __init__(self, pos, items_to_get, model):
        super().__init__(pos, model)
        self.mind = DecisionEngine(self)
        self.x, self.y = pos
        self.pos = pos
        self.need = items_to_get
        self.have = Counter()
        self.action = None

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
            "Color": "white" if not self.action else "yellow",
            "text_color": "red"
        }

    @property
    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    @property
    def surround(self):
        return self.model.grid.iter_neighbors((self.x, self.y), moore=True, radius=15)

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
        pass

    def advance(self):
        if self.action:
            self.action.step()
        elif not self.using_shelves() and not self.using_exits():
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
        if not self.done() and not self.action:
            for n in self.neighbors:
                if hasattr(n, "category") and n.category in self.need and self.need[n.category] > 0:
                    self.action = PickAction(self, n)
                    return True
        return False

    def using_exits(self):
        if self.done() and not self.action:
            for n in self.neighbors:
                if hasattr(n, "check_out"):
                    self.action = ExitAction(self, n)
                    return True
        return False

    def _possible_moves(self):
        return utils.places_to_move(self.x, self.y, self.model.width, self.model.height)

