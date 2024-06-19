
from player import*
from prettytable import PrettyTable
from board import create_board
from cards import*
from utils import *


def move_player(player, steps, board):
    player.position = (player.position + steps) % len(board)
    current_square = board[player.position]
    print(f"{player.name} moved to square {current_square['square']}: {current_square['name']} (${current_square['price']})")

    if current_square['name'] in [prop['name'] for prop in player.properties]:
        print(f"{player.name} owns this property and doesn't need to pay rent.")
    else:
        for owner in [p for p in players if current_square['name'] in [prop['name'] for prop in p.properties]]:
            rent = current_square['rent'][owner.houses[current_square['name']]]
            print(f"{player.name} pays ${rent} in rent to {owner.name}")
            player.money -= rent
            owner.money += rent

    player.check_bankruptcy()


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
    global player1, player2, board
    board = create_board()
    player1, player2 = load_game(board)
    if player1 is None or player2 is None:
        player1 = Player("Player 1")
        player2 = Player("Computer")

    players = [player1, player2]
    current_player_index = 0

    while True:
        current_player = players[current_player_index]
        if current_player.is_bankrupt:
            winner = player1 if player2.is_bankrupt else player2
            print(f"{winner.name} wins the game!")
            break

        print(f"\n{current_player.name}'s turn.")
        input("Press Enter to roll the dice.\n")
        dice1, dice2 = roll_dice()
        print(f"You rolled a {dice1} and a {dice2}.")
        move_player(current_player, dice1 + dice2, board)

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
            else:
                current_player_index = 1
        else:
            current_player_index = 0

        player_table = PrettyTable()
        player_table.field_names = ["Player", "Position", "Money", "Properties", "Mortgaged Properties"]
        player_table.add_row(["\033[94mPlayer 1\033[0m", player1.position, f"\033[94m${player1.money}\033[0m", ", \n".join([prop['name'] for prop in player1.properties]), ", \n".join([prop['name'] for prop in player1.mortgaged_properties])])
        player_table.add_row(["\033[91mComputer\033[0m", player2.position, f"\033[91m${player2.money}\033[0m", ", \n".join([prop['name'] for prop in player2.properties]), ", \n".join([prop['name'] for prop in player2.mortgaged_properties])])

        print("\nPlayer Information:")
        print(player_table)


if __name__ == "__main__":
    play_game()