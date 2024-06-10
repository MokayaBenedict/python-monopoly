import random
from collections import defaultdict
from prettytable import PrettyTable

# Define the player class
class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 1500
        self.properties = []
        self.houses = defaultdict(int)
        self.hotels = defaultdict(int)


# Define the game board
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

# Define the game functions
def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

def move_player(player, steps):
    player.position = (player.position + steps) % 40
    if player.position >= len(board):
        player.position -= len(board)
    current_square = board[player.position]
    print(f"{player.name} moved to square {current_square['square']}: {current_square['name']} (${current_square['price']})")

    # Check if the current square is owned, and collect rent if it is
    if current_square['name'] in player.properties:
        print(f"{player.name} owns this property and doesn't need to pay rent.")
    else:
        for owner in [p for p in [player1, player2] if current_square['name'] in p.properties]:
            rent = current_square['rent'][owner.houses[current_square['name']]]
            print(f"{player.name} pays ${rent} in rent to {owner.name}")
            player.money -= rent
            owner.money += rent

    # Print the player's properties
    print(f"Properties owned by {player.name}:")
    for property in player.properties:
        print(f"- {property}")

def buy_property(player, square):
    if square['price'] <= player.money:
        player.money -= square['price']
        player.properties.append(square['name'])
        print(f"{player.name} bought {square['name']} for ${square['price']}")
        print(f"{player.name} has cash at hand: ${player.money}")
    else:
        print(f"{player.name} does not have enough money to buy {square['name']}")

def buy_house(player, property):
    if property in player.properties and player.money >= board[property]['rent'][player.houses[property] + 1]:
        player.money -= board[property]['rent'][player.houses[property] + 1]
        player.houses[property] += 1
        print(f"{player.name} bought a house on {property} for ${board[property]['rent'][player.houses[property]]}")
        print(f"{player.name} has cash at hand: ${player.money}")
    else:
        print(f"{player.name} cannot buy a house on {property}")

def buy_hotel(player, property):
    if property in player.properties and player.money >= board[property]['rent'][5] and player.houses[property] == 4:
        player.money -= board[property]['rent'][5]
        player.houses[property] = 5
        player.hotels[property] = 1
        print(f"{player.name} bought a hotel on {property} for ${board[property]['rent'][5]}")
        print(f"{player.name} has cash at hand: ${player.money}")
    else:
        print(f"{player.name} cannot buy a hotel on {property}")

def play_game():
    global player1, player2
    player1 = Player("Player 1")
    player2 = Player("Computer")

    current_player = player1

    while True:
        print(f"\n{current_player.name}'s turn.")
        input("Press Enter to roll the dice.\n")
        dice1, dice2 = roll_dice()
        print(f"You rolled a {dice1} and a {dice2}.")
        move_player(current_player, dice1 + dice2)

        current_square = board[current_player.position]
        if current_square['name'] not in current_player.properties and current_square['price'] > 0:
            buy_property(current_player, current_square)

        if current_player.name == "Player 1":
            print("What would you like to do?")
            print("1. Buy a house")
            print("2. Buy a hotel")
            print("3. End turn")
            choice = input("Enter your choice (1-3): ")
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
