import numpy


class PerceptionDriver:
    GENERAL_COEFF = 2.0

    EFFECTS_NORMAL = {
        "shelf": 1,
        "other_client": -0.1,
        "exit": -0.5,
        "entrance": -0.5
    }

    EFFECTS_DONE = {
        "shelf": -0.5,
        "other_client": -0.1,
        "exit": 5,
        "entrance": -0.5
    }

    def __init__(self, client):
        self.client = client
        self.x = 0
        self.y = 0
        effects = self.EFFECTS_NORMAL if not client.done() else self.EFFECTS_DONE
        for n in client.surround:
            vector = self.build_vector_to(n)
            norm = numpy.linalg.norm(numpy.asanyarray(vector))
            if hasattr(n, "category"):
                weight = self.assess_shelf(client.need, n)
                self.x += effects["shelf"] * weight * vector[0] / norm
                self.y += effects["shelf"] * weight * vector[1] / norm
        self.x *= self.GENERAL_COEFF
        self.y *= self.GENERAL_COEFF

    def assess_shelf(self, need, shelf):
        return 1.0 if shelf.category in need else 0.5

    def weight(self, move):
        vector = self.debased_vector(move)
        return max(0, (vector[0] * self.x + vector[1] * self.y) * self.GENERAL_COEFF)

    def build_vector_to(self, n):
        return n.x - self.client.x, n.y - self.client.y

    @staticmethod
    def debased_vector(move):
        return move[1][0] - move[0][0], move[1][1] - move[0][1]
