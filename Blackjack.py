import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):

        self.hand = []
        self.ace = 0
        self.value = 0
        
    def __str__(self):
           return str([str(card) for card in self.cards])
            
    def add_card(self, card):
         self.hand.append(card)
         if card.get_rank() == 'A':
            self.ace += 1
            
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        self.value = sum([VALUES[card.get_rank()] for card in self.hand])
        if self.ace == 0:
            return self.value
        else: 
            if self.value + 10 <= 21:
                return self.value + 10
            else:
                return self.value
         
    
    def draw(self, canvas, pos,at_dealer):
        for i in range(len(self.hand)):
            self.hand[i].draw(canvas, [pos[0] + 100 * i, pos[1]])
        if in_play:
            if at_dealer:
                canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
      
       

        
# define deck class 
class Deck:
    def __init__(self):
          self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]
              
            
    def shuffle(self):
    # add cards back to deck and shuffle

        random.shuffle(self.deck)

    def deal_card(self):
       return self.deck.pop()
    # deal a card object from the deck
    
    def __str__(self):
        ans=''
        for card in self.deck:
            ans = ans + str(card) + ' , '
        return ans   

#define event handlers for buttons
def deal():
    global outcome,dealer, player, in_play, deck
    outcome = ''
    deck = Deck()
    deck.shuffle()
    dealer = Hand()
    player = Hand()
    dealer.add_card(deck.deal_card()) 
    dealer.add_card(deck.deal_card())    
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())

    in_play = True

def hit():
    global  in_play, score , outcome, message
    # if the hand is in play, hit the player
    if in_play:
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
        else:
            outcome = 'You have busted!'
            score -= score
            in_play = False
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global in_play, score,outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while(dealer.get_value() < 17):
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21 or dealer.get_value() < player.get_value():
            outcome = "You win!"
            score += 1
        else:
            outcome = "You lose."
            score -= 1
            in_play = False
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global in_play
    
    canvas.draw_text("Blackjack", [200, 70], 35, "Black")
    canvas.draw_text("Dealer", [200, 150], 25, "Black")
    canvas.draw_text("Player", [200, 350], 25, "Black")
    canvas.draw_text("Score: "+str(score), (450, 90), 26, "Black")
    player.draw(canvas, [200, 375],False)
    dealer.draw(canvas, [200, 175],True)
    canvas.draw_text(outcome, [500, 150], 40, "Red")

    if not in_play:
        canvas.draw_text("New Deal?",[500,300], 40, "Red")

    
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 800, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
frame.start()
deal()

