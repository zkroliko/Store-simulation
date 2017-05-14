from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import SimultaneousActivation

from store.builder import Builder


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
    def __init__(self, specification):

        self.schedule = SimultaneousActivation(self)
        builder = Builder(specification)
        self.height, self.width = builder.dims()
        self.grid = Grid(self.height, self.width, torus=False)
        self.categories = builder.get_categories()
        builder.build(self)

        self.running = True

        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Need": lambda s: s.need_count() if hasattr(s, "need_count") else 0})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
