# import simplegui module
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
POSITION = [[60, 200], [60, 400]]

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            
            "Invalid card: ", suit, rank

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

    def draw_back(self, canvas, pos):
        canvas.draw_image(card_back,
                          CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE) 
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
#        pass	# create Hand object

    def __str__(self):
        string = "Hand contains: "
        for card in self.cards:
            string += card.suit + card.rank + " "
        return string
#        pass	# return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)
#        pass	# add a card object to a hand

    def get_value(self):
        numAce = 0
        value = 0
        for card in self.cards:
            value += VALUES[card.rank]
            if card.rank == 'A':
                numAce += 1
   
        if numAce != 0:
            if value + 10 <= 21:
                value += 10     
   
        return value
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
#        pass	# compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        pass	# draw a hand on the canvas, use the draw method for cards
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
        
#        pass	# create a Deck object

    def shuffle(self):
        random.shuffle(self.cards)
        
        # shuffle the deck 
#        pass    # use random.shuffle()

    def deal_card(self):
        return self.cards.pop()
#        pass	# deal a card object from the deck
    
    def __str__(self):
        string = "Deck contains: "
        for card in self.cards:
            string += str(card) + " "
        
        return string
#        pass	# return a string representing the deck



#define event handlers for buttons
def reset():
    global score 
    deal()
    score = 0
    
def deal():
    global score, outcome, in_play
    global dealer_hand, player_hand, deck, outcome
    # your code goes here

    if in_play == True:
        score -= 1
        outcome = str(score)
   
    deck = Deck()
    deck.shuffle()
    outcome = ""
    in_play = True
    dealer_hand = Hand()
    player_hand = Hand()
    
    for i in range(2):
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())    
    
    
def hit():     
    global player_hand, deck, outcome, in_play, score
    if in_play:
        player_hand.add_card(deck.deal_card())
        if isbusted(player_hand.get_value()):
            outcome += "You lose!"
            score -= 1
            in_play = False
        
#    pass	# replace with your code below
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global dealer_hand, player_hand, deck, outcome, in_play, score
    if in_play:
        in_play = False
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        dealer_value = dealer_hand.get_value()
        player_value = player_hand.get_value()
        
        if isbusted(dealer_hand.get_value()) or dealer_value < player_value:
            outcome += "You win!"
            score += 1
        else:
            outcome += "You lose!"
            score -= 1
    
    pass	# replace with your code below

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global dealer_hand, player_hand, card_back, outcome, in_play
    
    for idx, card in enumerate(dealer_hand.cards):
        if(in_play and idx == 0):
            card.draw_back(canvas, [POSITION[0][0] + idx * 100, POSITION[0][1]])
            continue
        card.draw(canvas, [POSITION[0][0] + idx * 100, POSITION[0][1]])
    for idx, card in enumerate(player_hand.cards):
        card.draw(canvas, [POSITION[1][0] + idx * 100, POSITION[1][1]])
    
    canvas.draw_text(outcome, [250, 160], 60, "Orange")
    canvas.draw_text("Black Jack", [60, 70], 40, "Orange")
    canvas.draw_text("score: "+ str(score), [400, 100], 40, "Black")
    canvas.draw_text("dealer", [60, 160], 50, "Black")
    canvas.draw_text("player", [60, 360], 50, "Black")
    if in_play:
        canvas.draw_text("Hit or Stand?", [250, 360], 50, "Black")
    else:
        canvas.draw_text("New deal?", [250, 360], 50, "Black")


    
#    card = Card("S", "A")
#    card.draw(canvas, [300, 300])
    
def isbusted(value):
    if value > 21:
        return True
    else: 
        return False

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("reset", reset, 200)
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)

frame.set_draw_handler(draw)


# get things rolling
deck = None
dealer_hand = None
player_hand = None

deal()
frame.start()


# remember to review the gradic rubric
