class Strategy():
    def __init__(self, savings, num):
        self.savings = savings
        self.num = num

    def algorithm(self, savings):
        # Simple betting strategy
        if self.num == 1:
            return 10 

    def get(self):
        return self.algorithm(self.savings)