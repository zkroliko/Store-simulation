import os

import matplotlib.pyplot as plt
import numpy
import time


class TimeCollector:
    def __init__(self):
        # First in tuple for total, second for walking time
        self.times = []

    @property
    def total_times(self):
        return [t[0] for t in self.times]

    @property
    def active_times(self):
        return [t[1] for t in self.times]

    def commit_time(self, total_time, actions):
        action_time = 0
        for a in actions:
            action_time += a.length
        self.times.append((total_time, total_time - action_time))

    def finalize(self):
        self.print_report()
        self.save_report()
        self.save_data()
        self.plot()

    def plot(self):
        self._plot_together()
        self._plot_single(self.total_times, "Total turns spent by actors in the simulation", 'Turns spent in the shop',
                        'Count')
        self._plot_single(self.active_times, "Turns spent by actors active in the simulation", 'Turns spent active',
                        'Count')

    def _plot_together(self):
        n_bins = 30
        fig, axes = plt.subplots(nrows=3, ncols=1)
        ax0, ax1, ax2 = axes.flatten()

        x = (self.total_times,self.active_times)

        colors = ['red', 'tan']
        labels = ['total', 'active']
        title = 'Turns spent by actors in the simulation'
        ax0.hist(x, n_bins, histtype='bar', color=colors, label=labels)
        ax0.legend(prop={'size': 10})
        ax0.set_title(title)

        ax1.hist(x, n_bins, histtype='bar', stacked=True, label=labels)
        ax1.legend(prop={'size': 10})
        ax1.set_title(title)

        ax2.hist(x, n_bins, histtype='step', stacked=True, fill=False, label=labels)
        ax2.legend(prop={'size': 10})
        ax2.set_title(title)

        fig.tight_layout()
        plt.show()

    def _plot_single(self, data, description="", x_label="", y_label=""):
        plot = plt.plot()
        plt.hist(data, 20, linewidth=1, edgecolor='black')
        plt.title(description)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()

    def report(self):
        return "---TIME REPORT FOR CUSTOMERS---\n" \
               + "Average turns in shop: {}\n".format(numpy.mean(self.total_times)) \
               + "Median turns in shop: {}\n".format(numpy.median(self.total_times)) \
               + "Standard deviation for turns in shop: {}\n".format(numpy.std(self.total_times)) \
               + "WALKING TIME:\n" \
               + "Average turns walking in shop: {}\n".format(numpy.mean(self.active_times)) \
               + "Median turns walking in shop: {}\n".format(numpy.median(self.active_times)) \
               + "Standard deviation for turns walking in shop: {}".format(numpy.std(self.active_times))

    def print_report(self):
        print(self.report())

    def save_report(self):
        if not os.path.exists("results"):
            os.makedirs("results")
        with open(os.path.join('results', 'time_report_{}.csv'.format(str(time.time()))), 'w') as file:
            file.write(self.report())

    def save_data(self):
        if not os.path.exists("results"):
            os.makedirs("results")
        with open(os.path.join('results', 'time_data_{}.csv'.format(str(time.time()))), 'w') as file:
            file.write("time_total, time_walking")
            for row in self.times:
                file.write("{}, {}\n".format(str(row[0]),str(row[1])))
