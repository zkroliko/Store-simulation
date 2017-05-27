from matplotlib import mlab
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import numpy

class TotalTimeCollector:
    def __init__(self):
        self.times = []

    def commit_total_time(self,time):
        self.times.append(time)

    def plot(self):
        events = self.times
        plot = plt.plot()
        plt.hist(events,20,linewidth=1, edgecolor='black')
        plt.title("Total turns spent by actors in the simulation")
        plt.xlabel('Turns spent in the shop')
        plt.ylabel('Count')
        plt.show()

    def report(self):
        print("---TIME REPORT FOR CUSTOMERS---")
        print("Average turns in shop: {}".format(numpy.mean(self.times)))
        print("Median turns in shop: {}".format(numpy.median(self.times)))
        print("Standard deviation for turns in shop: {}".format(numpy.std(self.times)))