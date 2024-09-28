import json, random
import logging


from collections import deque

from flask import request, jsonify

from routes import app



# Helper function for riffle shuffle
def riffle_shuffle(deck):
    # Ensure the deck is a list
    if not isinstance(deck, list):
        deck = list(deck)
    
    mid = len(deck) // 2
    shuffled_deck = []
    left, right = deck[:mid], deck[mid:]
    
    while left or right:
        if left:
            shuffled_deck.append(left.pop(0))
        if right:
            shuffled_deck.append(right.pop(0))
    return shuffled_deck

# Helper function to cut deck at a specific index
def cut_deck(deck, cut_at):
    return deck[cut_at:] + deck[:cut_at]

# Helper function to deal cards
def deal_cards(deck, num_players, hand_size):
    hands = [[] for _ in range(num_players)]
    for i in range(hand_size):
        for j in range(num_players):
            hands[j].append(deck.pop(0))
    return hands

# Function to determine hand strength
def hand_strength(hand):
    # Placeholder - Implement hand ranking logic based on card strength
    # For now, return the highest card rank as the strength
    return max(hand)

# POST endpoint to rig the dealer
@app.route('/riggedDealer', methods=['POST'])
def rigged_dealer():
    data = request.json
    
    rounds = data['rounds']
    all_actions = []
    
    for round_config in rounds:
        num_players = round_config['numberOfPlayers']
        hand_size = round_config['handSize']
        max_actions = round_config['maxActions']
        winning_player = round_config['winningPlayer']
        expected_hand_strength = round_config['expectedHandStrength']
        deck = round_config['startingDeck']
        
        # Ensure the deck is a list
        if not isinstance(deck, list):
            deck = list(deck)
        
        actions = []
        
        # Perform rigging actions (this is an example flow)
        for _ in range(max_actions):
            # Only cut if the deck has more than 1 card
            if len(deck) > 1:
                cut_at = random.randint(1, len(deck) - 1)
                deck = cut_deck(deck, cut_at)
                actions.append(f"cutAt-{cut_at}")
            
            # Perform riffle shuffle
            deck = riffle_shuffle(deck)
            actions.append("shuffle")
        
        # Deal cards to players
        hands = deal_cards(deck.copy(), num_players, hand_size)
        
        # Ensure accomplice (winningPlayer) gets the expected hand
        accomplice_hand = hands[winning_player]
        accomplice_strength = hand_strength(accomplice_hand)
        
        # If accomplice doesn't have the required hand strength, continue rigging
        if accomplice_strength < expected_hand_strength:
            # Additional logic to continue manipulating the deck
            pass
        
        # Add actions for this round
        all_actions.append(actions)
    
    # Return the shuffle actions
    return jsonify({"actions": all_actions})