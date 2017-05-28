import unittest

import matplotlib.pyplot as plt
import numpy

from store.builder import Builder


class TestPlacesToBe(unittest.TestCase):
    input_json = {
        "categories": ["m", "n", "p", "s", "c", "k", "h", "b", "g", "a", "d", "f"],
        "c_probabilities": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    }

    def test_general(self):
            builder = Builder(self.input_json)
            probs = builder.get_category_probabilities()
            names = numpy.arange(len(probs))

            self.assertEqual(len(names),12)
            self.assertEqual(len(names),len(probs))

    def test_graph(self):

            builder = Builder(self.input_json)

            bar_width = 0.35

            values = builder.get_category_probabilities()
            index = numpy.arange(len(values))

            x_labels = builder.get_categories()

            fig, ax = plt.subplots()
            plt.title("Probabilities of occurrence of items for categories")

            plt.bar(index, values, width=bar_width)
            plt.xlabel('Categories')
            plt.ylabel('Probabilities')
            plt.xticks(index + bar_width / 2, x_labels)
            ax.set_xticklabels(x_labels)

            plt.show()