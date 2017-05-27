import numpy

from store.utils import vectorUtils


class PerceptionDriver:
    GENERAL_COEFF = 2.0

    WEIGHTS_NORMAL = {
        "shelf": 1,
        "other_client": -0.15,
        "exit": -1,
        "entrance": -1,
        "ghost": 20
    }

    WEIGHTS_DONE = {
        "shelf": -0.1,
        "other_client": -0.05,
        "exit": 5,
        "entrance": -1
    }

    def __init__(self, client):
        self.w_x = 0
        self.w_y = 0
        self.client = client

    def update(self):
        # Zeroing the weights
        self.w_x = 0
        self.w_y = 0
        # First the grid objects
        for n in self.client.surround:
            impact = 0
            if hasattr(n, "category"):
                impact = self.assess_shelf(n)
            elif hasattr(n, "check_out"):
                impact = self.assess_exit(n)
            elif hasattr(n, "create_client"):
                impact = self.assess_entrance(n)
            elif hasattr(n, "done"):
                impact = self.assess_client(n)
            if impact != 0:
                vector = self.build_vector_to(n)
                norm = numpy.linalg.norm(numpy.asanyarray(vector))
                norm_sq = norm * norm
                self.w_x += impact * vector[0] / norm_sq
                self.w_y += impact * vector[1] / norm_sq
        # For non grid objects
        for g in self.client.model.ghosts:
            impact = self.assess_ghost(g)
            vector = self.build_vector_to(g)
            norm = numpy.linalg.norm(numpy.asanyarray(vector))
            norm_sq = norm * norm
            self.w_x += impact * vector[0] / norm_sq
            self.w_y += impact * vector[1] / norm_sq

        # Scaling the weights according to the coefficient
        self.w_x *= self.GENERAL_COEFF

    def assess_shelf(self, shelf):
        return self.WEIGHTS_NORMAL["shelf"] if self.needed_shelf(shelf) else self.WEIGHTS_DONE["shelf"]

    def assess_exit(self, exit):
        return self.WEIGHTS_DONE["exit"] if self.client.done() else self.WEIGHTS_NORMAL["exit"]

    def assess_entrance(self, entrance):
        return self.WEIGHTS_NORMAL["entrance"]

    def assess_client(self, client):
        return self.WEIGHTS_NORMAL["other_client"]

    def assess_ghost(self, ghost):
        return self.WEIGHTS_NORMAL["ghost"]*ghost.strength

    def needed_shelf(self, shelf):
        return shelf.category in self.client.need and self.client.need[shelf.category] > 0

    def weight(self, move):
        vector = vectorUtils.move_to_vec(move)
        return max(0, (vector[0] * self.w_x + vector[1] * self.w_y) * self.GENERAL_COEFF)

    def build_vector_to(self, n):
        return n.x - self.client.x, n.y - self.client.y

