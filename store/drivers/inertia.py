class Inertia:
    GENERAL_COEFF = 1.0
    RETENTION = 0.9

    def __init__(self):
        self.x = 1
        self.y = 1

    def weight(self, move):
        vector = self._move_to_dir(move)
        return max(0, (vector[0] * self.x + vector[1] * self.y) * self.GENERAL_COEFF)

    def update(self, move):
        vector = self._move_to_dir(move)
        self.x = self.RETENTION * self.x + vector[0]
        self.y = self.RETENTION * self.y + vector[1]

    def _move_to_dir(self, move):
        return move[1][0] - move[0][0], move[1][1] - move[0][1]
