import numpy
from card import Card

class Deck():

    def __init__(self, num_decks):
        self.full_deck = []
        for i in range(num_decks):
            clubs = self.make_suit("Clubs")
            diamonds = self.make_suit("Diamonds")
            hearts = self.make_suit("Hearts")
            spades = self.make_suit("Spades")
            
            new_deck = clubs + diamonds + hearts + spades
            self.full_deck = self.full_deck + new_deck

    def get(self):
        return self.full_deck

    def make_suit(self, suit):
        numbers = [2,3,4,5,6,7,8,9,10]
        faces = ['Jack', 'Queen', 'King', 'Ace']
        cards = []
        for value in numbers + faces:
            card = Card(value, suit)
            cards.append(card)

        return cards

