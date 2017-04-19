class Inertia:
    GENERAL_COEFF = 1.7
    RETENTION = 0.9

    def __init__(self):
        self.x = 0
        self.y = 0

    def weight(self, move):
        vector = self._move_to_vec(move)
        return max(0, (vector[0] * self.x + vector[1] * self.y))

    def update(self, move):
        vector = self._move_to_vec(move)
        self.x = self.RETENTION * self.x + vector[0] * self.GENERAL_COEFF
        self.y = self.RETENTION * self.y + vector[1] * self.GENERAL_COEFF

    def _move_to_vec(self, move):
        vec = move[1][0] - move[0][0], move[1][1] - move[0][1]
        return vec
