import matplotlib.pyplot as plt
import numpy

from store.actors.entrance import Entrance
from store.actors.exit import Exit
from store.actors.shelf import Shelf


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

    def get_category_probabilities(self):
        return self.data["c_probabilities"]

    def get_sim_length(self):
        return self.data["length"]

    def get_client_count(self):
        return self.data["client_count"] if "client_count" in self.data else 100

    def get_client_distribution(self):
        if not "client_distribution" in self.data:
            return 1000.0, 350.0
        else:
            dist = self.data["client_distribution"]
            return dist["mean"], dist["variance"]

    def get_entrances(self, model, list):
        c_per_entrance = int(self.get_client_count()/len(list))
        for e in list:
            entry_events = self.create_entry_events(c_per_entrance)
            entrance = Entrance((e["x"],e["y"]), model, entry_events)
            print("Entrance at {}, {} will have {} clients enter ".format(e["x"],e["y"],len(entry_events)))
            model.grid.place_agent(entrance, (e["x"],e["y"]))
            model.schedule.add(entrance)

    def create_entry_events(self,count):
        dist = self.get_client_distribution()
        left = count
        events = []
        while left > 0:
            new_event = numpy.random.normal(dist[0],dist[1])
            if 0 < new_event < self.get_sim_length():
                events.append(new_event)
                left -= 1
        return events


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

