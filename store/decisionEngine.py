import random
import numpy as np

from store import utils
from store.drivers.inertia import Inertia


class DecisionEngine:
    INERTIA_COEFF = 1.0
    INERTIA_RETENTION = 0.9

    def __init__(self, model):
        self.model = model
        self.inertia = Inertia()

    def make_decision(self, current, options):
        w_choices  = [(option,0.2+self.inertia.weight((current, option))) for option in options]
        choice = utils.weighted_choice(w_choices)
        next_move = (current, choice)
        self._update(next_move)
        return choice

    def _update(self, move):
        self.inertia.update(move)
