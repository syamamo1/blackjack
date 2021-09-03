# https://towardsdatascience.com/winning-blackjack-using-machine-learning-681d924f197c
# https://www.pokernews.com/casino/best-blackjack-strategy.htm#a-blackjack-cheat-sh
from mover import Mover 
from scorer import Scorer

class Game():
    
    def __init__(self):
        self.scorer = Scorer()

    def play_round(self, bank, initial_bets):
        mover = Mover(bank, initial_bets) 
        mover.compute()
        finished_hands, bank = mover.get()

        results = {}
        # Compare scores
        dealer_score = self.scorer.get_scores_and_bets(finished_hands['Dealer'])[0][0]
        if dealer_score > 21:
            dealer_bust = True
        else:
            dealer_bust = False

        print('Dealer score: ', dealer_score)
        for player in bank:
            player_results = self.scorer.get_scores_and_bets(finished_hands[player])
            results[player] = []

            for result in player_results:
                score = result[0]
                bet = result[1]
                print('Player score: ', score)
                print('Bet size: ', bet)
                print('Savings: ', bank[player])
                if score > 21:
                    player_bust = True
                else:
                    player_bust = False

                # If someone busts
                if dealer_bust or player_bust:
                    if dealer_bust and player_bust:
                        print('LOSE: ', bet)
                        results[player].append(('LOSE', bet))
                    elif dealer_bust:
                        print('WIN: ', bet)
                        bank[player] += 2*bet
                        results[player].append(('WIN', bet))
                    elif player_bust:
                        print('LOSE: ', bet)
                        results[player].append(('LOSE', bet))

                elif not dealer_bust and not player_bust:
                    if score == 21:
                        if dealer_score == 21:
                            print('TIE BLACKJACK')
                            bank[player] += bet
                            results[player].append(('TIE', bet))
                        else:
                            print('BLACKJACK: ', 2.5*bet)
                            bank[player] += 2.5*bet
                            results[player].append(('WIN', bet))                            
                    elif score > dealer_score:
                        print('WIN: ', bet)
                        bank[player] += 2*bet
                        results[player].append(('WIN', bet))
                    elif score == dealer_score:
                        print('TIE')
                        bank[player] += bet
                        results[player].append(('TIE', bet))
                    else:
                        print('LOSE: ', bet)
                        results[player].append(('LOSE', bet))

        return bank, initial_bets, results



    