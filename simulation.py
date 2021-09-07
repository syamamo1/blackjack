from bokeh.models.annotations import Title
from game import Game
from strategy import Strategy 
from bokeh.plotting import figure, show
from bokeh.models import Title
import time # time.time()

class Simulation():
    
    # n == how many games
    def run_simulation(self, strategy, num_rounds, num_games):
        num_winning = 0
        num_broke = 0

        total_blackjacks = 0
        total_wins = 0
        total_losses = 0

# REWRITE ALL THIS SHIT BELOW ||||||||||||||||

        # builder[round num] = sum bankroll (all games)
        builder = {}
        for i in range(1, num_rounds+1):
            builder[i] = 0

        for j in range(num_games):
            record, blackjacks, wins, losses = self.run_game(strategy, num_rounds)
            total_blackjacks += blackjacks
            total_wins += wins
            total_losses += losses

            for round_num, savings in record:
                sum_savings = builder[round_num]
                builder[round_num] = sum_savings + savings
                if savings == 0 and round_num == 20:
                    num_broke += 1
                if savings >= 20 and round_num == 20:
                    num_winning += 1
            print((j+1)/num_games)

        x = []
        y = []
        # get rid of this using numpy
        for round_num in range(1, num_rounds+1):
            sum_savings = builder[round_num]
            x.append(round_num)
            y.append(round(sum_savings/num_games, 2))

# REWRITE ALL THIS SHIT ABOVE ^^^^^^^^^^^^^^

        p = figure(title = 'Round Number vs. Average Bankroll', x_axis_label = 'Round Number',
                y_axis_label = 'Average Bankroll', y_range = (0, 25))
        p.add_layout(Title(text = 'Blackjacks: %s, Rounds Won: %s, Rounds Lost: %s'%(total_blackjacks, total_wins, total_losses)), 'above')
        p.add_layout(Title(text = 'Total Games: %s, Games Won: %s, Games Lost: %s'%(num_games, num_winning, num_broke)), 'above')
        p.line(x, y)
        show(p)

        print(' ')
        print('===========================')

        print('Total Games: %s'%num_games)
        print('Rounds per Game: %s'%num_rounds)
        print('Total Rounds: ', num_rounds*num_games)
        print(' ')

        print('Total Blackjacks: %s'%total_blackjacks)
        print('Total Round Wins: %s'%(total_wins+total_blackjacks))
        print('Total Round Losses: %s'%total_losses)
        print(' ')

        print('Num Broke: %s'%num_broke)
        print('Num Winnning: %s'%num_winning)
        print(' ')

        print('Calculated Player Odds: ', round(100*(total_blackjacks*1.5 + total_wins)/(total_blackjacks + total_wins + total_losses), 2), '%')
        print('Average Bankroll after 20 rounds: ', '$', y[-1])
        print('Expected Earnings per Game: $', round(y[-1]-10, 2))
        print('===========================')

    # n == how many rounds
    def run_game(self, strategy, num_rounds):
        G2 = Game()
        record = []
        blackjacks = 0
        wins = 0
        losses = 0
        for i in range(num_rounds):
            start_bank = {'Player1': 10}
            if i == 0:
                bank, bets = self.collect_bets(strategy, 0, start_bank, None, None)
            else:
                bank, bets = self.collect_bets(strategy, i+1, bank, prev_bets, results)

            bank, prev_bets, results = G2.play_round(bank, bets)
            blackjacks, wins, losses = self.count_wins_losses(blackjacks, wins, losses, results['Player1'])

            record.append((i+1, bank['Player1']))
        
        return record, blackjacks, wins, losses

    def collect_bets(self, strategy, round_num, bank, prev_bets, results):
        new_bets = {}
        for player in bank:
            if round_num == 0:
                bet = 1
            elif player == 'Player1':
                prev_bet = prev_bets[player]
                bet = strategy(bank[player], prev_bet, results[player])
            new_bets[player] = bet
            bank[player] -= new_bets[player]

        return bank, new_bets

    def count_wins_losses(self, blackjacks, wins, losses, results):
        for result in results:
            outcome = result[0]
            if outcome == 'BLACKJACK':
                blackjacks += 1
            if outcome == 'WIN':
                wins += 1
            if outcome == 'LOSE':
                losses += 1
        return blackjacks, wins, losses

if __name__ == '__main__':
    S = Simulation()
    S.run_simulation(Strategy().positive_progression_system1, num_rounds = 20, num_games = 99)

    # updated to .4734 on 3M runs
    # (Approx 1min for 100k runs)