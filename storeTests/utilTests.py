import unittest

from store import utils


class TestPlacesToBe(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(set(utils.places_to_be(5, 5, 10, 10)),
                         {(5, 5), (4, 4), (4, 5), (5, 4), (6, 6), (6, 5), (5, 6), (4, 6), (6, 4)})

    def test_edge(self):
        self.assertEqual(set(utils.places_to_be(5, 5, 6, 10)),
                         {(5, 5), (4, 4), (4, 5), (5, 4), (5, 6), (4, 6)})
        self.assertNotEqual(set(utils.places_to_be(5, 5, 5, 10)),
                            {(5, 5), (4, 4), (4, 5), (5, 4), (6, 6), (6, 5), (5, 6), (4, 6), (6, 4)})

    def test_cornet(self):
        self.assertEqual(set(utils.places_to_be(5, 5, 6, 6)),
                         {(5, 5), (4, 4), (4, 5), (5, 4)})
        self.assertNotEqual(set(utils.places_to_be(5, 5, 5, 5)),
                            {(5, 5), (4, 4), (4, 5), (5, 4), (6, 6), (6, 5), (5, 6), (4, 6), (6, 4)})
        self.assertNotEqual(set(utils.places_to_be(5, 5, 5, 5)),
                            {(5, 5), (4, 4), (4, 5), (5, 4), (5, 6), (4, 6)})


class TestPlacesToMove(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(set(utils.places_to_move(5, 5, 10, 10)),
                         {(4, 4), (4, 5), (5, 4), (6, 6), (6, 5), (5, 6), (4, 6), (6, 4)})
        self.assertNotEqual(set(utils.places_to_move(5, 5, 10, 10)),
                            {(5, 5), (4, 4), (4, 5), (5, 4), (6, 6), (6, 5), (5, 6), (4, 6), (6, 4)})

    def test_edge(self):
        self.assertEqual(set(utils.places_to_move(5, 5, 6, 10)),
                         {(4, 4), (4, 5), (5, 4), (5, 6), (4, 6)})
        self.assertNotEqual(set(utils.places_to_move(5, 5, 5, 10)),
                            {(5, 5), (4, 4), (4, 5), (5, 4), (5, 6), (4, 6)})
        self.assertNotEqual(set(utils.places_to_move(5, 5, 5, 10)),
                            {(4, 4), (4, 5), (5, 4), (6, 6), (6, 5), (5, 6), (4, 6), (6, 4)})

    def test_cornet(self):
        self.assertEqual(set(utils.places_to_move(5, 5, 6, 6)),
                         {(4, 4), (4, 5), (5, 4)})
        self.assertNotEqual(set(utils.places_to_move(5, 5, 5, 5)),
                            {(5, 5), (4, 4), (4, 5), (5, 4)})
        self.assertNotEqual(set(utils.places_to_move(5, 5, 5, 5)),
                            {(4, 4), (4, 5), (5, 4), (6, 6), (6, 5), (5, 6), (4, 6), (6, 4)})
        self.assertNotEqual(set(utils.places_to_move(5, 5, 5, 5)),
                            {(4, 4), (4, 5), (5, 4), (5, 6), (4, 6)})
