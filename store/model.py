from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import SimultaneousActivation
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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
        self.c_probabilities = builder.get_category_probabilities()
        self.end_turn = builder.get_sim_length()
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
        if self.schedule.time < self.end_turn:
            self.needCollector.collect(self)
            self.NCustomersCollector.collect(self)
            self.schedule.step()
        else:
            self.running = False
            print("Simulation stopped after {} turns".format(self.schedule.time))
            plt.title("Needed items and active customers in time")
            plt.legend(handles=[mpatches.Patch(color='red', label='Needed items'),
                        mpatches.Patch(color='orange', label='Active customers')])
            plt.plot(self.needCollector.get_model_vars_dataframe(), color="red")
            plt.plot(self.NCustomersCollector.get_model_vars_dataframe(), color="orange")
            plt.show()
