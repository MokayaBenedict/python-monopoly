import random
from collections import defaultdict
from prettytable import PrettyTable
import json

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 1500
        self.properties = []
        self.houses = defaultdict(int)
        self.hotels = defaultdict(int)
        self.mortgaged_properties = []
        self.is_bankrupt = False
        self.in_jail = False
        self.jail_turns = 0
        self.consecutive_doubles = 0
        self.get_out_of_jail_free = False

    def mortgage(self, property_name):
        for property in self.properties:
            if property['name'] == property_name:
                mortgage_value = property['price'] // 2
                self.money += mortgage_value
                self.mortgaged_properties.append(property)
                self.properties.remove(property)
                property['mortgaged'] = True
                print(f"{self.name} mortgaged {property_name} for ${mortgage_value}")
                return
        print(f"{self.name} does not own {property_name}")

    def unmortgage(self, property_name):
        for property in self.mortgaged_properties:
            if property['name'] == property_name:
                unmortgage_value = property['price'] // 2
                if self.money >= unmortgage_value:
                    self.money -= unmortgage_value
                    self.mortgaged_properties.remove(property)
                    self.properties.append(property)
                    property['mortgaged'] = False
                    print(f"{self.name} unmortgaged {property_name} for ${unmortgage_value}")
                    return
        print(f"{self.name} does not have {property_name} mortgaged")

board = [
    {"square": 0, "name": "GO", "price": 0},
    {"square": 1, "name": "Mediterranean Avenue", "price": 60, "rent": [2, 10, 30, 90, 160, 250]},
    {"square": 2, "name": "Community Chest", "price": 0},
    {"square": 3, "name": "Baltic Avenue", "price": 60, "rent": [4, 20, 60, 180, 320, 450]},
    {"square": 4, "name": "Income Tax", "price": 0},
    {"square": 5, "name": "Reading Railroad", "price": 200, "rent": [25, 50, 100, 200]},
    {"square": 6, "name": "Oriental Avenue", "price": 100, "rent": [6, 30, 90, 270, 400, 550]},
    {"square": 7, "name": "Chance", "price": 0},
    {"square": 8, "name": "Vermont Avenue", "price": 100, "rent": [6, 30, 90, 270, 400, 550]},
    {"square": 9, "name": "Connecticut Avenue", "price": 120, "rent": [8, 40, 100, 300, 450, 600]},
    {"square": 10, "name": "Jail", "price": 0},
    {"square": 11, "name": "St. Charles Place", "price": 140, "rent": [10, 50, 150, 450, 625, 750]},
    {"square": 12, "name": "Electric Company", "price": 150, "rent": [4, 10]},
    {"square": 13, "name": "Virginia Avenue", "price": 160, "rent": [12, 60, 180, 500, 700, 900]},
    {"square": 14, "name": "Pennsylvania Railroad", "price": 200, "rent": [25, 50, 100, 200]},
    {"square": 15, "name": "St. James Place", "price": 180, "rent": [14, 70, 200, 550, 750, 950]},
    {"square": 16, "name": "Community Chest", "price": 0},
    {"square": 17, "name": "Tennessee Avenue", "price": 180, "rent": [14, 70, 200, 550, 750, 950]},
    {"square": 18, "name": "New York Avenue", "price": 200, "rent": [16, 80, 220, 600, 800, 1000]},
    {"square": 19, "name": "Free Parking", "price": 0},
    {"square": 20, "name": "Kentucky Avenue", "price": 220, "rent": [18, 90, 250, 700, 875, 1050]},
    {"square": 21, "name": "Chance", "price": 0},
    {"square": 22, "name": "Indiana Avenue", "price": 220, "rent": [18, 90, 250, 700, 875, 1050]},
    {"square": 23, "name": "Illinois Avenue", "price": 240, "rent": [20, 100, 300, 750, 925, 1100]},
    {"square": 24, "name": "B&O Railroad", "price": 200, "rent": [25, 50, 100, 200]},
    {"square": 25, "name": "Atlantic Avenue", "price": 260, "rent": [22, 110, 330, 800, 975, 1150]},
    {"square": 26, "name": "Ventnor Avenue", "price": 260, "rent": [22, 110, 330, 800, 975, 1150]},
    {"square": 27, "name": "Water Works", "price": 150, "rent": [4, 10]},
    {"square": 28, "name": "Marvin Gardens", "price": 280, "rent": [24, 120, 360, 850, 1025, 1200]},
    {"square": 29, "name": "Go to Jail", "price": 0},
    {"square": 30, "name": "Pacific Avenue", "price": 300, "rent": [26, 130, 390, 900, 1100, 1275]},
    {"square": 31, "name": "North Carolina Avenue", "price": 300, "rent": [26, 130, 390, 900, 1100, 1275]},
    {"square": 32, "name": "Community Chest", "price": 0},
    {"square": 33, "name": "Pennsylvania Avenue", "price": 320, "rent": [28, 150, 450, 1000, 1200, 1400]},
    {"square": 34, "name": "Short Line Railroad", "price": 200, "rent": [25, 50, 100, 200]},
    {"square": 35, "name": "Chance", "price": 0},
    {"square": 36, "name": "Park Place", "price": 350, "rent": [35, 175, 500, 1100, 1300, 1500]},
    {"square": 37, "name": "Luxury Tax", "price": 0},
    {"square": 38, "name": "Boardwalk", "price": 400, "rent": [50, 200, 600, 1400, 1700, 2000]}
]

chance_cards = [
    "Advance to GO",
    "Go to Jail",
    "Pay Poor Tax of $15",
    "Your building and loan matures. Collect $150",
    "You have won a crossword competition. Collect $100",
    "Bank pays you dividend of $50",
    "Get out of Jail Free",
    "Advance to Illinois Ave",
    "Advance to St. Charles Place",
    "Take a ride on the Reading Railroad",
    "Advance to Boardwalk",
    "Advance to the nearest Utility",
    "Advance to the nearest Railroad",
    "You are assessed for street repairs: $40 per house, $115 per hotel",
    "Pay each player $50",
    "Collect $150"
]

community_chest_cards = [
    "Advance to GO",
    "Bank error in your favor. Collect $200",
    "Doctor's fees. Pay $50",
    "From sale of stock you get $50",
    "Get out of Jail Free",
    "Go to Jail",
    "Grand Opera Night. Collect $50 from every player",
    "Holiday Fund matures. Receive $100",
    "Income tax refund. Collect $20",
    "It is your birthday. Collect $10 from each player",
    "Life insurance matures. Collect $100",
    "Pay hospital fees of $100",
    "Pay school fees of $150",
    "Receive $25 consultancy fee",
    "You have won second prize in a beauty contest. Collect $10",
    "You inherit $100"
]

def draw_card(cards):
    return random.choice(cards)

def display_board(players, board):
    table = PrettyTable()
    table.field_names = ["Square", "Property", "Price", "Rent", "Owner", "Houses", "Hotels"]
    for property in board:
        owner = ""
        houses = ""
        hotels = ""
        for player in players:
            for p in player.properties:
                if p['name'] == property['name']:
                    owner = player.name
                    houses = player.houses[property['name']]
                    hotels = player.hotels[property['name']]
                    break
        table.add_row([property['square'], property['name'], property.get('price', ''), property.get('rent', ''), owner, houses, hotels])
    print(table)

def play_game(players, board, chance_cards, community_chest_cards):
    while not all(player.is_bankrupt for player in players[1:]):
        for player in players:
            if player.is_bankrupt:
                continue

            print(f"\n{player.name}'s turn. Current money: ${player.money}")
            display_board(players, board)

            if player.in_jail:
                if player.get_out_of_jail_free:
                    player.get_out_of_jail_free = False
                    player.in_jail = False
                    player.jail_turns = 0
                    print(f"{player.name} used a 'Get out of Jail Free' card to get out of jail.")
                else:
                    if player.jail_turns < 3:
                        roll1, roll2 = roll_dice()
                        if roll1 == roll2:
                            player.in_jail = False
                            player.jail_turns = 0
                            print(f"{player.name} rolled doubles to get out of jail.")
                        else:
                            player.jail_turns += 1
                            print(f"{player.name} did not roll doubles and is still in jail.")
                            continue
                    else:
                        if player.money >= 50:
                            player.money -= 50
                            player.in_jail = False
                            player.jail_turns = 0
                            print(f"{player.name} paid $50 to get out of jail.")
                        else:
                            player.is_bankrupt = True
                            print(f"{player.name} went bankrupt trying to pay to get out of jail.")
                            continue

            roll1, roll2 = roll_dice()
            move = roll1 + roll2
            print(f"{player.name} rolled {roll1} and {roll2}, moving {move} spaces.")

            if roll1 == roll2:
                player.consecutive_doubles += 1
                if player.consecutive_doubles == 3:
                    player.position = 10
                    player.in_jail = True
                    player.jail_turns = 0
                    player.consecutive_doubles = 0
                    print(f"{player.name} rolled three consecutive doubles and is sent to jail.")
                    continue
            else:
                player.consecutive_doubles = 0

            previous_position = player.position
            player.position = (player.position + move) % len(board)
            if player.position < previous_position:
                player.money += 200
                print(f"{player.name} passed GO and collected $200.")

            current_square = board[player.position]

            print(f"{player.name} landed on {current_square['name']}.")

            if current_square['name'] == "Go to Jail":
                player.position = 10
                player.in_jail = True
                player.jail_turns = 0
                print(f"{player.name} is sent to jail.")

            elif current_square['name'] == "Community Chest":
                card = draw_card(community_chest_cards)
                print(f"Community Chest: {card}")
                handle_card(player, card, players)

            elif current_square['name'] == "Chance":
                card = draw_card(chance_cards)
                print(f"Chance: {card}")
                handle_card(player, card, players)

            elif 'price' in current_square and current_square['price'] > 0:
                owner = None
                for p in players:
                    for prop in p.properties:
                        if prop['name'] == current_square['name']:
                            owner = p
                            break
                if owner is None:
                    if player.money >= current_square['price']:
                        player.money -= current_square['price']
                        player.properties.append(current_square)
                        print(f"{player.name} bought {current_square['name']} for ${current_square['price']}.")
                    else:
                        print(f"{player.name} cannot afford {current_square['name']}.")
                elif owner != player:
                    rent = current_square['rent'][0]
                    if player.money >= rent:
                        player.money -= rent
                        owner.money += rent
                        print(f"{player.name} paid ${rent} rent to {owner.name}.")
                    else:
                        player.is_bankrupt = True
                        print(f"{player.name} went bankrupt.")
                        owner.money += player.money
                        player.money = 0

def handle_card(player, card, players):
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
        player.position = 39
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
        total_cost = player.houses * 40 + player.hotels * 115
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

def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

players = [Player("Player 1"), Player("Player 2")]
play_game(players, board, chance_cards, community_chest_cards)
