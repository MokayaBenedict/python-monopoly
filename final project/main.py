# main.py

from player import Player
from board import board
from prettytable import PrettyTable
from cards import chance_cards, community_chest_cards
from game_utils import (roll_dice, move_player, handle_card, display_board, save_game, load_game, check_winner, buy_property, buy_house, buy_hotel, draw_card)
from computer import computer_decision

def play_game():
    """Main game loop."""
    global player1, player2
    player1, player2 = load_game()
    if player1 is None or player2 is None:
        player1 = Player("Player 1")
        player2 = Player("Computer")

    players = [player1, player2]
    current_player_index = 0

    while True:
        current_player = players[current_player_index]
        if current_player.is_bankrupt:
            winner = check_winner(players)
            if winner:
                print(f"{winner.name} wins the game!")
                break
            else:
                current_player_index = (current_player_index + 1) % len(players)
                continue

        print(f"\n{current_player.name}'s turn. Current money: ${current_player.money}")
        display_board(players, board)

        if current_player.in_jail:
            if current_player.get_out_of_jail_free:
                current_player.get_out_of_jail_free = False
                current_player.in_jail = False
                current_player.jail_turns = 0
                print(f"{current_player.name} used a 'Get out of Jail Free' card to get out of jail.")
            else:
                if current_player.jail_turns < 3:
                    roll1, roll2 = roll_dice()
                    if roll1 == roll2:
                        current_player.in_jail = False
                        current_player.jail_turns = 0
                        print(f"{current_player.name} rolled doubles to get out of jail.")
                    else:
                        current_player.jail_turns += 1
                        print(f"{current_player.name} did not roll doubles and is still in jail.")
                        current_player_index = (current_player_index + 1) % len(players)
                        continue
                else:
                    if current_player.money >= 50:
                        current_player.money -= 50
                        current_player.in_jail = False
                        current_player.jail_turns = 0
                        print(f"{current_player.name} paid $50 to get out of jail.")
                    else:
                        current_player.go_bankrupt()
                        current_player_index = (current_player_index + 1) % len(players)
                        continue

        roll1, roll2 = roll_dice()
        move = roll1 + roll2
        print(f"{current_player.name} rolled {roll1} and {roll2}, moving {move} spaces.")

        if roll1 == roll2:
            current_player.consecutive_doubles += 1
            if current_player.consecutive_doubles == 3:
                current_player.position = 10
                current_player.in_jail = True
                current_player.jail_turns = 0
                current_player.consecutive_doubles = 0
                print(f"{current_player.name} rolled three consecutive doubles and is sent to jail.")
                current_player_index = (current_player_index + 1) % len(players)
                continue
        else:
            current_player.consecutive_doubles = 0

        previous_position = current_player.position
        move_player(current_player, move)
        if current_player.position < previous_position:
            current_player.money += 200
            print(f"{current_player.name} passed GO and collected $200.")

        current_square = board[current_player.position]

        print(f"{current_player.name} landed on {current_square['name']}.")

        if current_square['name'] == "Go to Jail":
            current_player.position = 10
            current_player.in_jail = True
            current_player.jail_turns = 0
            print(f"{current_player.name} is sent to jail.")
        elif current_square['name'] == "Community Chest":
            card = draw_card(community_chest_cards)
            print(f"Community Chest: {card}")
            handle_card(current_player, card, players)
        elif current_square['name'] == "Chance":
            card = draw_card(chance_cards)
            print(f"Chance: {card}")
            handle_card(current_player, card, players)
        elif 'price' in current_square and current_square['price'] > 0:
            owner = None
            for p in players:
                for prop in p.properties:
                    if prop['name'] == current_square['name']:
                        owner = p
                        break
            if owner is None:
                if current_player.money >= current_square['price']:
                    buy_property(current_player, current_square)
                else:
                    print(f"{current_player.name} cannot afford {current_square['name']}.")
            elif owner != current_player:
                if owner.houses[current_square['name']] > 0:
                    rent = current_square['rent'][owner.houses[current_square['name']]]
                elif owner.hotels[current_square['name']] > 0:
                    rent = current_square['rent'][5]
                else:
                    rent = current_square['rent'][0]
                
                if current_player.money >= rent:
                    current_player.money -= rent
                    owner.money += rent
                    print(f"{current_player.name} paid ${rent} rent to {owner.name}.")
                else:
                    current_player.go_bankrupt()
                    owner.money += current_player.money
                    current_player.money = 0

        if current_player.name == "Computer":
            computer_decision(current_player, board)
        else:
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

        current_player_index = (current_player_index + 1) % len(players)

        player_table = PrettyTable()
        player_table.field_names = ["Player", "Position", "Money", "Properties", "Mortgaged Properties"]
        player_table.add_row(["\033[94mPlayer 1\033[0m", player1.position, f"\033[94m${player1.money}\033[0m", ", \n".join([prop['name'] for prop in player1.properties]), ", \n".join([prop['name'] for prop in player1.mortgaged_properties])])
        player_table.add_row(["\033[91mComputer\033[0m", player2.position, f"\033[91m${player2.money}\033[0m", ", \n".join([prop['name'] for prop in player2.properties]), ", \n".join([prop['name'] for prop in player2.mortgaged_properties])])

        print("\nPlayer Information:")
        print(player_table)


if __name__ == "__main__":
    play_game()