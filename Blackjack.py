import random
import time

CARD_TYPES = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
DEFAULT_DECKS = 6
DEFAULT_PLAYERS = 5
RESHUFFLE_PERCENT = 0.75  # reshuffle after 75% of the shoe is used

def user_welcome(): # welcome message
    print("Welcome to the blackjack simulator!")
    print() # blank line for readability 

def get_num_decks(): # get number of decks
    while True:
        # no need to print, you can add the string inside the input function. 
        # also, need the input inside the loop to re-prompt user if the number is less than 1 or greater than 8
        # if the valueerror is hit, it passes/continues, and will keep looping until a return is hit with the default set or user input val set
        user_input = input("How many decks do you want to use today? (min: 1; default: 6; max: 8) ")
        if user_input == "":
            return DEFAULT_DECKS
        try:
            val = int(user_input) #cleaner to convert to int once
            if (1 <= val <= 8):
                return val
        except ValueError: 
            pass
        print("Please enter a valid number 1–8 or press Enter for default.")

def build_deck(num_decks = 6): # deck building function
    deck = []
    for _ in range(num_decks):
        for _ in range(4): # 4 suits
            deck.extend(CARD_TYPES)
    random.shuffle(deck)
    return deck

def print_deck_structure(num_decks): # prints the deck structure, mostly for testing and visualizing the deck(s) and making sure they were all built correctly
    suits = ["♠️ Spades", "♥️ Hearts", "♦️ Diamonds", "♣️ Clubs"]
    for d in range(1, num_decks + 1):
        print(f"\n===== DECK {d} =====")
        for s in suits:
            print(f"{s}: {CARD_TYPES}")

def get_num_players(): # get number of players
    # same as above, input inside loop to re-prompt user if invalid input
    while True:
        user_input = input("How many players are playing with you today, not counting the dealer? (min: 1; default: 5; max: 12)")
        if user_input == "":
            return DEFAULT_PLAYERS
        try:
            val = int(user_input)
            if 1 <= val <= 12:
                return val
        except ValueError:
            pass
        print("Please enter a valid number 1–12 or press Enter for default 5.")

def get_player_position(max_players): # gets player position
    while True:
        user_input = input(f"Your seat (1–{max_players}): ").strip()
        try:
            val = int(user_input)
            if 1 <= val <= max_players:
                return val
        except ValueError:
            pass
        print(f"Please enter a valid number 1–{max_players}.")

def initialize_players(num_players_val): #creates empty hands for each player
    return [[] for _ in range(num_players_val)]

#only need deck and target hand as parameters and we can remove player index and just used the deck name directly
def deal_card(deck, target_hand): # deal card function; no check if deck has cards because there will be a future penetration function
    if not deck: #check that there is a deck to draw from / will be replaced with penetration logic later
        raise RuntimeError("Shoe is empty (no penetration/reshuffle logic yet).")
    card = deck.pop()
    target_hand.append(card)
    return card


def initial_deal(deck, player_hands, dealer_hand):
    # one up-card to each player
    for i, hand in enumerate(player_hands):
        card = deal_card(deck, hand)
        time.sleep(1)
        print(f"Player {i+1} gets: {card}")

    # dealer up-card
    deal_card(deck, dealer_hand)
    time.sleep(1)
    print(f"Dealer shows: {dealer_hand[0]}")

    # second card to each player
    for i, hand in enumerate(player_hands):
        card = deal_card(deck, hand)
        time.sleep(1)
        print(f"Player {i+1} gets: {card}")

    # dealer hole card
    deal_card(deck, dealer_hand)
    time.sleep(1)
    print("Dealer gets hole card (face down)")

def display_hands(player_hands, dealer_hand, user_position, show_hole_card=False): #Display all player hands and dealer hand
    print("\n--- Current Hands ---")
    time.sleep(1)
    # loop through all player hands
    for i, hand in enumerate(player_hands):
        marker = " (YOU)" if i == user_position - 1 else ""
        # Print player number, the hand (list of cards), and the current total value
        time.sleep(1)
        print(f"Player {i+1}{marker}: {hand} (Value: {hand_value(hand)})")

    if not dealer_hand: # harmless check if dealer hand is empty
        time.sleep(1)
        print("Dealer: [] (Showing: 0)")

     # If show_hole_card=True, reveal both dealer cards and show total value
    elif show_hole_card:
        time.sleep(1)
        print(f"Dealer: {dealer_hand} (Value: {hand_value(dealer_hand)})")
        
    else:
        # else hide the dealer's second hole card and only show the first
        # value of just the up-card
        time.sleep(1)
        print(f"Dealer: [{dealer_hand[0]}, ???] (Showing: {hand_value([dealer_hand[0]])})")
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

#changing to prompt action with hit or stand options
def prompt_action():
    while True:
        choice = input("Your action: (H)it or (S)tand? ").strip().lower()
        if choice in ('h','s'):
            return choice
        time.sleep(1)
        print("Please enter 'h' or 's'.")


#added the below function to return action
def is_blackjack(hand): #returns boolean if hand is a blackjack
    return len(hand) == 2 and hand_value(hand) == 21

def is_bust(hand): #returns boolean if hand is bust
    return hand_value(hand) > 21

def all_players_bust(player_hands): #returns boolean if all players have bust
    for hand in player_hands:
        if not is_bust(hand):
            return False
    print("All players bust. Dealer wins.")
    return True


# player turn function with is_user parameter to differentiate between user and bot players
def player_turn(deck, hand, is_user=True):
    # If opening blackjack, no action.
    if is_blackjack(hand):
        return
    while True:
        if is_user: # user prompt for action
            time.sleep(1)
            print(f"Your hand: {hand} (Value: {hand_value(hand)})")
            act = prompt_action()
        else:
            # simple bot: stand always (can be made smarter later)
            act = 's'
        if act == 'h': # hit
            card = deal_card(deck, hand)
            if is_user:
                time.sleep(1)
                print(f"You draw: {card} (Value: {hand_value(hand)})")
            if is_bust(hand): # check for bust
                if is_user:
                    time.sleep(1)
                    print("You bust!")
                break
        else:
            if is_user: # stand
                time.sleep(1)
                print("You stand.")
            break

def dealer_turn(deck, dealer_hand, hit_soft_17=True): # dealer turn function with soft 17 rule
    time.sleep(1)
    print("\nDealer reveals hole card...")
    time.sleep(1)
    print(f"Dealer has: {dealer_hand} (Value: {hand_value(dealer_hand)})")
    while True:
        value = hand_value(dealer_hand)
        # detect soft 17: value==17 and hand contains an Ace counted as 11
        # quick check: if any Ace and (value - 10) is between 7 and 11 inclusive
        soft17 = (value == 17) and any(c == 'A' for c in dealer_hand) and (hand_value([c if c != 'A' else 1 for c in dealer_hand]) == 7)
        must_hit = value < 17 or (hit_soft_17 and soft17)
        if must_hit:
            card = deal_card(deck, dealer_hand)
            time.sleep(1)
            print(f"Dealer draws: {card} (Value: {hand_value(dealer_hand)})")
            if is_bust(dealer_hand):
                time.sleep(1)
                print("Dealer busts!")
                break
        else:
            time.sleep(1)
            print("Dealer stands.")
            break

def resolve_round(player_hands, dealer_hand): # resolve round function to determine outcomes 
    dealer_total = hand_value(dealer_hand)
    dealer_bj = is_blackjack(dealer_hand)
    time.sleep(1)
    print("\n--- Results ---")
    for i, hand in enumerate(player_hands): # loop through each player hand to determine outcome
        player_total = hand_value(hand)
        player_bj = is_blackjack(hand)
        if player_bj and dealer_bj:
            outcome = "Push (both blackjack)."
        elif player_bj:
            outcome = "Win (blackjack)."
        elif is_bust(hand):
            outcome = "Lose (bust)."
        elif is_bust(dealer_hand):
            outcome = "Win (dealer bust)."
        elif dealer_bj:
            outcome = "Lose (dealer blackjack)."
        elif player_total > dealer_total:
            outcome = "Win."
        elif player_total < dealer_total:
            outcome = "Lose."
        else:
            outcome = "Push."
        time.sleep(1)
        print(f"Player {i+1}: {hand} (Value: {player_total}) -> {outcome}")

def yes_no(prompt): # simple yes/no function
    while True:
        time.sleep(1)
        a = input(f"{prompt} (y/n): ").strip().lower()
        if a in ('y', 'n'):
            return a == 'y' # return True for 'y', False for 'n' to check at the bottom if user wants another round
        print("Please enter 'y' or 'n'.")

def can_start_round(deck, num_players): # check if enough cards to start a new round
    # 2 per player + 2 for dealer to *start* a round
    return len(deck) >= (2 * num_players + 2)


# def hit():
#     for i in range(num_players_val):
#     card = deal_card(deck, player_hands, i)
#     print(f"Player {i+1} gets: {card}")

def main():
    # Welcome the user
    user_welcome()
    
    # Get game setup
    num_decks = get_num_decks()
    num_players = get_num_players() # changed to just numplayers. litte cleaner, implies a num value already
    user_pos = get_player_position(num_players)

    # Create player order
    
    # Build and show the deck
    deck = build_deck(num_decks)
    full_shoe_size = len(deck) # store full shoe size for reshuffle
    time.sleep(1)
    print(f"Game setup: {num_players} players, you are in position {user_pos}.")
    time.sleep(1)
    print(f"Shoe prepared with {len(deck)} cards across {num_decks} deck(s).\n")
    print_deck_structure(num_decks)  # For testing purposes; can be removed in production
    
    # Initialize game
    while True:

         # Check if shoe needs reshuffling
        used_ratio = 1 - (len(deck) / full_shoe_size)
        if used_ratio >= RESHUFFLE_PERCENT:
            time.sleep(1)
            print("\n🔄 The dealer is reshuffling the shoe...")
            for _ in range(3):
                print("...shuffling...")
                time.sleep(0.8)
            deck = build_deck(num_decks)
            full_shoe_size = len(deck)
            time.sleep(1)
            print(f"Shoe reshuffled! Back to {len(deck)} cards.\n")

        if not can_start_round(deck, num_players):
            time.sleep(1)
            print("Not enough cards left in the shoe to start another round.")
            time.sleep(1)
            print(f"Cards remaining: {len(deck)}. Stopping here.")
            break

        player_hands = initialize_players(num_players) # create empty hands for each player
        dealer_hand = []

        time.sleep(1)
        print("Dealing new round...")
        time.sleep(1)
        print("---------- New Round ----------")
        initial_deal(deck, player_hands, dealer_hand)
        display_hands(player_hands, dealer_hand, user_pos, show_hole_card=False)

        for i, hand in enumerate(player_hands):
            is_user = (i == user_pos - 1)
            if is_user:
                time.sleep(1)
                print("\n--- Your Turn ---")
            else:
                time.sleep(1)
                print(f"\n--- Player {i+1} Turn --- (auto-stand in Phase 1)")
            player_turn(deck, hand, is_user=is_user)

        if not all_players_bust(player_hands):
            dealer_turn(deck, dealer_hand, hit_soft_17=True)

        display_hands(player_hands, dealer_hand, user_pos, show_hole_card=True)
        resolve_round(player_hands, dealer_hand)

        if not yes_no("\nDeal another round with the remaining shoe?"):
            time.sleep(1)
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()