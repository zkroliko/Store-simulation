import json

from store.entrance import Entrance
from store.exit import Exit
from store.shelf import Shelf


class Loader:
    def __init__(self, model, path):
        self.model = model
        self.path = path

    def load_from_json(self):
        with open(self.path) as file:
            data = json.load(file)
            self._load_entrances(data["entrances"])
            self._load_exits(data["exits"])
            self._load_shelves(data["shelves"])

    def _load_entrances(self, list):
        for e in list:
            entrance = Entrance((e["x"],e["y"]), self.model)
            self.model.grid.place_agent(entrance, (e["x"],e["y"]))
            self.model.schedule.add(entrance)

    def _load_exits(self, list):
        for e in list:
            exit = Exit((e["x"],e["y"]), self.model)
            self.model.grid.place_agent(exit, (e["x"],e["y"]))
            self.model.schedule.add(exit)

    def _load_shelves(self, list):
        for s in list:
            exit = Shelf((s["x"],s["y"]), s["category"], self.model)
            self.model.grid.place_agent(exit, (s["x"],s["y"]))
            self.model.schedule.add(exit)

