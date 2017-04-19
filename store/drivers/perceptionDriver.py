import numpy


class PerceptionDriver:
    GENERAL_COEFF = 2.0
    DIAG_COEFF = 0.709 # For diagonal vector normalization

    WEIGHTS_NORMAL = {
        "shelf": 1,
        "other_client": -0.05,
        "exit": -1,
        "entrance": -1
    }

    WEIGHTS_DONE = {
        "shelf": -0.1,
        "other_client": -0.05,
        "exit": 5,
        "entrance": -1
    }

    def __init__(self, client):
        self.x = 0
        self.y = 0
        self.client = client

    def update(self):
        self.x = 0
        self.y = 0
        for n in self.client.surround:
            weight = 0
            if hasattr(n, "category"):
                weight = self.assess_shelf(n)
            elif hasattr(n, "check_out"):
                weight = self.assess_exit(n)
            if hasattr(n, "create_client"):
                weight = self.assess_entrance(n)
            if hasattr(n, "done"):
                weight = self.assess_client(n)
            if weight != 0:
                vector = self.build_vector_to(n)
                norm = numpy.linalg.norm(numpy.asanyarray(vector))
                norm_sq = norm * norm
                self.x += weight * vector[0] / norm_sq
                self.y += weight * vector[1] / norm_sq
        self.x *= self.GENERAL_COEFF
        self.y *= self.GENERAL_COEFF

    def assess_shelf(self, shelf):
        return self.WEIGHTS_NORMAL["shelf"] if shelf.category in self.client.need else self.WEIGHTS_DONE["shelf"]

    def assess_exit(self, exit):
        return self.WEIGHTS_DONE["exit"] if self.client.done() else self.WEIGHTS_NORMAL["exit"]

    def assess_entrance(self, entrance):
        return self.WEIGHTS_NORMAL["entrance"]

    def assess_client(self, client):
        return self.WEIGHTS_NORMAL["other_client"]

    def weight(self, move):
        vector = self.debased_vector(move)
        return max(0, (vector[0] * self.x + vector[1] * self.y) * self.GENERAL_COEFF)

    def build_vector_to(self, n):
        return n.x - self.client.x, n.y - self.client.y

    def debased_vector(self, move):
        # This is all on integers - only on move vectors
        # Normalizing the move vector
        vec = move[1][0] - move[0][0], move[1][1] - move[0][1]
        if vec[0] == vec[1] != 0:
            return vec[0]*self.DIAG_COEFF, vec[1]*self.DIAG_COEFF
        else:
            return vec
