import json

from mesa.space import Grid

from store.entrance import Entrance
from store.exit import Exit
from store.shelf import Shelf


class Builder:
    def __init__(self, data):
        self.data = data

    def dims(self):
        return self.data["height"], self.data["width"]

    def build(self, model):
        self.get_entrances(model, self.data["entrances"])
        self.get_exits(model, self.data["exits"])
        self.get_shelves(model, self.data["shelves"])

    def get_categories(self):
        return self.data["categories"]

    def get_entrances(self, model, list):
        for e in list:
            entrance = Entrance((e["x"],e["y"]), model)
            model.grid.place_agent(entrance, (e["x"],e["y"]))
            model.schedule.add(entrance)

    def get_exits(self, model, list):
        for e in list:
            exit = Exit((e["x"],e["y"]), model)
            model.grid.place_agent(exit, (e["x"],e["y"]))
            model.schedule.add(exit)

    def get_shelves(self, model, list):
        for s in list:
            shelf = Shelf((s["x"],s["y"]), s["category"], model)
            model.grid.place_agent(shelf, (s["x"],s["y"]))
            model.schedule.add(shelf)

