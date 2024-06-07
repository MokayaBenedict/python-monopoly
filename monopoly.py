import random

board = [
    {"square": 0, "name": "GO", "price": 0},
    {"square": 1, "name": "Mediterranean Avenue", "price": 60},
    {"square": 2, "name": "Community Chest", "price": 0},
    {"square": 3, "name": "Baltic Avenue", "price": 60},
    {"square": 4, "name": "Income Tax", "price": 0},
    {"square": 5, "name": "Reading Railroad", "price": 200},
    {"square": 6, "name": "Oriental Avenue", "price": 100},
    {"square": 7, "name": "Chance", "price": 0},
    {"square": 8, "name": "Vermont Avenue", "price": 100},
    {"square": 9, "name": "Connecticut Avenue", "price": 120},
    {"square": 10, "name": "Jail", "price": 0},
    {"square": 11, "name": "St. Charles Place", "price": 140},
    {"square": 12, "name": "Electric Company", "price": 150},
    {"square": 13, "name": "Virginia Avenue", "price": 160},
    {"square": 14, "name": "Pennsylvania Railroad", "price": 200},
    {"square": 15, "name": "St. James Place", "price": 180},
    {"square": 16, "name": "Community Chest", "price": 0},
    {"square": 17, "name": "Tennessee Avenue", "price": 180},
    {"square": 18, "name": "New York Avenue", "price": 200},
    {"square": 19, "name": "Free Parking", "price": 0},
    {"square": 20, "name": "Kentucky Avenue", "price": 220},
    {"square": 21, "name": "Chance", "price": 0},
    {"square": 22, "name": "Indiana Avenue", "price": 220},
    {"square": 23, "name": "Illinois Avenue", "price": 240},
    {"square": 24, "name": "B&O Railroad", "price": 200},
    {"square": 25, "name": "Atlantic Avenue", "price": 260},
    {"square": 26, "name": "Ventnor Avenue", "price": 260},
    {"square": 27, "name": "Water Works", "price": 150},
    {"square": 28, "name": "Marvin Gardens", "price": 280},
    {"square": 29, "name": "Go to Jail", "price": 0},
    {"square": 30, "name": "Go to Jail", "price": 0}
    {"square": 31, "name": "Pacific Avenue", "price": 300},
    {"square": 32, "name": "North Carolina Avenue", "price": 300},
    {"square": 33, "name": "Community Chest", "price": 0},
    {"square": 34, "name": "Pennsylvania Avenue", "price": 320},
    {"square": 35, "name": "Short Line Railroad", "price": 200},
    {"square": 36, "name": "Chance", "price": 0},
    {"square": 37, "name": "Park Place", "price": 350},
    {"square": 38, "name": "Luxury Tax", "price": 0},
    {"square": 39, "name": "Boardwalk", "price": 400}
    
   
]



# Define the player class
class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 1500
        self.property = []

# Define the game functions
def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

def move_player(player, steps):
    player.position = (player.position + steps) % 40
    print(f"{player.name} moved to {board[player.position]}")

def play_game():
    players = [Player("Player 1"), Player("Player 2")]
    current_player_index = 0

    while True:
        player = players[current_player_index]
        print(f"\n{player.name}'s turn.")
        input("Press Enter to roll the dice.")
        dice1, dice2 = roll_dice()
        print(f"You rolled a {dice1} and a {dice2}.")
        move_player(player, dice1 + dice2)

        # Add game logic here (buying properties, collecting rent, etc.)

        current_player_index = (current_player_index + 1) % len(players)

if __name__ == "__main__":
    play_game()
