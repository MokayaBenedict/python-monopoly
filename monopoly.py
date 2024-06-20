
import random
from collections import defaultdict
from prettytable import PrettyTable
import json

class Player:
    def __init__(self, name: str):
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

    def mortgage(self, property_name: str):
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

    def unmortgage(self, property_name: str):
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

def computer_decision(player: Player, board: list):
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

def draw_card(cards: list) -> str:
    return random.choice(cards)

def handle_card(player: Player, card_type: str, players: list):
    if card_type == "Chance":
        card = draw_card(chance_cards)
        print(f"{player.name} drew a Chance card: {card}")
        handle_chance_card(player, card, players)
    elif card_type == "Community Chest":
        card = draw_card(community_chest_cards)
        print(f"{player.name} drew a Community Chest card: {card}")
        handle_community_chest_card(player, card, players)

def handle_chance_card(player: Player, card: str, players: list):
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

def handle_community_chest_card(player: Player, card: str, players: list):
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

def roll_dice() -> tuple:
    return random.randint(1, 6), random.randint(1, 6)

def move_player(player: Player, steps: int, board: list, players: list):
    player.position = (player.position + steps) % len(board)
    current_square = board[player.position]
    print(f"{player.name} moved to square {current_square['square']}: {current_square['name']} (${current_square['price']})")

    if current_square['name'] in [prop['name'] for prop in player.properties]:
        print(f"{player.name} owns this property and doesn't need to pay rent.")
    elif current_square['price'] == 0 and current_square['name'] in ["Chance", "Community Chest"]:
        handle_card(player, current_square['name'], players)
    else:
        for owner in players:
            if current_square['name'] in [prop['name'] for prop in owner.properties] and owner != player:
                rent = current_square['rent'][owner.houses[current_square['name']]]
                print(f"{player.name} pays ${rent} in rent to {owner.name}")
                player.money -= rent
                owner.money += rent

    print(f"Properties owned by {player.name}:")
    for property in player.properties:
        print(f"- {property['name']}")

def buy_property(player: Player, square: dict):
    if square['price'] <= player.money:
        player.money -= square['price']
        player.properties.append(square)
        print(f"{player.name} bought {square['name']} for ${square['price']}")
        print(f"{player.name} has cash at hand: ${player.money}")
    else:
        print(f"{player.name} does not have enough money to buy {square['name']}")

def buy_house(player: Player, property_name: str):
    for square in board:
        if square['name'] == property_name:
            if property_name in [prop['name'] for prop in player.properties] and player.money >= square['rent'][player.houses[property_name] + 1]:
                player.money -= square['rent'][player.houses[property_name] + 1]
                player.houses[property_name] += 1
                print(f"{player.name} bought a house on {property_name} for ${square['rent'][player.houses[property_name]]}")
                print(f"{player.name} has cash at hand: ${player.money}")
                return
    print(f"{player.name} cannot buy a house on {property_name}")

def buy_hotel(player: Player, property_name: str):
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

def save_game(player1: Player, player2: Player):
    game_state = {
        "player1": {
            "name": player1.name,
            "position": player1.position,
            "money": player1.money,
            "properties": [prop['name'] for prop in player1.properties],
            "mortgaged_properties": [prop['name'] for prop in player1.mortgaged_properties],
            "houses": dict(player1.houses),
            "hotels": dict(player1.hotels),
            "is_bankrupt": player1.is_bankrupt
        },
        "player2": {
            "name": player2.name,
            "position": player2.position,
            "money": player2.money,
            "properties": [prop['name'] for prop in player2.properties],
            "mortgaged_properties": [prop['name'] for prop in player2.mortgaged_properties],
            "houses": dict(player2.houses),
            "hotels": dict(player2.hotels),
            "is_bankrupt": player2.is_bankrupt
        }
    }
    with open("game_state.json", "w") as f:
        json.dump(game_state, f)
    print("Game state saved.")

def load_game() -> tuple:
    try:
        with open("game_state.json", "r") as f:
            game_state = json.load(f)
        player1 = Player(game_state["player1"]["name"])
        player1.position = game_state["player1"]["position"]
        player1.money = game_state["player1"]["money"]
        player1.properties = [prop for prop in board if prop['name'] in game_state["player1"]["properties"]]
        player1.mortgaged_properties = [prop for prop in board if prop['name'] in game_state["player1"].get("mortgaged_properties", [])]
        player1.houses = defaultdict(int, game_state["player1"]["houses"])
        player1.hotels = defaultdict(int, game_state["player1"]["hotels"])
        player1.is_bankrupt = game_state["player1"]["is_bankrupt"]

        player2 = Player(game_state["player2"]["name"])
        player2.position = game_state["player2"]["position"]
        player2.money = game_state["player2"]["money"]
        player2.properties = [prop for prop in board if prop['name'] in game_state["player2"]["properties"]]
        player2.mortgaged_properties = [prop for prop in board if prop['name'] in game_state["player2"].get("mortgaged_properties", [])]
        player2.houses = defaultdict(int, game_state["player2"]["houses"])
        player2.hotels = defaultdict(int, game_state["player2"]["hotels"])
        player2.is_bankrupt = game_state["player2"]["is_bankrupt"]

        print("Game state loaded.")
        return player1, player2
    except FileNotFoundError:
        print("No saved game found.")
        return None, None

def player_turn(player: Player, board: list, players: list):
    print(f"\n{player.name}'s turn.")
    if player.name == "Player 1":
        input("Press Enter to roll the dice.\n")
        
    dice1, dice2 = roll_dice()
    print(f"{player.name} rolled a {dice1} and a {dice2}.")
    move_player(player, dice1 + dice2, board, players)

    current_square = board[player.position]
    if current_square['name'] not in [prop['name'] for prop in player.properties] and current_square['price'] > 0:
        buy_property(player, current_square)

    if player.name == "Player 1":
        print("What would you like to do?")
        print("1. Buy a house")
        print("2. Buy a hotel")
        print("3. Mortgage property")
        print("4. Unmortgage property")
        print("5. Save and exit")
        print("6. End turn")

        choice = input("Enter your choice (1-6): ")
        if choice == "1":
            for property in player.properties:
                print(f"{property['name']} ({player.houses[property['name']]} houses)")
            prop = input("Enter the property to buy a house: ")
            buy_house(player, prop)
        elif choice == "2":
            for property in player.properties:
                if player.houses[property['name']] == 4:
                    print(f"{property['name']} (4 houses)")
            prop = input("Enter the property to buy a hotel: ")
            buy_hotel(player, prop)
        elif choice == "3":
            for property in player.properties:
                if property['name'] not in [prop['name'] for prop in player.mortgaged_properties]:
                    print(f"{property['name']} ({player.houses[property['name']]} houses)")
            property_name = input("Enter the property to mortgage: ")
            player.mortgage(property_name)
        elif choice == "4":
            for property in player.mortgaged_properties:
                print(f"{property['name']} (mortgaged)")
            property_name = input("Enter the property to unmortgage: ")
            player.unmortgage(property_name)
        elif choice == "5":
            save_game(players[0], players[1])
            return True
    else:
        computer_decision(player, board)

    return False

def display_player_info(players: list):
    player_table = PrettyTable()
    player_table.field_names = ["Player", "Position", "Money", "Properties", "Mortgaged Properties"]
    for player in players:
        player_table.add_row([
            player.name,
            player.position,
            f"${player.money}",
            ", \n".join([prop['name'] for prop in player.properties]),
            ", \n".join([prop['name'] for prop in player.mortgaged_properties])
        ])
    print("\nPlayer Information:")
    print(player_table)

def play_game():
    player1, player2 = load_game()
    if player1 is None or player2 is None:
        player1 = Player("Player 1")
        player2 = Player("Computer")

    players = [player1, player2]
    current_player = 0

    while True:
        game_ended = player_turn(players[current_player], board, players)
        if game_ended:
            break
        current_player = (current_player + 1) % len(players)
        display_player_info(players)

if __name__ == "__main__":
    play_game()