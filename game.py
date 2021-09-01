# https://towardsdatascience.com/winning-blackjack-using-machine-learning-681d924f197c
# https://www.pokernews.com/casino/best-blackjack-strategy.htm#a-blackjack-cheat-sh
from mover import Mover 
from scorer import Scorer

class Game():
    
    def __init__(self):
        self.scorer = Scorer()

    def play_round(self, num_players, bank, pot):
        return_pot = pot
        mover = Mover(num_players, bank, pot)
        mover.compute()
        finished_hands, bank, pot = mover.get()

        results = {}
        # Compare scores
        dealer_score = self.scorer.get_scores(finished_hands['Dealer'])
        if dealer_score > 21:
            dealer_bust = True
        else:
            dealer_bust = False

        print('Dealer score: ', dealer_score)
        for i in range(num_players):
            player = 'Player%s'%(i+1)
            player_scores = self.scorer.get_scores(finished_hands[player])
            results[player] = []
            print('Player score: ', player_scores)
            print('Bet size: ', pot['Player1'])

            for score in player_scores:
                if score > 21:
                    player_bust = True
                else:
                    player_bust = False

                if dealer_bust or player_bust:
                    if dealer_bust and player_bust:
                        print('LOSE')
                        results[player].append('LOSE')
                    elif dealer_bust:
                        print('WIN')
                        bank[player] += 2*round(pot[player]/len(finished_hands[player]),2)
                        results[player].append('WIN')
                    elif player_bust:
                        print('LOSE')
                        results[player].append('LOSE')

                elif not dealer_bust and not player_bust:
                    if score > dealer_score:
                        print('WIN')
                        bank[player] += 2*round(pot[player]/len(finished_hands[player]),2)
                        results[player].append('WIN')
                    elif score == dealer_score:
                        print('TIE')
                        bank[player] += round(pot[player]/len(finished_hands[player]),2)
                        results[player].append('TIE')
                    else:
                        print('LOSE')
                        results[player].append('LOSE')

        return bank, return_pot, results



    