from game import Game
from strategy import Strategy 
import time

class Simulation():
    
    def run(self, n):
        self.bank = {'Player1': 100}
        pot = self.collect_bets()
        
        G2 = Game(1, self.bank, pot)
        wins = 0
        losses = 0
        ties = 0
        s = time.time()
        tt = [s]
        for i in range(n):
            if (i+1)%100000 == 0: 
                tt.append(time.time()-tt[-1])
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
        e = time.time()
        print('Runtime: ', e-s)
        print('Velocities: ', tt)
            
        print(wins/(wins+losses))


    def collect_bets(self):
        player1_strat = Strategy(self.bank['Player1'], 1).get()
        pot = {'Player1': player1_strat}

        for player in pot:
            self.bank[player] -= pot[player]

        return pot


if __name__ == '__main__':
    S = Simulation()
    S.run(1000000)

    # .377 on 10k runs....little low huh?
    # updated to .4734 on 3M runs
    # (Approx 1min for 100k runs)