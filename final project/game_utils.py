
# game_utils.py

import random
from collections import defaultdict
from prettytable import PrettyTable
from board import board
from cards import chance_cards, community_chest_cards
from player import Player
import json

def draw_card(cards):
    """Draw a random card from the deck."""
    
    return random.choice(cards)

def roll_dice():
    """Roll two six-sided dice and return their values."""
    return random.randint(1, 6), random.randint(1, 6)

def move_player(player, steps, players):
    """
    Move the player a number of steps on the board and handle the resulting action.
    
    Args:
    player (Player): The player object to move.
    steps (int): The number of steps to move the player.
    players (list): List of all players.
    """
    player.position = (player.position + steps) % len(board)
    current_square = board[player.position]
    print(f"{player.name} moved to square {current_square['square']}: {current_square['name']} (${current_square['price']})")

    if current_square['name'] in [prop['name'] for prop in player.properties]:
        print(f"{player.name} owns this property and doesn't need to pay rent.")
    else:
        for owner in [p for p in players if current_square['name'] in [prop['name'] for prop in p.properties]]:
            if owner.houses[current_square['name']] > 0:
                rent = current_square['rent'][owner.houses[current_square['name']]]
            elif owner.hotels[current_square['name']] > 0:
                rent = current_square['rent'][5]
            else:
                rent = current_square['rent'][0]

            if player.money >= rent:
                player.money -= rent
                owner.money += rent
                print(f"{player.name} pays ${rent} in rent to {owner.name}")
            else:
                print(f"{player.name} cannot pay the rent and goes bankrupt.")
                player.go_bankrupt()
                owner.money += player.money
                player.money = 0
                player.properties = []
                player.houses = defaultdict(int)
                player.hotels = defaultdict(int)
                break

    if player.money < 0:
        player.go_bankrupt()

    print(f"Properties owned by {player.name}:")
    for property in player.properties:
        print(f"- {property['name']}")

def handle_card(player, card, players):
    """
    Handle the effect of a drawn card.
    
    Args:
    player (Player): The player who drew the card.
    card (str): The card drawn.
    players (list): List of all players.
    """
    if card == "Advance to GO":
        player.position = 0
        player.money += 200
        print(f"{player.name} advanced to GO and collected $200.")
    elif card == "Go to Jail":
        player.position = 10
        player.in_jail = True
        player.jail_turns = 0
        print(f"{player.name} is sent to jail.")
    elif card == "Pay Poor Tax of $15":
        player.money -= 15
        print(f"{player.name} paid $15 Poor Tax.")
    elif card == "Your building and loan matures. Collect $150":
        player.money += 150
        print(f"{player.name} collected $150 from building and loan maturing.")
    elif card == "You have won a crossword competition. Collect $100":
        player.money += 100
        print(f"{player.name} collected $100 for winning a crossword competition.")
    elif card == "Bank pays you dividend of $50":
        player.money += 50
        print(f"{player.name} collected $50 bank dividend.")
    elif card == "Get out of Jail Free":
        player.get_out_of_jail_free = True
        print(f"{player.name} received a 'Get out of Jail Free' card.")
    elif card == "Advance to Illinois Ave":
        player.position = 24
        print(f"{player.name} advanced to Illinois Ave.")
    elif card == "Advance to St. Charles Place":
        player.position = 11
        print(f"{player.name} advanced to St. Charles Place.")
    elif card == "Take a ride on the Reading Railroad":
        player.position = 5
        print(f"{player.name} advanced to Reading Railroad.")
    elif card == "Advance to Boardwalk":
        player.position = 38
        print(f"{player.name} advanced to Boardwalk.")
    elif card == "Advance to the nearest Utility":
        if player.position < 12 or player.position > 28:
            player.position = 12
        else:
            player.position = 28
        print(f"{player.name} advanced to the nearest Utility.")
    elif card == "Advance to the nearest Railroad":
        if player.position < 5 or player.position > 35:
            player.position = 5
        elif player.position < 15:
            player.position = 15
        elif player.position < 25:
            player.position = 25
        else:
            player.position = 35
        print(f"{player.name} advanced to the nearest Railroad.")
    elif card == "You are assessed for street repairs: $40 per house, $115 per hotel":
        total_cost = sum(player.houses.values()) * 40 + sum(player.hotels.values()) * 115
        player.money -= total_cost
        print(f"{player.name} paid ${total_cost} for street repairs.")
    elif card == "Pay each player $50":
        for p in players:
            if p != player:
                player.money -= 50
                p.money += 50
        print(f"{player.name} paid each player $50.")
    elif card == "Collect $150":
        player.money += 150
        print(f"{player.name} collected $150.")

def buy_property(player, square):
    """
    Allow the player to buy a property.
    
    Args:
    player (Player): The player attempting to buy the property.
    square (dict): The property to be bought.
    """
    if square['price'] <= player.money:
        player.money -= square['price']
        player.properties.append(square)
        print(f"{player.name} bought {square['name']} for ${square['price']}")
        print(f"{player.name} has cash at hand: ${player.money}")
    else:
        print(f"{player.name} does not have enough money to buy {square['name']}")

def buy_house(player, property_name):
    """
    Allow the player to buy a house on a property.
    
    Args:
    player (Player): The player attempting to buy the house.
    property_name (str): The name of the property.
    """
    for square in board:
        if square['name'] == property_name:
            if property_name in [prop['name'] for prop in player.properties] and player.money >= square['rent'][player.houses[property_name] + 1]:
                player.money -= square['rent'][player.houses[property_name] + 1]
                player.houses[property_name] += 1
                print(f"{player.name} bought a house on {property_name} for ${square['rent'][player.houses[property_name]]}")
                print(f"{player.name} has cash at hand: ${player.money}")
                return
    print(f"{player.name} cannot buy a house on {property_name}")

def buy_hotel(player, property_name):
    """
    Allow the player to buy a hotel on a property.
    
    Args:
    player (Player): The player attempting to buy the hotel.
    property_name (str): The name of the property.
    """
    for square in board:
        if square['name'] == property_name:
            if property_name in [prop['name'] for prop in player.properties] and player.money >= square['rent'][5] and player.houses[property_name] == 4:
                player.money -= square['rent'][5]
                player.houses[property_name] = 0
                player.hotels[property_name] = 1
                print(f"{player.name} bought a hotel on {property_name} for ${square['rent'][5]}")
                print(f"{player.name} has cash at hand: ${player.money}")
                return
    print(f"{player.name} cannot buy a hotel on {property_name}")

def display_board(players, board):
    """
    Display the current state of the game board.
    
    Args:
    players (list): List of all players.
    board (list): List of all properties on the board.
    """
    table = PrettyTable()
    table.field_names = ["Square", "Property", "Price", "Rent", "Owner", "Houses", "Hotels"]
    for property in board:
        owner = ""
        houses = 0
        hotels = 0
        for player in players:
            for p in player.properties:
                if p['name'] == property['name']:
                    owner = player.name
                    houses = player.houses[property['name']]
                    hotels = player.hotels[property['name']]
                    break
        table.add_row([property['square'], property['name'], property.get('price', ''), property.get('rent', ''), owner, houses, hotels])
    print(table)

def save_game(player1, player2):
    """
    Save the current game state to a file.
    
    Args:
    player1 (Player): The first player.
    player2 (Player): The second player.
    """
    game_state = {
        "player1": {
            "name": player1.name,
            "position": player1.position,
            "money": player1.money,
            "properties": [prop['name'] for prop in player1.properties],
            "houses": dict(player1.houses),
            "hotels": dict(player1.hotels),
            "is_bankrupt": player1.is_bankrupt
        },
        "player2": {
            "name": player2.name,
            "position": player2.position,
            "money": player2.money,
            "properties": [prop['name'] for prop in player2.properties],
            "houses": dict(player2.houses),
            "hotels": dict(player2.hotels),
            "is_bankrupt": player2.is_bankrupt
        }
    }
    with open("game_state.json", "w") as f:
        json.dump(game_state, f)
    print("Game state saved.")

def load_game():
    """
    Load the game state from a file.
    
    Returns:
    tuple: Two Player objects representing the loaded game state.
    """
    try:
        with open("game_state.json", "r") as f:
            game_state = json.load(f)
        player1 = Player(game_state["player1"]["name"])
        player1.position = game_state["player1"]["position"]
        player1.money = game_state["player1"]["money"]
        player1.properties = [prop for prop in board if prop['name'] in game_state["player1"]["properties"]]
        player1.houses = defaultdict(int, game_state["player1"]["houses"])
        player1.hotels = defaultdict(int, game_state["player1"]["hotels"])
        player1.is_bankrupt = game_state["player1"]["is_bankrupt"]

        player2 = Player(game_state["player2"]["name"])
        player2.position = game_state["player2"]["position"]
        player2.money = game_state["player2"]["money"]
        player2.properties = [prop for prop in board if prop['name'] in game_state["player2"]["properties"]]
        player2.houses = defaultdict(int, game_state["player2"]["houses"])
        player2.hotels = defaultdict(int, game_state["player2"]["hotels"])
        player2.is_bankrupt = game_state["player2"]["is_bankrupt"]

        print("Game state loaded.")
        return player1, player2
    except FileNotFoundError:
        print("No saved game found.")
        return None, None

def check_winner(players):
    """
    Check if there is a winner in the game.
    
    Args:
    players (list): List of all players.
    
    Returns:
    Player: The winning player, or None if no winner yet.
    """
    active_players = [player for player in players if not player.is_bankrupt]
    if len(active_players) == 1:
        return active_players[0]
    return None