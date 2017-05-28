import unittest
import matplotlib.pyplot as plt
import numpy

from store.actors.entrance import Entrance
from store.builder import Builder


class TestPlacesToBe(unittest.TestCase):
    input_json = {
        "length": 10800,
        "client_count": 500,
        "client_distribution": {
            "mean": 5400,
            "variance": 3000
        }
    }

    def test_graph(self):
        builder = Builder(self.input_json)

        plot = plt.plot()
        bins = 40
        plt.title("Distribution of customer entry events")
        events = builder.create_entry_events(builder.get_client_count())
        bins, e, v = plt.hist(events, bins, linewidth=1, edgecolor='black')
        plt.xlabel('Time')
        plt.ylabel('Customers entering')
        plt.xticks(range(0, builder.get_sim_length(), 540))
        plt.show()
