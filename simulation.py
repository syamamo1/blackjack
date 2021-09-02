from game import Game
from strategy import Strategy 
import time

class Simulation():
    
    # n == how many rounds
    def run(self, n):
        G2 = Game()
        wins = 0
        losses = 0
        ties = 0
        # s = time.time()
        # tt = [s]
        for i in range(n):
            start_bank = {'Player1': 10}
            if i == 0:
                bank, pot = self.collect_bets(0, start_bank, None, None)
            else:
                bank, pot = self.collect_bets(i+1, bank, prev_pot, results)

            # if (i+1)%100000 == 0: 
            #     tt.append(time.time()-tt[-1])
            bank, prev_pot, results = G2.play_round(bank, pot)

            print('Bank at end of round %s: '%(i+1), bank)
            print('--------------------------------------------')

            if bank['Player1'] >= 20 or bank['Player1'] == 0:
                exit()

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

    def collect_bets(self, round_num, bank, prev_pot, results):
        new_pot = {}
        for player in bank:
            if round_num == 0:
                bet = 1
            elif player == 'Player1':
                prev_bet = prev_pot[player]
                bet = Strategy().positive_progression_system1(bank[player], prev_bet, results[player])
            new_pot[player] = bet
            bank[player] -= new_pot[player]

        return bank, new_pot

if __name__ == '__main__':
    S = Simulation()
    S.run(100)

    # updated to .4734 on 3M runs
    # (Approx 1min for 100k runs)