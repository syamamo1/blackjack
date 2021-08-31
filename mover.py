import random
from deck import Deck
from scorer import Scorer

# This class manages all the cards and moves
# and returns finished hands and money info
class Mover():

    def __init__(self, num_players, bank, pot):
        self.num_players = num_players
        self.bank = bank
        self.pot = pot

        self.deck = Deck(6).get()

        self.cards_in_play = {}
        self.finished_hands = {}
        self.scorer = Scorer()

    def get(self):
        return self.finished_hands, self.bank, self.pot

    def compute(self):
        self.deal_cards()
        for i in range(self.num_players):
            player = 'Player%s'%(i+1)
            self.player_move(player)
        self.dealer_move()

    def deal_cards(self):
        self.dealer_card1 = self.random_card()
        dealer_card2 = self.random_card()
        self.cards_in_play['Dealer'] = [[self.dealer_card1, dealer_card2]]
        self.finished_hands['Dealer'] = []

        for i in range(self.num_players):
            player_card1 = self.random_card()
            player_card2 = self.random_card()
            self.cards_in_play['Player%s'%(i+1)] = [[player_card1, player_card2]]
            self.finished_hands['Player%s'%(i+1)] = []

    def print_hands(self, player):
        for i in range(len(self.cards_in_play[player])):
            print(player, 'Unfinished Hand')
            for card in self.cards_in_play[player][i]:
                print(card.value, card.suit)
        for i in range(len(self.finished_hands[player])):
            print(player, 'Finished Hand')
            for card in self.finished_hands[player][i]:
                print(card.value, card.suit)

    # doesn't account for deck running out of cards
    def random_card(self):
        random_int = random.randint(0, len(self.deck)-1)
        card = self.deck[random_int]
        self.deck.remove(card)

        return card

    # Dealer hits until >= 17 or on soft 17
    # Returns value of hand
    def dealer_move(self):
        sum, soft = self.scorer.check_status(self.cards_in_play['Dealer'][0])
        while sum < 17:
            self.cards_in_play['Dealer'][0].append(self.random_card()) 
            sum, soft = self.scorer.check_status(self.cards_in_play['Dealer'][0])    
        if sum == 17:
            if soft:
                self.cards_in_play['Dealer'][0].append(self.random_card()) 
                sum, soft = self.scorer.check_status(self.cards_in_play['Dealer'][0])
        final_hand = self.cards_in_play['Dealer'][0]
        self.stand('Dealer', final_hand)

    def stand(self, player, hand):
        self.cards_in_play[player].remove(hand)
        self.finished_hands[player].append(hand)

    def hit(self, player, hand):
        self.cards_in_play[player].remove(hand)
        hand.append(self.random_card())
        self.cards_in_play[player].append(hand)
        return hand

    # Solved moves of BlackJack
    def player_move(self, player):
        while len(self.cards_in_play[player]) > 0:
            hand = self.cards_in_play[player][0]
            sum, soft = self.scorer.check_status(hand)

            # Pair
            if len(hand) == 2 and hand[0].value == hand[1].value:
                self.pair_hit(player, hand)

            # Not Pair
            else:
                # Soft
                if soft:
                    self.soft_hit(player, hand)

                # Double Down 
                elif sum == 9 and self.dealer_card1.value in [3,4,5,6]:
                    self.double_down(player, hand)
                elif sum == 10 and self.dealer_card1.value in [2,3,4,5,6,7,8,9]:
                    self.double_down(player, hand)
                elif sum == 11:
                    self.double_down(player, hand)

                # Hit
                else:
                    self.hard_hit(player, hand)

    def hard_hit(self, player, hand):
        sum, soft = self.scorer.check_status(hand)

        if sum <= 11:
            self.hit(player, hand)
            self.hard_hit(player, hand)

        if sum == 12:
            if self.dealer_card1.value in [4,5,6]:
                self.stand(player, hand)
            else:
                self.hit(player, hand)
                self.hard_hit(player, hand)

        if sum in [13,14,15,16]:
            if self.dealer_card1.value in [2,3,4,5,6]:
                self.stand(player, hand)
            else:
                self.hit(player, hand)
                self.hard_hit(player, hand)

        if sum >= 17:
            self.stand(player, hand)


    # If soft hand...
    def soft_hit(self, player, hand):
        sum, soft = self.scorer.check_status(hand)        

        # Double Down or Hit
        if len(hand) == 2:
            if sum - 11 == 2 and self.dealer_card1.value in [5,6]:
                self.double_down(player, hand)
            elif sum - 11 == 3 and self.dealer_card1.value in [5,6]:
                self.double_down(player, hand)
            elif sum - 11 == 4 and self.dealer_card1.value in [4,5,6]:
                self.double_down(player, hand)
            elif sum - 11 == 5 and self.dealer_card1.value in [4,5,6]:
                self.double_down(player, hand)
            elif sum - 11 == 6 and self.dealer_card1.value in [3,4,5,6]:
                self.double_down(player, hand)
            elif sum - 11 == 7 and self.dealer_card1.value in [2,3,4,5,6]:
                self.double_down(player, hand)
            elif sum - 11 == 8 and self.dealer_card1.value in [6]:
                self.double_down(player, hand)
            elif (sum - 11 in [2,3,4,5,6]) or (sum - 11 == 7 and self.dealer_card1.value in [9,10,'Ace']):
                self.hit(player, hand)
            else:
                self.stand(player, hand)

        # Hit
        elif len(hand) > 2:
            if sum - 11 in [2,3,4,5,6]:
                self.hit(player, hand)
            elif sum - 11 == 7 and self.dealer_card1.value not in [7,8]:
                self.hit(player, hand)
            elif sum - 11 == 8 and self.dealer_card1.value == 6:
                self.hit(player, hand)
            else:
                self.stand(player, hand)  

    def pair_hit(self, player, hand):
        if hand[0].value in [2,3] and self.dealer_card1.value not in [8,9,'Jack','Queen','King','Ace']:
            self.split_hand(player, hand) 
        elif hand[0].value == 4 and self.dealer_card1.value in [5,6]:
            self.split_hand(player, hand)  
        elif hand[0].value == 5 and self.dealer_card1.value not in ['Jack','Queen','King','Ace']:
            self.double_down(player, hand)          
        elif hand[0].value == 6 and self.dealer_card1.value not in [7,8,9,'Jack','Queen','King','Ace']:
            self.split_hand(player, hand)
        elif hand[0].value == 7 and self.dealer_card1.value not in [8,9,'Jack','Queen','King','Ace']:
            self.split_hand(player, hand)
        elif hand[0].value == 8:
            self.split_hand(player, hand)
        elif hand[0].value == 9 and self.dealer_card1.value not in [7,10,'Jack','Queen','King','Ace']:
            self.split_hand(player, hand)
        elif hand[0].value in [10,'Jack','Queen','King']:
            self.stand(player, hand)
        elif hand[0].value == 'Ace' and hand[1].value == 'Ace':
            self.split_hand(player, hand)
        elif hand[0].value in [2,3,4,5,6,7]:
            self.hard_hit(player, hand)
        else:
            self.stand(player, hand)

    # Split hands, double bet
    def split_hand(self, player, hand):
        savings = self.bank[player]
        bet = self.pot[player]

        if savings >= bet:
            self.pot[player] = 2*bet
            self.bank[player] = savings - bet

            new_hand1 = [hand[0]]
            new_hand1.append(self.random_card())
            new_hand2 = [hand[1]]
            new_hand2.append(self.random_card())

            self.cards_in_play[player].append(new_hand1)
            self.cards_in_play[player].append(new_hand2)
            self.cards_in_play[player].remove(hand)

        else:
            self.hard_hit(player, hand)

    # Double the bet but only one card left...
    def double_down(self, player, hand):
        savings = self.bank[player]
        bet = self.pot[player]
        if savings >= bet:
            self.pot[player] = 2*bet
            self.bank[player] = savings - bet

        new_hand = self.hit(player, hand)
        self.stand(player, new_hand)