import os

import numpy
import time
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt


class NeedCollector(DataCollector):
    @staticmethod
    def need_compute(model):
        needed_items = [agent.need_count() for agent in model.schedule.agents if hasattr(agent, "need_count")]
        N = len(needed_items)
        if N > 0:
            B = sum(xi for i, xi in enumerate(needed_items))
            return B
        else:
            return 0

    def __init__(self):
        super().__init__(model_reporters={"TotalNeeded": self.need_compute},
                         agent_reporters={"TotalNeededR": lambda s: s.need_count() if hasattr(s, "need_count") else 0})

    @property
    def data(self):
        return self.get_model_vars_dataframe().values

    def finalize(self):
        self.plot()
        self.print_report()
        self.save_report()
        self.save_data()

    def print_report(self):
        print(self.report())

    def report(self):
        return "---NEEDED ITEMS REPORT---\n" \
               + "Average total needed items: {}\n".format(numpy.mean(self.data)) \
               + "Median total needed items: {}\n".format(numpy.median(self.data)) \
               + "Standard deviation of total needed items: {}\n".format(numpy.std(self.data))

    def save_report(self):
        if not os.path.exists("results"):
            os.makedirs("results")
        with open(os.path.join('results', 'needed_items_report_{}.txt'.format(str(time.time()))), 'w') as file:
            file.write(self.report())

    def save_data(self):
        path = os.path.join('results', 'needed_items_data_{}.csv'.format(str(time.time())))
        self.get_model_vars_dataframe().to_csv(path)

    def plot(self):
        plt.title("Needed items in simulation time")
        plt.plot(self.get_model_vars_dataframe(), color="red")
        plt.show()
