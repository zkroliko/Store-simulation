from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid, MultiGrid
from mesa.time import SimultaneousActivation
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from store.actors.force_ghost import ForceGhost
from store.builder import Builder
from store.stats.active_customers import ActiveCustomersCollector
from store.stats.need import NeedCollector
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

        self.needCollector = NeedCollector
        self.activeCustomersCollector = ActiveCustomersCollector
        self.collectors = [self.needCollector,self.activeCustomersCollector]

    def step(self):
        if self.schedule.time < self.end_turn:
            for collector in self.collectors:
                collector.collect(self)
            self.schedule.step()
        else:
            self.running = False
            print("Simulation stopped after {} turns".format(self.schedule.time))
            plt.title("Needed items and active customers in time")
            plt.legend(handles=[mpatches.Patch(color='red', label='Needed items'),
                                mpatches.Patch(color='orange', label='Active customers')])
            plt.plot(self.needCollector.get_model_vars_dataframe(), color="red")
            plt.plot(self.activeCustomersCollector.get_model_vars_dataframe(), color="orange")
            plt.show()

    def build_force_ghosts(self):
        ghosts = []
        for pos in gen_corner_pos(self.height, self.width):
            ghosts.append(ForceGhost(pos, self))
        return ghosts


