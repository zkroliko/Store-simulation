from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import SimultaneousActivation

from store.builder import Builder


def need_compute(model):
    needed_items = [agent.need_count() for agent in model.schedule.agents if hasattr(agent, "need_count")]
    N = len(needed_items)
    if N > 0:
        B = sum(xi for i, xi in enumerate(needed_items))
        return B
    else:
        return 0


def n_customers_compute(model):
    customers = [agent for agent in model.schedule.agents if hasattr(agent, "need_count")]
    return len(customers)

class Shop(Model):
    def __init__(self, specification):
        self.schedule = SimultaneousActivation(self)
        builder = Builder(specification)
        self.height, self.width = builder.dims()
        self.grid = Grid(self.height, self.width, torus=False)
        self.categories = builder.get_categories()
        builder.build(self)

        self.running = True

        self.needCollector = DataCollector(
            model_reporters={"TotalNeeded": need_compute},
            agent_reporters={"TotalNeededR": lambda s: s.need_count() if hasattr(s, "need_count") else 0}
        )

        self.NCustomersCollector = DataCollector(
            model_reporters={"NCustomers": n_customers_compute},
            agent_reporters={"NCustomersR": lambda s: 1 if hasattr(s, "need_count") else 0}
        )

    def step(self):
        self.needCollector.collect(self)
        self.NCustomersCollector.collect(self)
        self.schedule.step()
