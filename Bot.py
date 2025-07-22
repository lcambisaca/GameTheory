class Bot:
    def __init__(self, bluff_strategy, call_strategy):
        self.bluff_strategy = bluff_strategy
        self.call_strategy = call_strategy
        self.score = 0
        self.history = []

    def clone(self, mutate=False):
        # You can implement mutation logic later
        return Bot(self.bluff_strategy, self.call_strategy)
