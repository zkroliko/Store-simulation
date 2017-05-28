import csv

import os

import matplotlib.pyplot as plt
import numpy
import time


class TotalTimeCollector:
    def __init__(self):
        self.times = []

    def commit_total_time(self, time):
        self.times.append(time)

    def finalize(self):
        self.print_report()
        self.save_report()
        self.save_data()
        self.plot()

    def plot(self):
        events = self.times
        plot = plt.plot()
        plt.hist(events, 20, linewidth=1, edgecolor='black')
        plt.title("Total turns spent by actors in the simulation")
        plt.xlabel('Turns spent in the shop')
        plt.ylabel('Count')
        plt.show()

    def report(self):
        return "---TIME REPORT FOR CUSTOMERS---\n" \
               + "Average turns in shop: {}\n".format(numpy.mean(self.times)) \
               + "Median turns in shop: {}\n".format(numpy.median(self.times)) \
               + "Standard deviation for turns in shop: {}".format(numpy.std(self.times))

    def print_report(self):
        print(self.report())

    def save_report(self):
        if not os.path.exists("results"):
            os.makedirs("results")
        with open(os.path.join('results', 'total_time_report_{}.csv'.format(str(time.time()))), 'w') as file:
            file.write(self.report())

    def save_data(self):
        if not os.path.exists("results"):
            os.makedirs("results")
        with open(os.path.join('results', 'total_time_data_{}.csv'.format(str(time.time()))), 'w') as file:
            # writer = csv.writer(file, delimiter=' ',
            #                     quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in self.times:
                file.write(str(row)+"\n")
                # writer.writerow(list(row))
