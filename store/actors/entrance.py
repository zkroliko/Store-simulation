import random
from collections import Counter

from mesa import Agent

from store.utils import moveUtils
from store.actors.client import Client


class Entrance(Agent):
    MIN_ITEMS = 1
    MAX_ITEMS = 10

    def __init__(self, pos, model, entry_events):
        super().__init__(pos, model)
        self.x, self.y = pos
        self.pos = pos
        self.arrival_events = sorted(entry_events)
        self.waiting_to_enter = 0
        self.curr_event_index = 0

    def display(self):
        return {
            "Shape": "rect",
            "w": 1,
            "h": 1,
            "Filled": "false",
            "Layer": 0,
            "x": self.x,
            "y": self.y,
            "Color": "blue",
            "text": self.waiting_to_enter,
            "text_color": "white"
        }

    def gen_item_list(self):
        count = random.randrange(self.MIN_ITEMS, self.MAX_ITEMS)
        items = Counter()
        for i in range(count):
            items[random.choice(self.model.categories)] += 1
        return items

    @property
    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def step(self):
        self.asses_entry_events()
        self.invite_waiting_clients()

    def asses_entry_events(self):
        if self.curr_event_index < len(self.arrival_events) and int(self.arrival_events[self.curr_event_index]) < self.model.schedule.time:
            self.waiting_to_enter += 1
            self.curr_event_index += 1

    def invite_waiting_clients(self):
        failed_to_place = False
        while self.waiting_to_enter > 0 and not failed_to_place:
            failed_to_place = not self.create_client()
            if not failed_to_place:
                self.waiting_to_enter -= 1

    def advance(self):
        pass

    def create_client(self):
        positions = [pos for pos in self._places_to_create() if self.model.grid.is_cell_empty(pos)]
        if len(positions) > 0:
            pos = random.choice(positions)
            cell = Client(pos, self.gen_item_list(), self.model)
            self.model.grid.place_agent(cell, cell.pos)
            self.model.schedule.add(cell)
            print("Client entered at {}".format(pos))
            return True
        else:
            print("Entrance blocked at ({},{})".format(self.x, self.y))
            return False

    def _places_to_create(self):
        return moveUtils.places_to_move(self.x, self.y, self.model.width, self.model.height)
