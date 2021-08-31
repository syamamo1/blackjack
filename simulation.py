from deck import Deck
from game import Game
from strategy import Strategy 

class Simulation():
    
    def run(self, n):
        self.bank = {'Player1': 100}
        pot = self.collect_bets()
        
        G2 = Game(1, self.bank, pot)
        wins = 0
        losses = 0
        ties = 0
        for i in range(n):
            G2.pot = self.collect_bets()
            self.bank, results = G2.play_round()
            print('Bank at end of round %s: '%(i+1), self.bank)
            print('--------------------------------------------')

            for result in results['Player1']:
                if result == 'WIN':
                    wins += 1
                if result == 'LOSE':
                    losses += 1
                if result == 'TIE':
                    ties += 1
            
        print(wins/(wins+losses))


    def collect_bets(self):
        pot = {'Player1': Strategy(self.bank['Player1'], 1).get()}
        for player in pot:
            self.bank[player] -= pot[player]

        return pot


if __name__ == '__main__':
    S = Simulation()
    S.run(10)
    # .377 on 10k runs....little low huh?
    # updated to .4746 on 1M runs