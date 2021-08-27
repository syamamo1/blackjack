import numpy as np
from deck import Deck
from game import Game

D = Deck().get()
B = {'Player1': 100000}
G = Game(1, B)

def test1():
    print(len(D))
    for card in G.deck: print(card.value)
    # for i in range(52):
    #     print(i+1, G.random_card())

# test1()

hand1 = D[0:4]
hand2 = D[4:8]
hand3 = D[8:12]
hand4 = [D[12], D[0],D[12],D[12]]

def test2(hand):
    print(G.check_status(hand))
    for card in hand:
        print(card.value)

# test2(hand1)
# test2(hand2)
# test2(hand3)
# test2(hand4)

# testing dealer_hit
def test3(n):
    for i in range(n):
        print('%s ------------------------------------------'%(i+1))
        G2 = Game(1, B)
        G2.deal_cards()
        print('dealer delt', G2.check_status(G2.cards_in_play['Dealer'][0]))
        G2.print_hands('Dealer')
        print(' ')

        G2.dealer_hit()
        print('dealer final', G2.check_status(G2.cards_in_play['Dealer'][0]))
        G2.print_hands('Dealer')

# test3(10)

# testing player_hit
def test4(n):
    for i in range(n):
        print('%s ------------------------------------------'%(i+1))
        G2 = Game(1, B)
        G2.deal_cards()
        print('Player delt', G2.check_status(G2.cards_in_play['Player1'][0]), '--> Dealer shows ', G2.dealer_card1.value)
        G2.print_hands('Player1')
        print(' ')

        G2.player_hit('Player1')
        print('Player final', G2.check_status(G2.cards_in_play['Player1'][0]))
        G2.print_hands('Player1')

# test4(100)
def test5(kk):
    kk.append(4)
    print(kk)

# test5([1,2])
hand5 = [D[0], D[13],D[26],D[39]]
hand5 = [D[0], D[13]]

def test6(hand):
    G2 = Game(1, B)
    G2.deal_cards()
    G2.cards_in_play['Player1'] = [hand]
    print('Player delt', G2.check_status(G2.cards_in_play['Player1'][0]))
    G2.print_hands('Player1')
    print(' ')

    G2.player_move('Player1')
    print('Player final', G2.check_status(G2.finished_hands['Player1'][0]))
    G2.print_hands('Player1')

test6(hand5)

hand1 = [D[0]]
hand2 = [D[13]]
hands1 = [hand1, hand2]

def test7(hands):
    for hand in hands:
        print(hand[0].value, hand[0].suit)
    hands.remove(hand1)
    print(len(hands))

# test7(hands1)
