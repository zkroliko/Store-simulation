import random
import numpy as np

from store import utils
from store.drivers.borderForce import BorderForce
from store.drivers.inertia import Inertia
from store.drivers.perceptionDriver import PerceptionDriver


class DecisionEngine:
    def __init__(self, client):
        self.model = client.model
        self.client = client
        self.inertia = Inertia()
        self.border_force = BorderForce(self, self.client.model.width, self.client.model.height)
        self.perception = PerceptionDriver(self.client)

    def make_decision(self, current, options):
        self.perception.update()
        self.border_force.update(current)
        weights = [self.inertia.weight((current, option)) + self.perception.weight(
            (current, option)) + self.border_force.weight((current, option)) for option in options]
        w_choices = zip(options, weights)
        choice = utils.weighted_choice(list(w_choices))
        next_move = (current, choice)
        self._update(next_move)
        return choice

    def _update(self, move):
        self.inertia.update(move)
