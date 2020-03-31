import random
# ---------------- CARD ----------------
class Card:
    """ CARD OBJECT FOR POKER SIMULATION"""
    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank
        self.t1tle =  str(self.rank_names[self.rank]) + ' of ' + str(self.suit_names[self.suit]) + ' '
        self.d1splay = str(self.rank_l2st[self.rank]) + ' of ' + str(self.suit_symbols[self.suit]) + ' '
        self.rank_zip_blackjack = int(self.rank_zip_blackjack[self.rank]) 
    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    suit_symbols = [
        '♣',
        '♦',
        '♥',
        '♠'
    ]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
                  "8", "9", "10", "Jack", "Queen", "King"]
    suit_l1st = ["C", "D", "H", "S"]

    rank_l1st = [None, "A-", "2-", "3-", "4-", "5-", "6-", "7-",
                 "8-", "9-", "10", "J-", "Q-", "K-"]
    rank_l2st = [None, "A", "2", "3", "4", "5",
                 "6", "7", "8", "9", "10", "J", "Q", "K"]
    rank_zip_blackjack = [None, "1", "2", "3", "4", "5",
                 "6", "7", "8", "9", "10", "10", "10", "10"]
    
    def title(self):
        title = str(Card.rank_names[self.rank]) + \
            ' of ' + str(Card.suit_names[self.suit])
        return title

    def __split2rows__(self):
        """ 
        FUNCTION RETURNS A LIST OF STRINGS WHERE EACH ELEMENT
        REPRESENTS A ROW OF A PLAYING CARD
        """
        pass
        suit = str(Card.suit_symbols[self.suit])
        rank = str(Card.rank_l2st[self.rank])
        # ten 10 rank is irregular thus below is req'd
        margin = ''
        if rank != '10':
            margin = ' '
        # t1tle =  str(Card.rank_names[self.rank]) + ' of ' + str(Card.suit_names[self.suit])
        top = '┌───┐'
        rank_left = '│{}{} │'.format(rank, margin)
        suit_center = '│ {} │'.format(suit)
        frame_lower = '│ {}{}│'.format(margin, rank)
        bottom = '└───┘'
        # like a lego of strings
        str_list = [
            # t1tle,
            # margin_top,
            top,
            rank_left,
            suit_center,
            frame_lower,
            bottom
        ]

        return str_list
    
    def __str__(self):
        pass
        suit = str(Card.suit_symbols[self.suit])
        rank = str(Card.rank_l2st[self.rank])
        # ten 10 rank is irregular thus below is req'd
        margin = ''
        if rank != '10':
            margin = ' '
        # briefly store building blocks under variables
        
        top = '┌───┐'
        rank_left = '│{}{} │'.format(rank, margin)
        suit_center = '│ {} │'.format(suit)
        frame_lower = '│ {}{}│'.format(margin, rank)
        bottom = '└───┘'
        # like a lego of strings
        str_list = [
            # t1tle,
            # margin_top,
            top,
            rank_left,
            suit_center,
            frame_lower,
            bottom
        ]
        # iterate through each element of the above list with new line as seperator
        return '\n'.join(str_list)

    def __lt__(self, other):
        """FIRST APPROACH: CHK THE SUITS; IF SAME:CHECK RANKS///SECOND APPROACH: TUPLES
        ///HOWEVER COMPARING CARDS INDVLY MAY NOT BE SO USEFUL IN POKER """
        if self.suit < other.suit:
            return True
        if self.suit > other.suit:
            return False
        return self.rank < other.rank
        # self_tuple = self.suit, self.rank
        # other_tuple = other.suit, other.rank
        # return self_tuple < other_tuple
# ---------------- DECK ----------------
class Deck():
    """ GENERATES FIFTY-TW0 CARDS RANDOM-UNIQUE """

    def __init__(self):
        self.cards = [
            Card(suit, rank) for suit in range(len(Card.suit_l1st)) for rank in range(1, len(Card.rank_l1st))
        ]

    def __str__(self):
        return '\n'.join([
            str(card) for card in self.cards
        ])

    def to_l1st(self):
        """
        JUST TO MAKE SURE OUR DECK OBJECT IS ITERABLE
        """
        get4_list = [card
                     for card in self.cards
                     ]
        return get4_list

    def shuffle(self):
        """
        SHUFFLE B4 BURN-N-TURN
        """
        random.shuffle(self.cards)
    def add_card(self, card):
        """
        TAKES A CARD TO HAND CLASS MEMBER INSTANCE
        """
        pass
        self.cards.append(card)

    def pop_card(self, i=0):
        """Removes and returns a card from the deck.
        i: index of the card to pop; by default, pops the last card.
        """
        return self.cards.pop(i)

    def move_cards(self, hand, num):
        """
        Moves the given number of cards from the deck into the Hand.
        hand: destination Hand object
        num: integer number of cards to move
        """
        for i in range(num):
            hand.add_card(self.pop_card())
    # ------------------------
# =========== HAND ======
class Hand(Deck):
    """ INHERIT FROM DECK SO  ALL METHODS AVLBLE """
    pass
    def __init__(self, label='', play3r_name = 'player'+str(random.randint(0, 99))):
        self.cards = []
        self.label = label
        self.play3r_name = play3r_name

    def __str__(self):
        """
        THIS IS A FUNCTION PRINTS OUT ALL CARDS IN HAND BY ILLSTRTN 
        WITH ASCII-CHARACTERS
        """
        # create a string
        out = ''
        s3lf = self.to_l1st()
        sample_card = Card()
        for n in range(len(sample_card.__split2rows__())):
            for kart in s3lf:
                out += kart.__split2rows__()[n]
            out += '\n'
        # print(out)
        return(out[:-1])
    def type_cards(self):
        out = ''
        for card in self.cards:
            out += str(card.t1tle) + '\n'
        print(out[:-1])
    def classify(self):
        pass
        print(poker_rankings_finder(self))
    def blackjack_sum(self):
        """ CALCULATES BLACKJACK TOTAL OF THE HAND INSTANCE """
        pass
        res = []
        # lets see if we can iterate thru our obj
        for card in self.cards:
            # print(str(card.rank_zip_blackjack))
            res.append(int(str(card.rank_zip_blackjack)))
        return res
    
# ============ POKER_TABLE =============
class PokerTable(Deck):
    def __init__(self, play3r_names=['Attila', 'Bob', 'Codie', 'Daniel', 'Erce', 'Funky'], cards = []):
        self.play3r_names = play3r_names
        self.cards = [ Card(suit, rank) for suit in range(len(Card.suit_l1st)) for rank in range(1, len(Card.rank_l1st))]
        players_message = ': ' 
        for name in play3r_names:
            name += ', '
            players_message+= name
        print('welcome to poker table ' + str(players_message))
        pass
    def deal_Classic5ive(self):
        pass
        self.shuffle()
        # print(str(self)[:90]) #shows the first three cards so lets make sure cards go one by one
        self.play3r_hands = [ Hand(play3r_name = name) for name in self.play3r_names]
        for number_of_cards in range(5):
            for hand in self.play3r_hands:
                self.move_cards(hand,1)
        for hand in self.play3r_hands:
            print('--------- ' + str(hand.play3r_name) + ' ---------')
            print(hand)
        pass
    def deal_Texas7even(self):
        pass
        self.shuffle()
        self.play3r_hands = [ Hand(play3r_name = name) for name in self.play3r_names]
        self.community_cards = Hand('community')
        self.play3r_7cards = self.play3r_hands.copy()
        print()
        print('pocket cards...')
        for hand in [hand for hand in self.play3r_7cards]:
            for n in range(2):
                self.move_cards(hand,1)
            # river card
        for hand in self.play3r_hands:
            print('--- ' + str(hand.play3r_name) + ' ---')
            print(hand)
            # print(hand.type_cards())
        print('the flop...')
        self.move_cards(self.community_cards,5)
        print(self.community_cards)
        for hand in self.play3r_hands:
            for card in self.community_cards.to_l1st():
                hand.add_card(card)
        for hand in self.play3r_hands:
            print('--- ' + str(hand.play3r_name) + ' ---')
            print(hand)
            hand.type_cards()

if __name__ == "__main__":
    pass
    # print(test_hand)
    # poker_rankings_finder(test_hand)
    # print(*Hist(test_hand.to_l1st()), sep = '\n')
    PokerTable().deal_Texas7even()
