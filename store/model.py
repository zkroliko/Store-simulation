from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import SimultaneousActivation

from store.loader import Loader


def compute_gini(model):
    agent_wealths = [agent.need_count() for agent in model.schedule.agents if hasattr(agent, "need_count")]
    x = sorted(agent_wealths)
    N = len(agent_wealths)
    if N > 0:
        B = sum(xi for i, xi in enumerate(x))
        return B
    else:
        return 0


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

        loader = Loader(self, "shop2.json")
        loader.load_from_json()
        self.categories = loader.get_categories()

        self.running = True

        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Need": lambda s: s.need_count() if hasattr(s, "need_count") else 0})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
