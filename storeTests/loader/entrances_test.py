import unittest
import matplotlib.pyplot as plt
import numpy

from store.actors.entrance import Entrance
from store.builder import Builder


class TestPlacesToBe(unittest.TestCase):
    input_json = {
        "length": 8640,
        "client_count": 300,
        "client_distribution": {
            "mean": 4320,
            "variance": 2500
        }
    }

    def test_graph(self):

        builder = Builder(self.input_json)


        plot, subplots = plt.subplots(4, sharex=True, sharey=True)
        subplots[0].set_title("Distribution of entry events for entrances")
        for i in range(0,4):
            events = builder.create_entry_events(1000)
            subplots[i].hist(events)
        plot.subplots_adjust(hspace=0)
        plt.show()
