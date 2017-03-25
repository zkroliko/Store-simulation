import random

from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid

from store.entrance import Entrance
from store.exit import Exit
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

        # Use a simple grid, where edges wrap around.
        self.height = height
        self.width = width
        self.grid = Grid(height, width, torus=False)

        for i in range(10, height - 10):
            cell = Exit((i, 0), self)
            print((i, height))
            self.grid.place_agent(cell, (i, 0))
            self.schedule.add(cell)

        for i in range(0, 20):
            cell = Shelf((5, i + 5), self)
            self.grid.place_agent(cell, (5, i + 5))
            self.schedule.add(cell)

        for i in range(0, 20):
            cell = Shelf((15, i + 5), self)
            self.grid.place_agent(cell, (15, i + 5))
            self.schedule.add(cell)

        for i in range(0, 20):
            cell = Shelf((25, i + 5), self)
            self.grid.place_agent(cell, (25, i + 5))
            self.schedule.add(cell)

        for i in range(0, height - 1):
            cell = Entrance((i, height - 1), self)
            self.grid.place_agent(cell, (i, height - 1))
            self.schedule.add(cell)

        # for i in range(0, 50):
        #     x = random.randrange(width)
        #     y = random.randrange(int(height / 5)) - int(height / 5)
        #     cell = Client((x, y), self)
        #     if (self.grid.is_cell_empty((x, y))):
        #         self.grid.place_agent(cell, (x, y))
        #     self.schedule.add(cell)

        self.running = True

    def step(self):
        self.schedule.step()
