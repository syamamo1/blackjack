# Calling a betting strategy with the correct inputs
# returns an amount to bet
class Strategy():

    def constant_bet(self, savings):
        # Simple betting strategy
        if self.strat_num == 1:
            return self.check_bet(1, savings)

    def positive_progression_system1(self, savings, prev_bet, results):
        # 1,2,3,..10 --> back to 1
        if prev_bet >= 10:
            return self.check_bet(1)
        wins, losses = self.count_wins_losses(results)
        if wins > losses:
            return self.check_bet(prev_bet+1, savings)
        elif wins == losses:
            return self.check_bet(prev_bet, savings)
        elif wins < losses:
            return self.check_bet(1, savings)

    def positive_progression_system2(self, savings, prev_bet, results):
        # 1,3,2,6 --> back to 1
        wins, losses = self.count_wins_losses(results)
        if wins > losses:
            if prev_bet == 1:
                return self.check_bet(3, savings)
            if prev_bet == 3:
                return self.check_bet(2, savings)
            if prev_bet == 2:
                return self.check_bet(6, savings)
            if prev_bet == 6:
                return self.check_bet(1, savings)
        elif wins == losses:
            return self.check_bet(prev_bet, savings)
        elif wins < losses:
            return self.check_bet(1, savings)

    # Checks if savings can afford bet
    # If cannot afford, return all of savings
    def check_bet(self, bet, savings):
        if bet > savings:
            return savings
        elif bet <= savings:
            return bet

    def count_wins_losses(self, results):
        wins = 0
        losses = 0
        for result in results:
            if result == 'WIN':
                wins += 1
            if result == 'LOSE':
                losses += 1
        return wins, losses