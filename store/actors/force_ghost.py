from mesa import Agent


class ForceGhost(Agent):
    def __init__(self, pos, model, strength=-1.0):
        super().__init__(pos,model)
        self.x, self.y = pos
        self.pos = pos
        self.strength = strength

    def display(self):
        return None
