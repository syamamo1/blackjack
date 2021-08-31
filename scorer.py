import numpy as np

# Helper class that returns scores for hands
class Scorer():

    # Returns scores for list of hands
    def get_scores(self, hands):
        results = list(map(self.check_status, hands))
        sums = np.array(results).flatten()[::2]    
        return sums
        
    # Returns max value of cards and if soft
    def check_status(self, cards):
        return self.smart_counter(self.dumb_counter(cards))

    # Returns largest value of cards and number of aces
    def dumb_counter(self, cards):
        sum = 0
        num_aces = 0
        for card in cards:
            if card.value == 'Ace':
               sum += 11
               num_aces += 1
            elif card.value in ['Jack', 'Queen', 'King']:
                sum += 10
            else:
                sum += card.value

        return sum, num_aces

    # Returns max value of cards and if soft
    def smart_counter(self, inputs):
        sum = inputs[0]
        num_aces = inputs[1]    
        if sum > 21:
            if num_aces == 0:
                return sum, False
            else:
                for i in range(num_aces):
                    sum -= 10
                    if sum <= 21 and i < (num_aces-1):
                        return sum, True
                    if sum <= 21 and i >= (num_aces-1):
                        return sum, False 
                if sum > 21:
                    return sum, False
        elif sum <= 21:
            if num_aces == 0:
                return sum, False
            else:
                return sum, True