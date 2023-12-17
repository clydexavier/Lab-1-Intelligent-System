import random
import time
import os

# Initialize deck
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


def initialize_deck(num):
    deck = []
    for i in range (0, num):
        for rank in ranks:
            for suit in suits:
                card = {'rank' : rank, 'suit': suit}
                deck.append(card)
    return deck
    
def calculate_hand_value(hand):
    value = sum(values[card['rank']] for card in hand)
    num_aces = sum(1 for card in hand if card['rank'] == 'Ace')
    
    while num_aces > 0 and value > 21:
        value -= 10  # Convert Ace from 11 to 1 if necessary
        num_aces -= 1
    
    return value

def deal_card(deck, hand):
    card = random.choice(deck)
    hand.append(card)
    deck.remove(card)

def display_hand(hand):
    for card in hand:
        print(f"{card['rank']} of {card['suit']}")



def decide(player_hand, true_count):
    if true_count >= 5:
        if calculate_hand_value(player_hand) >= 12:
            return False
        return True
    
    if calculate_hand_value(player_hand) <= 16:
        return True
    
    return False

def bet_size(bank_roll, remaining_money, true_count):
    betting_unit = 1/100 * bank_roll 
    min_bet = betting_unit
    max_bet = 3 * min_bet

    bet_multiplier = 2 #risk tolerance

    if remaining_money <= betting_unit:
        return remaining_money
    
    if true_count < 1:
        return min_bet

    if true_count >= 1:
        return min_bet + (true_count) * min_bet * bet_multiplier

    else:
        return (true_count - 1) * betting_unit
    
def card_count(card, running_count):
    #hi-low 
    if card['rank'] in ['Ten', 'Jack', 'Queen', 'King', 'Ace']:
        running_count -= 1
    elif card['rank'] in ['Two', 'Three', 'Four', 'Five', 'Six']:
        running_count += 1
    return running_count

def true_count(deck, running_count):
    num_decks = len(deck) / 52

    if num_decks < 1:
        return running_count
    true_count = running_count // num_decks
    return true_count

table_deck = 3
deck = initialize_deck(table_deck)
def game():
    player_money = 1000
    bank_roll = 1000
    running_count = 0

    # Initialize game
    global deck 
    
    while True:
        player_hand = []
        dealer_hand = []

        #print(f"\n\nPLAYER MONEY: {player_money} \n\n")
        
        """
        TODO: 
            Implement how much you bet.
            Implement proper accounting of bets
        """
        print("Enter bet: ")
        time.sleep(5)
        print("Bogart is thinking how much he will bet")
        time.sleep(5)

        bet = bet_size(bank_roll, player_money, true_count(deck, running_count))
        print(f"Bogart bets {bet}\n")
        # Deal initial cards
        for _ in range(2):
            deal_card(deck, player_hand)
            running_count = card_count(player_hand[-1], running_count)
            deal_card(deck, dealer_hand)
            running_count = card_count(dealer_hand[-1], running_count)
        
        # Display hands
        time.sleep(5)

        print("Bogart's hand:")
        display_hand(player_hand)
        print(f"Total value: {calculate_hand_value(player_hand)}\n")
        time.sleep(5)
        print("Dealer's upcard:")
        display_hand([dealer_hand[0]])

        time.sleep(5)
        
        # Player's turn
        while calculate_hand_value(player_hand) < 21:
            print("\nHit or stand? ")
            print("Bogart is thinking.")
            time.sleep(5)

            

            if decide(player_hand, true_count(deck, running_count)):
                print("Bogart chooses to hit.\n")
                time.sleep(5)
                deal_card(deck, player_hand)
                running_count = card_count(player_hand[-1], running_count)
                print("\nBogart's hand:")
                display_hand(player_hand)
                print(f"Total value: {calculate_hand_value(player_hand)}\n")
            else:
                print("Bogart chooses to stand.\n")
                time.sleep(5)
                print("Dealer's hand:")        
                display_hand(dealer_hand)
                print(f"Total value: {calculate_hand_value(dealer_hand)}\n")
                time.sleep(5)
                break
        

        print("Dealer's hand:")        
        display_hand(dealer_hand)
        print(f"Total value: {calculate_hand_value(dealer_hand)}\n")
        time.sleep(5)
        # Dealer's turn
        while calculate_hand_value(dealer_hand) < 17:
            print("Dealing a card to the dealer")
            time.sleep(5)
            deal_card(deck, dealer_hand)
            running_count = card_count(dealer_hand[-1], running_count)
            print("Dealer's hand:")        
            display_hand(dealer_hand)
            print(f"Total value: {calculate_hand_value(dealer_hand)}\n")
            time.sleep(5)
                

        
        # Display final hands
        print("\nBogart's hand:")
        display_hand(player_hand)
        print(f"Total value: {calculate_hand_value(player_hand)}\n")
        print("Dealer's hand:")
        display_hand(dealer_hand)
        print(f"Total value: {calculate_hand_value(dealer_hand)}\n")
        
        # Determine the winner
        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)
        
        if player_value > 21:
            print("Bogart busts! Dealer wins.")
            player_money -= bet
        elif dealer_value > 21:
            print("Dealer busts! Bogart wins.")
            player_money += bet
        elif player_value > dealer_value:
            print("Bogart wins!")
            player_money += bet
        elif player_value < dealer_value:
            print("Dealer wins.")
            player_money -= bet
        else:
            print("It's a tie!")
        
        print(f"\nRunning count: {running_count}\n")
        print(f"True count: {true_count(deck, running_count)}")
        print(f"Net winnings: {player_money - bank_roll} \n")
        print(f"Bogart's remaining money: {player_money}")
        print("\nDo you want to play again?  ")
        time.sleep(5)
        print(f"Bogart is thinking.")
        time.sleep(5)
        if player_money < 100:
            """
            TODO
            IF RUNNING COUNT IS NEGATIVE, BET SMALLER THAN BETTING UNIT
            print("Re-shuffling deck")
            print("NO MORE CARDS LEFT")
           """
            print("Bogart will no longer play.")
            break

        if len(deck) < 10 :
            print(f"Reshuffling deck.")
            running_count = 0
            deck.clear()
            deck = initialize_deck(table_deck)
        #print(f"\n\nPLAYER MONEY: {player_money} \n\n")
        #break 
        print("Bogart wants to play again\n\n")
        time.sleep(5)
        
        
if __name__ == "__main__":
    game()