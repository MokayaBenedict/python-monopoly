import random
import json
from collections import defaultdict
from prettytable import PrettyTable

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 1500
        self.properties = []
        self.houses = defaultdict(int)
        self.hotels = defaultdict(int)
        self.is_bankrupt = False

# Board and cards setup
board = [
    {"square": 0, "name": "Go", "price": 0, "rent": [0]},
    {"square": 1, "name": "Mediterranean Avenue", "price": 60, "rent": [2, 10, 30, 90, 160, 250]},
    {"square": 2, "name": "Community Chest", "price": 0, "rent": [0]},
    {"square": 3, "name": "Baltic Avenue", "price": 60, "rent": [4, 20, 60, 180, 320, 450]},
    {"square": 4, "name": "Income Tax", "price": 0, "rent": [0]},
    {"square": 5, "name": "Reading Railroad", "price": 200, "rent": [25, 50, 100, 200]},
    {"square": 6, "name": "Oriental Avenue", "price": 100, "rent": [6, 30, 90, 270, 400, 550]},
    {"square": 7, "name": "Chance", "price": 0, "rent": [0]},
    {"square": 8, "name": "Vermont Avenue", "price": 100, "rent": [6, 30, 90, 270, 400, 550]},
    {"square": 9, "name": "Connecticut Avenue", "price": 120, "rent": [8, 40, 100, 300, 450, 600]},
    {"square": 10, "name": "Jail", "price": 0, "rent": [0]},
    {"square": 11, "name": "St. Charles Place", "price": 140, "rent": [10, 50, 150, 450, 625, 750]},
    {"square": 12, "name": "Electric Company", "price": 150, "rent": [4, 10]},
    {"square": 13, "name": "States Avenue", "price": 140, "rent": [10, 50, 150, 450, 625, 750]},
    {"square": 14, "name": "Virginia Avenue", "price": 160, "rent": [12, 60, 180, 500, 700, 900]},
    {"square": 15, "name": "Pennsylvania Railroad", "price": 200, "rent": [25, 50, 100, 200]},
    {"square": 16, "name": "St. James Place", "price": 180, "rent": [14, 70, 200, 550, 750, 950]},
    {"square": 17, "name": "Community Chest", "price": 0, "rent": [0]},
    {"square": 18, "name": "Tennessee Avenue", "price": 180, "rent": [14, 70, 200, 550, 750, 950]},
    {"square": 19, "name": "New York Avenue", "price": 200, "rent": [16, 80, 220, 600, 800, 1000]},
    {"square": 20, "name": "Free Parking", "price": 0, "rent": [0]},
    {"square": 21, "name": "Kentucky Avenue", "price": 220, "rent": [18, 90, 250, 700, 875, 1050]},
    {"square": 22, "name": "Chance", "price": 0, "rent": [0]},
    {"square": 23, "name": "Indiana Avenue", "price": 220, "rent": [18, 90, 250, 700, 875, 1050]},
    {"square": 24, "name": "Illinois Avenue", "price": 240, "rent": [20, 100, 300, 750, 925, 1100]},
    {"square": 25, "name": "B&O Railroad", "price": 200, "rent": [25, 50, 100, 200]},
    {"square": 26, "name": "Atlantic Avenue", "price": 260, "rent": [22, 110, 330, 800, 975, 1150]},
    {"square": 27, "name": "Ventnor Avenue", "price": 260, "rent": [22, 110, 330, 800, 975, 1150]},
    {"square": 28, "name": "Water Works", "price": 150, "rent": [4, 10]},
    {"square": 29, "name": "Marvin Gardens", "price": 280, "rent": [24, 120, 360, 850, 1025, 1200]},
    {"square": 30, "name": "Go to Jail", "price": 0, "rent": [0]},
    {"square": 31, "name": "Pacific Avenue", "price": 300, "rent": [26, 130, 390, 900, 1100, 1275]},
    {"square": 32, "name": "North Carolina Avenue", "price": 300, "rent": [26, 130, 390, 900, 1100, 1275]},
    {"square": 33, "name": "Community Chest", "price": 0, "rent": [0]},
    {"square": 34, "name": "Pennsylvania Avenue", "price": 320, "rent": [28, 150, 450, 1000, 1200, 1400]},
    {"square": 35, "name": "Short Line Railroad", "price": 200, "rent": [25, 50, 100, 200]},
    {"square": 36, "name": "Chance", "price": 0, "rent": [0]},
    {"square": 37, "name": "Park Place", "price": 350, "rent": [35, 175, 500, 1100, 1300, 1500]},
    {"square": 38, "name": "Luxury Tax", "price": 0, "rent": [0]},
    {"square": 39, "name": "Boardwalk", "price": 400, "rent": [50, 200, 600, 1400, 1700, 2000]}
]

chance_cards = [
    "Advance to Go (Collect $200)",
    "Go to Jail. Go directly to Jail, do not pass Go, do not collect $200.",
    "Advance to Illinois Avenue. If you pass Go, collect $200.",
    "Advance to St. Charles Place. If you pass Go, collect $200.",
    "Take a trip to Reading Railroad. If you pass Go, collect $200.",
    "Bank pays you dividend of $50.",
    "Get out of Jail Free. This card may be kept until needed or traded.",
    "Go back 3 spaces.",
    "Pay poor tax of $15.",
    "You have been elected Chairman of the Board. Pay each player $50.",
    "Your building loan matures. Collect $150.",
    "You have won a crossword competition. Collect $100."
]

community_chest_cards = [
    "Bank error in your favor. Collect $200.",
    "Doctor's fees. Pay $50.",
    "From sale of stock you get $50.",
    "Get Out of Jail Free.",
    "Go to Jail. Go directly to jail, do not pass Go, do not collect $200.",
    "Grand Opera Night. Collect $50 from every player for opening night seats.",
    "Holiday Fund matures. Receive $100.",
    "Income tax refund. Collect $20.",
    "It is your birthday. Collect $10 from every player.",
    "Life insurance matures. Collect $100.",
    "Pay hospital fees of $100.",
    "Pay school fees of $50.",
    "Receive $25 consultancy fee.",
    "You are assessed for street repairs. $40 per house. $115 per hotel.",
    "You have won second prize in a beauty contest. Collect $10.",
    "You inherit $100."
]

def draw_chance_card(player):
    card = random.choice(chance_cards)
    print(f"Chance Card: {card}")
    apply_card_effect(card, player, player1 if player == player2 else player2)

def draw_community_chest_card(player):
    card = random.choice(community_chest_cards)
    print(f"Community Chest Card: {card}")
    apply_card_effect(card, player, player1 if player == player2 else player2)

def apply_card_effect(card, player, other_player):
    if "Collect $200" in card:
        player.money += 200
    elif "Go to Jail" in card:
        player.position = 10
    elif "Advance to Illinois Avenue" in card:
        player.position = 24
        player.money += 200 if player.position < 24 else 0
    elif "Advance to St. Charles Place" in card:
        player.position = 11
        player.money += 200 if player.position < 11 else 0
    elif "Take a trip to Reading Railroad" in card:
        player.position = 5
        player.money += 200 if player.position < 5 else 0
    elif "Bank pays you dividend of $50" in card:
        player.money += 50
    elif "Get out of Jail Free" in card:
        # Handle the  "Get out of Jail Free" card logic if needed.
        pass
    elif "Go back 3 spaces" in card:
        player.position -= 3
    elif "Pay poor tax of $15" in card:
        player.money -= 15
    elif "Pay each player $50" in card:
        player.money -= 50
        other_player.money += 50
    elif "Collect $150" in card:
        player.money += 150
    elif "Collect $100" in card:
        player.money += 100
    elif "Bank error in your favor" in card:
        player.money += 200
    elif "Doctor's fees" in card:
        player.money -= 50
    elif "Get Out of Jail Free" in card:
        # Handle the "Get out of Jail Free" card logic if needed.
        pass
    elif "Grand Opera Night" in card:
        player.money += 50
        other_player.money -= 50
    elif "Holiday Fund matures" in card:
        player.money += 100
    elif "Income tax refund" in card:
        player.money += 20
    elif "It is your birthday" in card:
        player.money += 10
        other_player.money -= 10
    elif "Life insurance matures" in card:
        player.money += 100
    elif "Pay hospital fees" in card:
        player.money -= 100
    elif "Pay school fees" in card:
        player.money -= 50
    elif "Receive $25 consultancy fee" in card:
        player.money += 25
    elif "You are assessed for street repairs" in card:
        # Calculate cost for street repairs based on number of houses and hotels owned by player or pc.
        total_cost = 40 * sum(player.houses.values()) + 115 * sum(player.hotels.values())
        player.money -= total_cost
    elif "You have won second prize in a beauty contest" in card:
        player.money += 10
    elif "You inherit $100" in card:
        player.money += 100

def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

def move_player(player, steps):
    player.position = (player.position + steps) % len(board)
    current_square = board[player.position]

    print(f"{player.name} landed on {current_square['name']}.")

    if current_square["name"] == "Chance":
        draw_chance_card(player)
    elif current_square["name"] == "Community Chest":
        draw_community_chest_card(player)
    elif current_square["name"] == "Go to Jail":
        player.position = 10
    elif current_square["name"] == "Income Tax":
        player.money -= 200
    elif current_square["name"] == "Luxury Tax":
        player.money -= 100

    if player.money < 0:
        player.is_bankrupt = True
        print(f"{player.name} is bankrupt!")

def buy_property(player, current_square):
    if current_square["price"] > player.money:
        print(f"{player.name} does not have enough money to buy {current_square['name']}.")
    else:
        player.money -= current_square["price"]
        player.properties.append(current_square["name"])
        print(f"{player.name} bought {current_square['name']} for ${current_square['price']}.")

def buy_house(player, property_name):
    if player.houses[property_name] < 4:
        cost = board[next(i for i, v in enumerate(board) if v["name"] == property_name)]["price"] // 2
        if player.money >= cost:
            player.money -= cost
            player.houses[property_name] += 1
            print(f"{player.name} bought a house on {property_name} for ${cost}.")
        else:
            print(f"{player.name} does not have enough money to buy a house on {property_name}.")
    else:
        print(f"{player.name} cannot buy more houses on {property_name}.")

def buy_hotel(player, property_name):
    if player.houses[property_name] == 4:
        cost = board[next(i for i, v in enumerate(board) if v["name"] == property_name)]["price"]
        if player.money >= cost:
            player.money -= cost
            player.houses[property_name] = 0
            player.hotels[property_name] += 1
            print(f"{player.name} bought a hotel on {property_name} for ${cost}.")
        else:
            print(f"{player.name} does not have enough money to buy a hotel on {property_name}.")
    else:
        print(f"{player.name} cannot buy a hotel on {property_name} without 4 houses.")

def save_game(player1, player2):
    with open("monopoly_save.json", "w") as file:
        json.dump({
            "player1": player1.__dict__,
            "player2": player2.__dict__,
            "player1_houses": dict(player1.houses),
            "player2_houses": dict(player2.houses),
            "player1_hotels": dict(player1.hotels),
            "player2_hotels": dict(player2.hotels)
        }, file)
    print("Game saved successfully.")
def load_game():
    try:
        with open("monopoly_save.json", "r") as file:
            data = json.load(file)
            player1 = Player("Player 1")
            player2 = Player("Computer")
            player1.__dict__.update(data["player1"])
            player2.__dict__.update(data["player2"])
            
    
            player1.houses.update(data.get("player1_houses", {}))
            player2.houses.update(data.get("player2_houses", {}))
            player1.hotels.update(data.get("player1_hotels", {}))
            player2.hotels.update(data.get("player2_hotels", {}))

            print("Game loaded successfully.")
            return player1, player2
    except FileNotFoundError:
        print("No saved game found.")
        return None, None


def play_game():
    global player1, player2
    player1, player2 = load_game()
    if player1 is None or player2 is None:
        player1 = Player("Player 1")
        player2 = Player("Computer")

    current_player = player1

    while True:
        if current_player.is_bankrupt:
            print(f"{current_player.name} is bankrupt and cannot continue.")
            break

        print(f"\n{current_player.name}'s turn.")
        input("Press Enter to roll the dice.\n")
        dice1, dice2 = roll_dice()
        print(f"You rolled a {dice1} and a {dice2}.")
        move_player(current_player, dice1 + dice2)

        if current_player.is_bankrupt:
            break

        current_square = board[current_player.position]
        if current_square['name'] not in current_player.properties and current_square['price'] > 0:
            buy_property(current_player, current_square)

        if current_player.name == "Player 1":
            print("What would you like to do?")
            print("1. Buy a house")
            print("2. Buy a hotel")
            print("3. Save and exit")
            print("4. End turn")
            choice = input("Enter your choice (1-4): ")
            if choice == "1":
                for property in current_player.properties:
                    print(f"{property} ({current_player.houses[property]} houses)")
                prop = input("Enter the property to buy a house: ")
                buy_house(current_player, prop)
            elif choice == "2":
                for property in current_player.properties:
                    if current_player.houses[property] == 4:
                        print(f"{property} (4 houses)")
                prop = input("Enter the property to buy a hotel: ")
                buy_hotel(current_player, prop)
            elif choice == "3":
                save_game(player1, player2)
                return
            else:
                current_player = player2
        else:
            # Computer player's turn
            current_player = player1

        # Display the player information table
        player_table = PrettyTable()
        player_table.field_names = ["Player", "Position", "Money", "Properties"]
        player_table.add_row(["\033[94mPlayer 1\033[0m", player1.position, f"\033[94m${player1.money}\033[0m", ", \n".join(player1.properties)])
        player_table.add_row(["\033[91mComputer\033[0m", player2.position, f"\033[91m${player2.money}\033[0m", ",\n ".join(player2.properties)])
        print("\nPlayer Information:")
        print(player_table)

if __name__ == "__main__":
    play_game()