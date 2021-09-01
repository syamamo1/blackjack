from game import Game
from strategy import Strategy 
import time

class Simulation():
    
    def run(self, n):
        start_bank = {'Player1': 10}
        bank, pot = self.collect_bets(0, start_bank, None, None)
        
        G2 = Game(1, bank, pot)
        wins = 0
        losses = 0
        ties = 0
        # s = time.time()
        # tt = [s]
        for i in range(n):
            # if (i+1)%100000 == 0: 
            #     tt.append(time.time()-tt[-1])
            bank, return_pot, results = G2.play_round(1, bank, pot)
            G2.bank, G2.pot = self.collect_bets(i, bank, return_pot, results)

            print('Bank at end of round %s: '%(i+1), bank)
            print('--------------------------------------------')

            for result in results['Player1']:
                if result == 'WIN':
                    wins += 1
                if result == 'LOSE':
                    losses += 1
                if result == 'TIE':
                    ties += 1

        # e = time.time()
        # print('Runtime: ', e-s)
        # print('Velocities: ', tt)
        print(wins/(wins+losses))

    def collect_bets(self, round_num, bank, return_pot, results):
        for player in return_pot:
            if player == 'Player1':
                if round_num == 0:
                    player1_strat = 1
                else:
                    player1_strat = Strategy().positive_progression_system1(bank['Player1'], return_pot, results)
                pot = {'Player1': player1_strat}
                bank[player] -= pot[player]

        return bank, pot

if __name__ == '__main__':
    S = Simulation()
    S.run(1000000)

    # updated to .4734 on 3M runs
    # (Approx 1min for 100k runs)