# https://towardsdatascience.com/winning-blackjack-using-machine-learning-681d924f197c
from mover import Mover 
from scorer import Scorer

class Game():
    
    def __init__(self, num_players, bank, pot):
        self.num_players = num_players
        self.bank = bank
        self.pot = pot

        self.scorer = Scorer()

    def play_round(self):
        mover = Mover(self.num_players, self.bank, self.pot)
        mover.compute()
        self.finished_hands, self.bank, self.pot = mover.get()

        results = {}
        # Compare scores
        dealer_score = self.scorer.get_scores(self.finished_hands['Dealer'])
        if dealer_score > 21:
            dealer_bust = True
        else:
            dealer_bust = False

        print('Dealer score: ', dealer_score)
        for i in range(self.num_players):
            player = 'Player%s'%(i+1)
            player_scores = self.scorer.get_scores(self.finished_hands[player])
            results[player] = []
            print('Player score: ', player_scores)
            print('Bet size: ', self.pot['Player1'])

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
                        self.bank[player] += 2*round(self.pot[player]/len(self.finished_hands[player]),2)
                        results[player].append('WIN')
                    elif player_bust:
                        print('LOSE')
                        results[player].append('LOSE')

                elif not dealer_bust and not player_bust:
                    if score > dealer_score:
                        print('WIN')
                        self.bank[player] += 2*round(self.pot[player]/len(self.finished_hands[player]),2)
                        results[player].append('WIN')
                    elif score == dealer_score:
                        print('TIE')
                        self.bank[player] += round(self.pot[player]/len(self.finished_hands[player]),2)
                        results[player].append('TIE')
                    else:
                        print('LOSE')
                        results[player].append('LOSE')

        return self.bank, results



    