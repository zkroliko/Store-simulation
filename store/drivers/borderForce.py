import numpy


class BorderForce:
    GENERAL_COEFF = 10000.0
    DIAG_COEFF = 0.709 # For diagonal vector normalization
    MARGIN = 2

    def __init__(self, client , width, height):
        self.client = client
        self.width = width
        self.height = height
        self.mid_x, self.mid_y = self.width/2, self.height/2
        self.x_weight = 0
        self.y_weight = 0

    def update(self, position):
        dx = self.mid_x - position[0]
        dy = self.mid_y - position[1]
        # Usage of mid_x and mid_y is warranted just by occasion, them being the same value
        self.x_weight = -dx if dx >= (self.mid_x - self.MARGIN) else 0
        self.y_weight = -dy if dy >= (self.mid_y - self.MARGIN) else 0

    def weight(self, move):
        if (self.x_weight or self.y_weight != 0):
            print("AAAAAA " + str(self.x_weight) + "   " + str(self.y_weight) )
        vector = self.debased_vector(move)
        weight = (vector[0] * self.x_weight * + vector[1] * self.y_weight) * self.GENERAL_COEFF
        return max(0, weight)

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
