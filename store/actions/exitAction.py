import random


class ExitAction:
    MIN_LENGTH = 15
    MAX_LENGTH = 80

    def __init__(self, client, exit):
        self.client = client
        self.time_left = random.randrange(self.MIN_LENGTH, self.MAX_LENGTH)
        print("Client started checking out")

    def ongoing(self):
        return self.time_left > 0

    def step(self):
        if self.ongoing():
            self.time_left -= 1
        else:
            self.finalize()

    def finalize(self):
        print("Client checking out at the exit after shopping for: {} turns".format(self.client.time_total))
        model = self.client.model
        model.schedule.remove(self.client)
        model.grid.remove_agent(self.client)
        model.total_time_collector.commit_total_time(self.client.time_total)
        self.client.action = None
