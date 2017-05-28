import matplotlib.pyplot as plt
from mesa import Model
from mesa.space import Grid
from mesa.time import SimultaneousActivation

from store.actors.force_ghost import ForceGhost
from store.builder import Builder
from store.stats.active_customers import ActiveCustomersCollector
from store.stats.need import NeedCollector
from store.stats.time_collector import TimeCollector
from storeTests.corner_utils import gen_corner_pos


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
        self.c_probabilities = builder.get_category_probabilities()
        self.end_turn = builder.get_sim_length()
        builder.build(self)
        self.ghosts = self.build_force_ghosts()

        self.running = True

        # This is for the by step collectors
        self.needCollector = NeedCollector()
        self.activeCustomersCollector = ActiveCustomersCollector()
        self.collectors = [self.needCollector,self.activeCustomersCollector]

        # This is for end of simulation collectors
        self.total_time_collector = TimeCollector()


    def step(self):
        if self.schedule.time < self.end_turn:
            for collector in self.collectors:
                collector.collect(self)
            self.schedule.step()
        else:
            self.running = False
            # For data aquisition
            self.total_time_collector.finalize()
            self.needCollector.finalize()
            self.activeCustomersCollector.finalize()
            plt.show()

    def build_force_ghosts(self):
        ghosts = []
        for pos in gen_corner_pos(self.height, self.width):
            ghosts.append(ForceGhost(pos, self))
        return ghosts


