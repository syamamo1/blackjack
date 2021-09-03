from card import Card

class Hand():

    def __init__(self, cards, bet):
        self.cards = cards
        self.bet = bet
        
    def add_card(self, card):
        self.cards.append(card)
        