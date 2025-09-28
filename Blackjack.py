import random

CARD_TYPES = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
DEFAULT_DECKS = 6
DEFAULT_PLAYERS = 5

def user_welcome(): # welcome message
    print("Welcome to the blackjack simulator!")

def get_num_decks(): # get number of decks
    print("How many decks do you want to use today? (min: 1; default: 6; max: 8) ")
    user_input = input()
    
    while True:
        if user_input == "":
            return DEFAULT_DECKS

        try:
            if (1 <= int(user_input) <= 8):
                return int(user_input)
            else:
                print("Please enter a valid number (between 1 and 8, inclusive) or press Enter for default of 6")
                user_input = input()
        except ValueError:
            print("Please enter a valid number (between 1 and 8, inclusive) or press Enter for default of 6")
            user_input = input()

def build_deck(num_decks = 6): # deck building function
    deck = []
    for _ in range(num_decks):
        for _ in range(4):
            deck.extend(CARD_TYPES)
    random.shuffle(deck)
    return deck

def print_deck(deck): # deck printing function
    for i in range(0, len(deck), 13):
        print(deck[i:i+13])

def get_num_players(): # get number of players
    print("How many players are playing with you today, not counting the dealer? (min: 1; default: 5; max: 12)")
    user_input = input()

    while True:
        if user_input == "":
            return DEFAULT_PLAYERS

        try:
            if (1 <= int(user_input) <= 12):
                return int(user_input)
            else:
                print("Please enter a valid number (between 1 and 12, inclusive) or press Enter for default of 5")
                user_input = input()
        except ValueError:
            print("Please enter a valid number (between 1 and 12, inclusive) or press Enter for default of 5")
            user_input = input()

def get_player_position(max_players): # gets player position
    print("Where are you sitting at the table? Type 1 for the first seat (gets cards first), 2 for the next seat, etc.")
    user_input = input()
    
    while True:
        try:
            if (1 <= int(user_input) <= max_players):
                return int(user_input)
            else:
                print(f"Please enter a valid number (between 1 and {max_players}).")
                user_input = input()
        except ValueError:
            print(f"Please enter a valid number (between 1 and {max_players}).")
            user_input = input()

def initialize_players(num_players_val): # create empty lists for each player
    player_hands = []
    for i in range(num_players_val):
        player_hands.append([])
    return player_hands

def deal_card(deck, player_hands, player_index): # deal card function; no check if deck has cards because there will be a future penetration function
    card = deck.pop()
    player_hands[player_index].append(card)
    return card

def initial_deal(deck, player_hands, dealer_hand):
    num_players_val = len(player_hands)

    for i in range(num_players_val):
        card = deal_card(deck, player_hands, i)
        print(f"Player {i+1} gets: {card}")

    dealer_card = deck.pop()
    dealer_hand.append(dealer_card)
    print(f"Dealer shows: {dealer_card}")

    for i in range(num_players_val):
        card = deal_card(deck, player_hands, i)
        print(f"Player {i+1} gets: {card}")

    hole_card = deck.pop()
    dealer_hand.append(hole_card)
    print("Dealer gets hole card (face down)")

def display_hands(player_hands, dealer_hand, user_position, show_hole_card=False): #Display all player hands and dealer hand
    print("\n--- Current Hands ---")
    
    for i, hand in enumerate(player_hands):
        marker = " (YOU)" if i == user_position - 1 else ""
        player_value = hand_value(hand)
        print(f"Player {i+1}{marker}: {hand} (Value: {player_value})")
    
    if show_hole_card:
        dealer_value = hand_value(dealer_hand)
        print(f"Dealer: {dealer_hand} (Value: {dealer_value})")
    else:
        dealer_visible_value = hand_value([dealer_hand[0]])
        print(f"Dealer: [{dealer_hand[0]}, ???] (Showing: {dealer_visible_value})")
    print()

def hand_value(hand): #calculates the value of the hand; not linked through main
    total = 0
    aces = 0

    for card in hand:
        if card == 'K' or card == 'Q' or card == 'J':
            total += 10
        elif card == 'A':
            total += 11
            aces += 1
        else:
            total += card

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total

def action(): # defines action (hit, stand, etc.)
    print("Your turn to play")
    print("1 to Hit")
    print("2 to stand")
    return input()

# def hit():
#     for i in range(num_players_val):
#     card = deal_card(deck, player_hands, i)
#     print(f"Player {i+1} gets: {card}")

def main():
    # Welcome the user
    user_welcome()
    
    # Get game setup
    num_decks = get_num_decks()
    num_players_val = get_num_players()
    user_pos = get_player_position(num_players_val)

    # Create player order
    
    # Build and show the deck
    deck = build_deck(num_decks)
    print_deck(deck)
    
    # Initialize game
    player_hands = initialize_players(num_players_val)
    dealer_hand = []
    
    print(f"\nGame setup: {num_players_val} players, you are in position {user_pos}")
    print("\nDealing initial cards...")
    
    # Deal initial cards
    initial_deal(deck, player_hands, dealer_hand)
    
    # Show current state
    display_hands(player_hands, dealer_hand, user_pos)

    # Player's turn to play
    print(action())

if __name__ == "__main__":
    main()