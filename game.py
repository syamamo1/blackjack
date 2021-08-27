# https://towardsdatascience.com/winning-blackjack-using-machine-learning-681d924f197c
from deck import Deck
import random
import numpy as np

class game():

    def __init__(self, num_players, bank):
        self.deck = Deck().get()

        self.cards_in_play = {}
        self.bank = bank
        self.pot = {}

        self.dealer_card1 = self.random_card()
        dealer_card2 = self.random_card()
        self.cards_in_play['Dealer'] = [self.dealer_card1, dealer_card2]

        for i in range(num_players):
            player_card1 = self.random_card()
            player_card2 = self.random_card()
            self.cards_in_play['Player%s'%i] = [[player_card1, player_card2]]

    # doesn't account for deck running out of cards
    def random_card(self):
        random_int = random.randint(0, len(self.deck)-1)
        card = self.deck[random_int]
        self.deck.remove(card)

        return card
        
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

    # Dealer hits until >= 17 or on soft 17
    # Returns value of hand
    def dealer_hit(self):
        sum, soft = self.check_status(self.cards_in_play['Dealer'])
        while sum < 17:
            self.cards_in_play['Dealer'].append(self.random_card()) 
            sum, soft = self.check_status(self.cards_in_play['Dealer'])    
        if sum == 17:
            if soft:
                self.cards_in_play['Dealer'].append(self.random_card()) 
                sum, soft = self.check_status(self.cards_in_play['Dealer'])
        return sum

    # Solved moves of BlackJack, returns value
    def player_hit(self, player):
        hand = self.cards_in_play[player][0]
        sum, soft = self.check_status(hand)

        # Pair
        if len(hand) == 2:
            if hand[0].value == hand[1].value:
                self.pair_hit(player)

        # Soft
        elif soft:
            self.soft_hit(player)

        # Double Down 
        elif sum == 9 and self.dealer_card1.value in [3,4,5,6]:
            self.double_down(player)
        elif sum == 10 and self.dealer_card.value in [2,3,4,5,6,7,8,9]:
            self.double_down(player)
        elif sum == 11:
            self.double_down(player)

        # Hit
        else:
            self.cards_in_play[player][0] = self.hard_hit(hand)

        sums = np.array(map(self.check_status, self.cards_in_play[player])).flatten()[::2]    
        return sums
        
    def hard_hit(self, hand):
        sum, soft = self.check_status(hand)

        if sum == 12:
            if self.dealer_card1.value in [4,5,6]:
                None
            else:
                hand.append(self.random_card()) 
                self.hard_hit(hand)

        if sum in [13,14,15,16]:
            if self.dealer_card1.value in [2,3,4,5,6]:
                None
            else:
                hand.append(self.random_card()) 
                self.hard_hit(hand)

        if sum >= 17:
            None

        return hand

    # If soft hand...
    def soft_hit(self, player):
        hand = self.cards_in_play[player][0]
        sum, soft = self.check_status(hand)        

        # Double Down or Hit
        if len(hand) == 2:
            if sum - 11 == 2 and self.dealer_card1.value in [5,6]:
                self.double_down(player)
            elif sum - 11 == 3 and self.dealer_card1.value in [5,6]:
                self.double_down(player)
            elif sum - 11 == 4 and self.dealer_card1.value in [4,5,6]:
                self.double_down(player)
            elif sum - 11 == 5 and self.dealer_card1.value in [4,5,6]:
                self.double_down(player)
            elif sum - 11 == 6 and self.dealer_card1.value in [3,4,5,6]:
                self.double_down(player)
            elif sum - 11 == 7 and self.dealer_card1.value in [2,3,4,5,6]:
                self.double_down(player)
            elif sum - 11 == 8 and self.dealer_card1.value in [6]:
                self.double_down(player)
            elif (sum - 11 in [2,3,4,5,6]) or (sum - 11 in [7] and self.dealer_card1.value in [9,10,'Ace']):
                self.soft_helper(player)

        # Hit
        elif len(hand) > 2:
            if sum - 11 in [2,3,4,5,6]:
                self.soft_helper(player)
            elif sum - 11 == 7 and self.dealer_card1.value not in [7,8]:
                self.soft_helper(player)   
            elif sum - 11 == 8 and self.dealer_card1.value == 6:
                self.soft_helper(player)

    def soft_helper(self, player):
        self.cards_in_play[player].append(self.random_card())

        hand = self.cards_in_play[player]
        sum, soft = self.check_status(hand)    
        if soft:
            self.soft_hit(player)
        else:
            self.cards_in_play[player][0] = self.hard_hit(hand)        

    def pair_hit(self, player):
        hand = self.cards_in_play[player][0]

        if hand[0].value in [2,3] and self.dealer_card1.value not in [8,9,'Jack','Queen','King','Ace']:
            self.split_hand(player) 
        elif hand[0].value == 4 and self.dealer_card1.value in [5,6]:
            self.split_hand(player)  
        elif hand[0].value == 5 and self.dealer_card1.value not in ['Jack','Queen','King','Ace']:
            self.double_down(player)          
        elif hand[0].value == 6 and self.dealer_card1.value not in [7,8,9,'Jack','Queen','King','Ace']:
            self.split_hand(player)
        elif hand[0].value == 7 and self.dealer_card1.value not in [8,9,'Jack','Queen','King','Ace']:
            self.split_hand(player)
        elif hand[0].value == 8:
            self.split_hand(player)
        elif hand[0].value == 9 and self.dealer_card1.value not in [7,10,'Jack','Queen','King','Ace']:
            self.split_hand(player)
        elif hand[0].value in [10,'Jack','Queen','King'] and hand[1].value in [10,'Jack','Queen','King']:
            None
        elif hand[0].value == 'Ace' and hand[1].value == 'Ace':
            self.split_hand(player)
        elif hand[0].value in [2,3,4,5,6,7]:
            self.cards_in_play[player] = self.hard_hit(hand)

    # Split hands, double bet
    def split_hand(self, player):
        hand = self.cards_in_play[player]
        savings = self.bank[player]
        bet = self.pot[player]

        if savings >= bet:
            self.pot[player] = 2*bet
            self.bank[player] = savings - bet

            new_hand1 = [hand[0]].append(self.random_card())
            new_hand2 = [hand[1]].append(self.random_card())

            self.cards_in_play[player] = [new_hand1,new_hand2]

            for i in range(len(self.cards_in_play[player])):
                new_hand = self.cards_in_play[player][i]
                self.cards_in_play[player][i] = self.hard_hit(new_hand)
        else:
            self.hard_hit(player)

    # Double the bet but only one card left...
    def double_down(self, player):
        savings = self.bank[player]
        bet = self.pot[player]
        if savings >= bet:
            self.pot[player] = 2*bet
            self.bank[player] = savings - bet

        self.cards_in_play[player][0].append(self.random_card())



    