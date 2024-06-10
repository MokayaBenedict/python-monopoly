import random

# Define the game board
board = [
    {"square": 0, "name": "GO", "price": 0, "rent": 0, "owner": None},
    {"square": 1, "name": "Mediterranean Avenue", "price": 60, "rent": 2, "owner": None},
    {"square": 2, "name": "Community Chest", "price": 0, "rent": 0, "owner": None},
    {"square": 3, "name": "Baltic Avenue", "price": 60, "rent": 4, "owner": None},
    {"square": 4, "name": "Income Tax", "price": 0, "rent": 0, "owner": None},
    {"square": 5, "name": "Reading Railroad", "price": 200, "rent": 25, "owner": None},
    {"square": 6, "name": "Oriental Avenue", "price": 100, "rent": 6, "owner": None},
    {"square": 7, "name": "Chance", "price": 0, "rent": 0, "owner": None},
    {"square": 8, "name": "Vermont Avenue", "price": 100, "rent": 6, "owner": None},
    {"square": 9, "name": "Connecticut Avenue", "price": 120, "rent": 8, "owner": None},
    {"square": 10, "name": "Jail", "price": 0, "rent": 0, "owner": None},
    {"square": 11, "name": "St. Charles Place", "price": 140, "rent": 10, "owner": None},
    {"square": 12, "name": "Electric Company", "price": 150, "rent": 15, "owner": None},
    {"square": 13, "name": "Virginia Avenue", "price": 160, "rent": 12, "owner": None},
    {"square": 14, "name": "Pennsylvania Railroad", "price": 200, "rent": 25, "owner": None},
    {"square": 15, "name": "St. James Place", "price": 180, "rent": 14, "owner": None},
    {"square": 16, "name": "Community Chest", "price": 0, "rent": 0, "owner": None},
    {"square": 17, "name": "Tennessee Avenue", "price": 180, "rent": 14, "owner": None},
    {"square": 18, "name": "New York Avenue", "price": 200, "rent": 16, "owner": None},
    {"square": 19, "name": "Free Parking", "price": 0, "rent": 0, "owner": None},
    {"square": 20, "name": "Kentucky Avenue", "price": 220, "rent": 18, "owner": None},
    {"square": 21, "name": "Chance", "price": 0, "rent": 0, "owner": None},
    {"square": 22, "name": "Indiana Avenue", "price": 220, "rent": 18, "owner": None},
    {"square": 23, "name": "Illinois Avenue", "price": 240, "rent": 20, "owner": None},
    {"square": 24, "name": "B&O Railroad", "price": 200, "rent": 25, "owner": None},
    {"square": 25, "name": "Atlantic Avenue", "price": 260, "rent": 22, "owner": None},
    {"square": 26, "name": "Ventnor Avenue", "price": 260, "rent": 22, "owner": None},
    {"square": 27, "name": "Water Works", "price": 150, "rent": 15, "owner": None},
    {"square": 28, "name": "Marvin Gardens", "price": 280, "rent": 24, "owner": None},
    {"square": 29, "name": "Go to Jail", "price": 0, "rent": 0, "owner": None},
    {"square": 30, "name": "Pacific Avenue", "price": 300, "rent": 26, "owner": None},
    {"square": 31, "name": "North Carolina Avenue", "price": 300, "rent": 26, "owner": None},
    {"square": 32, "name": "Community Chest", "price": 0, "rent": 0, "owner": None},
    {"square": 33, "name": "Pennsylvania Avenue", "price": 320, "rent": 28, "owner": None},
    {"square": 34, "name": "Short Line Railroad", "price": 200, "rent": 25, "owner": None},
    {"square": 35, "name": "Chance", "price": 0, "rent": 0, "owner": None},
    {"square": 36, "name": "Park Place", "price": 350, "rent": 35, "owner": None},
    {"square": 37, "name": "Luxury Tax", "price": 0, "rent": 0, "owner": None},
    {"square": 38, "name": "Boardwalk", "price": 400, "rent": 50, "owner": None}
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
    current_square = board[player.position]
    print(f"{player.name} moved to square {current_square['square']}: {current_square['name']} (${current_square['price']})")
    if current_square['name'] == "Go to Jail":
        player.position = 10  # Move player to Jail
        print(f"{player.name} goes to Jail!")
    elif current_square['owner'] and current_square['owner'] != player:
        pay_rent(player, current_square)

def buy_property(player, square):
    if square['price'] <= player.money:
        player.money -= square['price']
        player.property.append(square['name'])
        square['owner'] = player
        print(f"{player.name} bought {square['name']} for ${square['price']}")
        print(f"{player.name} has ${player.money} remaining.")
    else:
        print(f"{player.name} does not have enough money to buy {square['name']}")

def pay_rent(player, square):
    rent = square.get('rent', 0)
    owner = square.get('owner')
    if owner and owner != player:
        if player.money >= rent:
            player.money -= rent
            owner.money += rent
            print(f"{player.name} paid ${rent} rent to {owner.name}")
        else:
            print(f"{player.name} cannot pay the rent and goes bankrupt!")
            player.money = 0  # Adjust for bankruptcy handling if needed

def play_game():
    players = [Player("Player 1"), Player("Player 2")]
    current_player_index = 0
    turn_count = 0
    max_turns = 20  # Set a condition to stop the game after a certain number of turns

    while turn_count < max_turns:
        player = players[current_player_index]
        print(f"\n{player.name}'s turn.")
        input("Press Enter to roll the dice.\n")
        dice1, dice2 = roll_dice()
        print(f"You rolled a {dice1} and a {dice2}.")
        move_player(player, dice1 + dice2)

        current_square = board[player.position]
        if current_square['price'] > 0 and current_square['owner'] is None:
            buy_property(player, current_square)

        print(f"Properties owned by {player.name}: {', '.join(player.property)}")
        
        if dice1 != dice2:  # If the player didn't roll doubles, move to the next player
            current_player_index = (current_player_index + 1) % len(players)
            turn_count += 1

if __name__ == "__main__":
    play_game()
