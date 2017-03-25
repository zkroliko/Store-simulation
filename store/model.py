import random

from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid

from store.entrance import Entrance
from store.exit import Exit
from store.loader import Loader
from store.shelf import Shelf
from store.client import Client


class Shop(Model):
    def __init__(self, height, width):

        # Set up the grid and schedule.

        # Use SimultaneousActivation which simulates all the cells
        # computing their next state simultaneously.  This needs to
        # be done because each cell's next state depends on the current
        # state of all its neighbors -- before they've changed.
        self.schedule = SimultaneousActivation(self)

        self.height = height
        self.width = width
        self.grid = Grid(height, width, torus=False)

        loader = Loader(self,"example.json")
        loader.load_from_json()

        self.running = True

    def step(self):
        self.schedule.step()
