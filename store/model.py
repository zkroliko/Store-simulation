import random

from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid

from store.cell import Cell


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
        self.grid = Grid(height, width, torus=True)

        # Place a cell at each location, with some initialized to
        # ALIVE and some to DEAD.
		
        for i in range(0,50):
            x = random.randrange(width)
            y = random.randrange(height)
            cell = Cell((x, y), self)
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)
		 
        self.running = True

    def step(self):
        self.schedule.step()
