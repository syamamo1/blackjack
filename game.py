# https://towardsdatascience.com/winning-blackjack-using-machine-learning-681d924f197c
# https://www.pokernews.com/casino/best-blackjack-strategy.htm#a-blackjack-cheat-sh
from mover import Mover 
from scorer import Scorer

class Game():
    
    def __init__(self):
        self.scorer = Scorer()

    def play_round(self, bank, pot):
        initial_pot = pot
        mover = Mover(bank, pot) 
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
        for player in bank:
            player_scores = self.scorer.get_scores(finished_hands[player])
            results[player] = []
            print('Player score: ', player_scores)
            print('Bet size: ', pot[player])
            print('Savings: ', bank[player])

            # Needs to be updated for when Split, DD (one hand)
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
                    if score == 21:
                        if dealer_score == 21:
                            print('TIE BLACKJACK')
                            bank[player] += round(pot[player]/len(finished_hands[player]),2)
                            results[player].append('TIE')
                        else:
                            print('BLACKJACK')
                            bank[player] += 5*round(pot[player]/len(finished_hands[player]),2)/2
                            results[player].append('WIN')                            
                    elif score > dealer_score:
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

        return bank, initial_pot, results



    