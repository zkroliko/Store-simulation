import os

import matplotlib.pyplot as plt
import numpy
import time
from mesa.datacollection import DataCollector


class ActiveCustomersCollector(DataCollector):
    @staticmethod
    def active_customers_compute(model):
        customers = [agent for agent in model.schedule.agents if hasattr(agent, "need_count")]
        return len(customers)

    def __init__(self):
        super().__init__(model_reporters={"NCustomers": self.active_customers_compute},
                         agent_reporters={"NCustomersR": lambda s: 1 if hasattr(s, "need_count") else 0})

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
        return "---ACTIVE CUSTOMERS REPORT---\n" \
               + "Average active customers: {}\n".format(numpy.mean(self.data)) \
               + "Median active customers: {}\n".format(numpy.median(self.data)) \
               + "Standard deviation of active customers: {}\n".format(numpy.std(self.data))

    def save_report(self):
        if not os.path.exists("results"):
            os.makedirs("results")
        with open(os.path.join('results', 'active_cust_report_{}.txt'.format(str(time.time()))), 'w') as file:
            file.write(self.report())

    def save_data(self):
        path = os.path.join('results', 'active_cust_data_{}.csv'.format(str(time.time())))
        self.get_model_vars_dataframe().to_csv(path)

    def plot(self):
        plt.title("Active customers in simulation time")
        plt.plot(self.get_model_vars_dataframe(), color="orange")
        plt.show()
