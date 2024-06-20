
import random
from prettytable import PrettyTable
from player import Player
from board import board
from cards import chance_cards, community_chest_cards, draw_card
from utils import roll_dice, save_game, load_game

def computer_decision(player, board):
    """Make decisions for the computer player."""
    if player.money > 500:
        # Buy properties
        for square in board:
            if square['price'] > 0 and square['name'] not in [prop['name'] for prop in player.properties] and player.money >= square['price']:
                buy_property(player, square)
                break

        # Buy houses and hotels
        for property in player.properties:
            if player.houses[property['name']] < 4 and player.money >= board[property['square']]['rent'][player.houses[property['name']] + 1]:
                buy_house(player, property['name'])
            elif player.houses[property['name']] == 4 and player.money >= board[property['square']]['rent'][5]:
                buy_hotel(player, property['name'])
    elif player.money < 200:
        # Mortgage properties
        for property in player.properties:
            if property not in player.mortgaged_properties:
                player.mortgage(property['name'])
                break

def handle_card(player, card_type, players):
    if card_type == "Chance":
        card = random.choice(chance_cards)
        print(f"{player.name} drew a Chance card: {card}")
        handle_chance_card(player, card, players)
    elif card_type == "Community Chest":
        card = random.choice(community_chest_cards)
        print(f"{player.name} drew a Community Chest card: {card}")
        handle_community_chest_card(player, card, players)

def handle_chance_card(player, card, players):
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

def handle_community_chest_card(player, card, players):
    if card == "Advance to GO":
        player.position = 0
        player.money += 200
        print(f"{player.name} advanced to GO and collected $200.")
    elif card == "Go to Jail":
        player.position = 10
        player.in_jail = True
        player.jail_turns = 0
        print(f"{player.name} is sent to jail.")
    elif card == "You are assessed for street repairs: $40 per house, $115 per hotel":
        total_cost = sum(player.houses.values()) * 40 + sum(player.hotels.values()) * 115
        if player.money >= total_cost:
            player.money -= total_cost
            print(f"{player.name} paid ${total_cost} for street repairs.")
        else:
            player.is_bankrupt = True
            print(f"{player.name} went bankrupt while paying for street repairs.")
    elif card == "Pay each player $50":
        for p in players:
            if p != player:
                p.money += 50
                player.money -= 50
                print(f"{player.name} paid $50 to {p.name}.")
    elif card == "Grand Opera Night. Collect $50 from every player":
        for p in players:
            if p != player:
                if p.money >= 50:
                    p.money -= 50
                    player.money += 50
                    print(f"{player.name} collected $50 from {p.name}.")
                else:
                    p.is_bankrupt = True
                    player.money += p.money
                    print(f"{p.name} went bankrupt and {player.name} collected ${p.money}.")
    elif card == "It is your birthday. Collect $10 from each player":
        for p in players:
            if p != player:
                if p.money >= 10:
                    p.money -= 10
                    player.money += 10
                    print(f"{player.name} collected $10 from {p.name}.")
                else:
                    p.is_bankrupt = True
                    player.money += p.money
                    print(f"{p.name} went bankrupt and {player.name} collected ${p.money}.")

def move_player(player, steps):
    player.position = (player.position + steps) % len(board)
    current_square = board[player.position]
    print(f"{player.name} moved to square {current_square['square']}: {current_square['name']} (${current_square['price']})")

    if current_square['name'] in [prop['name'] for prop in player.properties]:
        print(f"{player.name} owns this property and doesn't need to pay rent.")
    else:
        for owner in [p for p in [player1, player2] if current_square['name'] in [prop['name'] for prop in p.properties]]:
            rent = current_square['rent'][owner.houses[current_square['name']]]
            print(f"{player.name} pays ${rent} in rent to {owner.name}")
            player.money -= rent
            owner.money += rent

    print(f"Properties owned by {player.name}:")
    for property in player.properties:
        print(f"- {property['name']}")

def buy_property(player, square):
    if square['price'] <= player.money:
        player.money -= square['price']
        player.properties.append(square)
        print(f"{player.name} bought {square['name']} for ${square['price']}")
        print(f"{player.name} has cash at hand: ${player.money}")
    else:
        print(f"{player.name} does not have enough money to buy {square['name']}")

def buy_house(player, property_name):
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
    for square in board:
        if square['name'] == property_name:
            if property_name in [prop['name'] for prop in player.properties] and player.money >= square['rent'][5] and player.houses[property_name] == 4:
                player.money -= square['rent'][5]
                player.houses[property_name] = 5
                player.hotels[property_name] = 1
                print(f"{player.name} bought a hotel on {property_name} for ${square['rent'][5]}")
                print(f"{player.name} has cash at hand: ${player.money}")
                return
    print(f"{player.name} cannot buy a hotel on {property_name}")

def play_game():
    global player1, player2
    player1, player2 = load_game()
    if player1 is None or player2 is None:
        player1 = Player("Player 1")
        player2 = Player("Computer")

    current_player = player1

    while True:
        print(f"\n{current_player.name}'s turn.")
        if current_player.name == "Player 1":
            input("Press Enter to roll the dice.\n")
        dice1, dice2 = roll_dice()
        print(f"{current_player.name} rolled a {dice1} and a {dice2}.")
        move_player(current_player, dice1 + dice2)

        current_square = board[current_player.position]
        if current_square['name'] not in [prop['name'] for prop in current_player.properties] and current_square['price'] > 0:
            buy_property(current_player, current_square)

        if current_player.name == "Player 1":
            print("What would you like to do?")
            print("1. Buy a house")
            print("2. Buy a hotel")
            print("3. Mortgage property")
            print("4. Unmortgage property")
            print("5. Save and exit")
            print("6. End turn")

            choice = input("Enter your choice (1-6): ")
            if choice == "1":
                for property in current_player.properties:
                    print(f"{property['name']} ({current_player.houses[property['name']]} houses)")
                prop = input("Enter the property to buy a house: ")
                buy_house(current_player, prop)
            elif choice == "2":
                for property in current_player.properties:
                    if current_player.houses[property['name']] == 4:
                        print(f"{property['name']} (4 houses)")
                prop = input("Enter the property to buy a hotel: ")
                buy_hotel(current_player, prop)
            elif choice == "3":
                for property in current_player.properties:
                    if property['name'] not in [prop['name'] for prop in current_player.mortgaged_properties]:
                        print(f"{property['name']} ({current_player.houses[property['name']]} houses)")
                property_name = input("Enter the property to mortgage: ")
                current_player.mortgage(property_name)
            elif choice == "4":
                for property in current_player.mortgaged_properties:
                    print(f"{property['name']} (mortgaged)")
                property_name = input("Enter the property to unmortgage: ")
                current_player.unmortgage(property_name)
            elif choice == "5":
                save_game(player1, player2)
                return
            elif choice == "6":
                pass
        else:
            computer_decision(current_player, board)
        
        # Switch player turns
        current_player = player2 if current_player == player1 else player1

        player_table = PrettyTable()
        player_table.field_names = ["Player", "Position", "Money", "Properties", "Mortgaged Properties"]
        player_table.add_row(["\033[94mPlayer 1\033[0m", player1.position, f"\033[94m${player1.money}\033[0m", ", \n".join([prop['name'] for prop in player1.properties]), ", \n".join([prop['name'] for prop in player1.mortgaged_properties])])
        player_table.add_row(["\033[91mComputer\033[0m", player2.position, f"\033[91m${player2.money}\033[0m", ", \n".join([prop['name'] for prop in player2.properties]), ", \n".join([prop['name'] for prop in player2.mortgaged_properties])])

        print("\nPlayer Information:")
        print(player_table)