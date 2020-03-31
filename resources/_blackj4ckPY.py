from Card_Deck_Hand import Card, Deck, Hand
# -------------- 1-ON-1 BLACKJACK ------------------------
class blackjack_1on1(Deck):
    """ CLASS INH FROM DECK THAT DEALS CARDS AND DPORTS THE PROBLTY """
    def __init__(self, player_name = 'Attila'):
        self.player_name = player_name
        self.cards = [Card(suit, rank) for suit in range(len(Card.suit_l1st)) for rank in range(1, len(Card.rank_l1st))] * 6
        print('self-cards')
        print(len(self.cards))
        self.shuffle() 
        self.player = Hand(play3r_name = self.player_name)
        self.de4ler = Hand('de4ler')
        self.player_blackjack = 0
        self.player_busted = 0
        self.playerStands_dealerWins = 0
        self.dealer_blackjack = 0
        self.dealer_busted = 0
        self.dealerStands_playerWins = 0 
        self.game_push = 0
        
        print('\n...play blackjack 1-on-1...\n')
    
    def display_with_style(self, display_message=''):
        print('\n...' + display_message + '...\n')

    def deal_first_cards(self):
        self.display_with_style('first cards')
        self.move_cards(self.player,1)
        self.move_cards(self.de4ler,1)
        print('>>>--- ' + str(self.player_name) + ' --- >')
        self.show_player_total()        
        print('             < --- de4ler  --- <<<')
        self.show_dealer_total()

    def show_dealer_total_cardClosed(self):
        open_card_list = self.de4ler.to_l1st()[0].__split2rows__()
        closed_card_list = [
            '┌───┐' , 
            '│♦♦♦│' ,
            '│♦♦│' ,
            '│♦♦♦│' ,
            '└───┘'
            ]
        for openCard_split2row, closedCard2row in zip(open_card_list, closed_card_list):
            print(openCard_split2row,closedCard2row)
        
    def show_player_total(self):
        print(self.player)
        player_total = 0
        for number in self.player.blackjack_sum():
            player_total += number
        print('player total is: ' + str(player_total))

    def deal_second_cards(self):
        self.display_with_style ('second cards')
        self.move_cards(self.player,1)
        print('>>>--- ' + str(self.player_name) + ' --- >')
        self.show_player_total()
        print('             < --- de4ler  --- <<<')
        self.show_dealer_total_cardClosed()
        self.move_cards(self.de4ler,1)
        self.show_dealer1st_total()

    def show_dealer1st_total(self):
        dealer_total =  self.de4ler.blackjack_sum()[0]
        print('dealer first card only total is: ' + str(dealer_total))    
    
    def show_dealer_total(self):
        dealer_total = 0
        for numb3r in self.de4ler.blackjack_sum():
            dealer_total += numb3r
        print('dealer total is: ' + str(dealer_total))
        print(self.de4ler)

    def player_hits(self):
        print('>>>--- ' + str(self.player_name) + ' --- >')
        self.display_with_style('player hits')
        self.move_cards(self.player,1)
        self.show_player_total()

    def dealer_hits(self):
        self.display_with_style('dealer hits')
        self.move_cards(self.de4ler, 1)
        self.show_dealer_total()

    def player_calc_total(self):
        current_total = 0
        for number in self.player.blackjack_sum():
            current_total += number
        return current_total

    def dealer_calc_total(self):
        dealer_total = 0
        for number in self.de4ler.blackjack_sum():
            dealer_total += number
        return dealer_total

    def the_play(self, upper_limit = 15):
        pass
        self.display_with_style('simulation upper limit is {}'.format(upper_limit))
        if self.player_calc_total() == 21:
            self.player_blackjack += 1
            self.sim_totals()
        elif self.player_calc_total() >= upper_limit:
            self.display_with_style('player stands')
            self.dealer_plays(17)
        while self.player_calc_total() <= upper_limit:
            self.player_hits()
            if self.player_calc_total()>= 22:
                self.display_with_style('player busted, dealer wins')
                self.player_busted += 1
                self.sim_totals()
            elif self.player_calc_total() >= upper_limit:
                self.display_with_style('player stands')
                self.dealer_plays(17)

    def dealer_plays(self, upper_limit = 17):
        pass
        print('             < --- de4ler  --- <<<')
        print('...second card up....')
        self.show_dealer_total()
        if self.dealer_calc_total() == 21:
            self.dealer_blackjack +=1 
        elif self.dealer_calc_total() > self.player_calc_total():
            self.display_with_style('\t\t\tdealer wins')
            self.playerStands_dealerWins += 1
            self.sim_totals()
        elif self.dealer_calc_total() == self.player_calc_total():
            self.display_with_style('\t\t\tboth sides push')
            self.game_push += 1
            self.sim_totals()
        while self.dealer_calc_total() <= self.player_calc_total() & self.dealer_calc_total() <= 20 :
            self.dealer_hits()
            if self.dealer_calc_total() >= 22:
                self.display_with_style('\t\t\tdealer busted, player wins')
                self.dealer_busted += 1
                self.sim_totals()
            elif self.dealer_calc_total() >= self.player_calc_total():
                if self.dealer_calc_total() <=21:
                    self.display_with_style('\t\t\tdealer wins')
                    self.playerStands_dealerWins += 1
                    self.sim_totals()
        
    def sim_results(self):
        print('player wins, blackjack: {}'.format(self.player_blackjack))
        print('player busted: {}'.format(self.player_busted))
        print('player stands, dealer wins: {}'.format(self.playerStands_dealerWins))
        print('player stands-wins, dealer busted: {}'.format(self.dealer_busted))
        print('player stands, dealer push: {}'.format(self.game_push))
        print('num of cards remaining in deck: {}'.format(len(self.cards)))

    def sim_totals(self):
        pass
        print('\t\t\t\t\tplayer total is: {}'.format(self.player_calc_total()))
        print('\t\t\t\t\tdealer total is: {}'.format(self.dealer_calc_total()))

    def simulation_mode(self, number_of_rounds = 10):
        pass
        for n in range(number_of_rounds):
            self.deal_first_cards()
            self.deal_second_cards()
            self.the_play(13)
            self.player.cards = []
            self.de4ler.cards = []
        self.sim_results()
        
# --------------------------------------
if __name__ == "__main__": 
    pass
    test_game = blackjack_1on1()
    test_game.simulation_mode()