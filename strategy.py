class Strategy():
    def __init__(self, savings, results, prev_bet, strat_num):
        self.savings = savings
        self.strat_num = strat_num

    def algorithm(self, savings, results, prev_bet):
        # Simple betting strategy
        if self.strat_num == 1:
            return self.check_bet(10, savings)

        # 1,2,3,..10 --> back to 1
        if self.strat_num == 2:
            if prev_bet == 10:
                return self.check_bet(1)
            wins = 0
            losses = 0
            for result in results:
                if result == 'WIN':
                    wins += 1
                if result == 'LOSE':
                    losses += 1
            if wins >= losses:
                return self.check_bet(prev_bet+1)
            elif wins < losses:
                return self.check_bet(1)

    def check_bet(self, bet, savings):
        if bet > savings:
            return savings
        elif bet <= savings:
            return bet

    def get(self):
        return self.algorithm(self.savings)