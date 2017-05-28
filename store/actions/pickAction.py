import random


class PickAction:
    MIN_LENGTH = 1
    MAX_LENGTH = 10

    def __init__(self, client, shelf):
        self.client = client
        self.item = shelf.category
        self.length = self.gen_time()
        self.time_left = self.length
        print("Client started picking an item of category {}".format(shelf.category))

    def gen_time(self):
        return random.randrange(self.MIN_LENGTH, self.MAX_LENGTH)

    def ongoing(self):
        return self.time_left > 0

    def step(self):
        if self.ongoing():
            self.time_left -= 1
        else:
            self.finalize()

    def finalize(self):
        print("Client picked up an item of category {}".format(self.item))
        self.client.need[self.item] -= 1
        self.client.have[self.item] += 1
        self.client.past_actions.append(self)
        self.client.action = None

