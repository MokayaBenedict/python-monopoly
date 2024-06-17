import random
from collections import defaultdict
from prettytable import PrettyTable
import json

board = [
    {"square": 0, "name": "GO", "price": 0},
    {"square": 1, "name": "Mediterranean Avenue", "price": 60, "rent": [2, 10, 30, 90, 160, 250]},
    {"square": 2, "name": "Community Chest", "price": 0},
    {"square": 3, "name": "Baltic Avenue", "price": 60, "rent": [4, 20, 60, 180, 320, 450]},
    {"square": 4, "name": "Income Tax", "price": 20},
    {"square": 5, "name": "Reading Railroad", "price": 200, "rent": [25, 50, 100, 200]},
    {"square": 6, "name": "Oriental Avenue", "price": 100, "rent": [6, 30, 90, 270, 400, 550]},
    {"square": 7, "name": "Chance", "price": 10},
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

def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

def move_player(player, steps):
    player.position = (player.position + steps) % len(board)
    current_square = board[player.position]
    print(f"{player.name} moved to square {current_square['square']}: {current_square['name']} (${current_square.get('price', 0)})")

    if current_square['name'] in player.properties:
        print(f"{player.name} owns this property and doesn't need to pay rent.")
    else:
        for owner in [p for p in players if current_square['name'] in p.properties]:
            rent = current_square['rent'][owner.houses[current_square['name']]]
            print(f"{player.name} pays ${rent} in rent to {owner.name}")
            player.money -= rent
            owner.money += rent

    print(f"Properties owned by {player.name}:")
    for property_name in player.properties:
        print(f"- {property_name}")

def buy_property(player, square):
    if square['price'] <= player.money:
        player.money -= square['price']
        player.properties.append(square['name'])
        print(f"{player.name} bought {square['name']} for ${square['price']}")
        print(f"{player.name} has cash at hand: ${player.money}")
    else:
        print(f"{player.name} does not have enough money to buy {square['name']}")

def buy_house(player, property_name):
    for square in board:
        if square['name'] == property_name:
            if property_name in player.properties and player.money >= square['rent'][player.houses[property_name] + 1]:
                player.money -= square['rent'][player.houses[property_name] + 1]
                player.houses[property_name] += 1
                print(f"{player.name} bought a house on {property_name} for ${square['rent'][player.houses[property_name]]}")
                print(f"{player.name} has cash at hand: ${player.money}")
                return
    print(f"{player.name} cannot buy a house on {property_name}")

def buy_hotel(player, property_name):
    for square in board:
        if square['name'] == property_name:
            if property_name in player.properties and player.money >= square['rent'][5] and player.houses[property_name] == 4:
                player.money -= square['rent'][5]
                player.houses[property_name] = 5
                player.hotels[property_name] = 1
                print(f"{player.name} bought a hotel on {property_name} for ${square['rent'][5]}")
                print(f"{player.name} has cash at hand: ${player.money}")
                return
    print(f"{player.name} cannot buy a hotel on {property_name}")

def save_game(players):
    game_state = []
    for player in players:
        player_state = {
            "name": player.name,
            "position": player.position,
            "money": player.money,
            "properties": player.properties,
            "houses": dict(player.houses),
            "hotels": dict(player.hotels),
            "mortgaged_properties": player.mortgaged_properties,
            "is_bankrupt": player.is_bankrupt
        }
        game_state.append(player_state)

    with open("game_state.json", "w") as f:
        json.dump(game_state, f)
    print("Game state saved.")

def load_game():
    try:
        with open("game_state.json", "r") as f:
            game_state = json.load(f)
        players = []
        for player_state in game_state:
            player = Player(player_state["name"])
            player.position = player_state["position"]
            player.money = player_state["money"]
            player.properties = player_state["properties"]
            player.houses = defaultdict(int, player_state["houses"])
            player.hotels = defaultdict(int, player_state["hotels"])
            player.mortgaged_properties = player_state["mortgaged_properties"]
            player.is_bankrupt = player_state["is_bankrupt"]
            players.append(player)

        print("Game state loaded.")
        return players
    except FileNotFoundError:
        print("No saved game found.")
        return None

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
            if property['name'] in player.properties:
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
            current_square = board[player.position]
            print(f"{player.name} moved to square {current_square['square']}: {current_square['name']} (${current_square.get('price', 0)})")

            if current_square['name'] not in player.properties and current_square['price'] > 0:
                buy_property(player, current_square)

            if current_square['name'] in ["Chance", "Community Chest"]:
                card = draw_card(chance_cards if current_square['name'] == "Chance" else community_chest_cards)
                print(f"{player.name} drew '{card}'.")
                if card == "Advance to GO":
                    player.money += 200
                   
