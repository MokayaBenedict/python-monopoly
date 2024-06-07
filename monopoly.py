import random


board = [
    "GO (0)", "Mediterranean Avenue (1)", "Community Chest (2)", "Baltic Avenue (3)", "Income Tax (4)",
    "Reading Railroad (5)", "Oriental Avenue (6)", "Chance (7)", "Vermont Avenue (8)", "Connecticut Avenue (9)",
    "Jail (10)", "St. Charles Place (11)", "Electric Company (12)", "Virginia Avenue (13)",
    "Pennsylvania Railroad (14)", "St. James Place (15)", "Community Chest (16)", "Tennessee Avenue (17)",
    "New York Avenue (18)", "Free Parking (19)", "Kentucky Avenue (20)", "Chance (21)", "Indiana Avenue (22)",
    "Illinois Avenue (23)", "B&O Railroad (24)", "Atlantic Avenue (25)", "Ventnor Avenue (26)",
    "Water Works (27)", "Marvin Gardens (28)", "Go to Jail (29)", "Pacific Avenue (30)",
    "North Carolina Avenue (31)", "Community Chest (32)", "Pennsylvania Avenue (33)",
    "Short Line Railroad (34)", "Chance (35)", "Park Place (36)", "Luxury Tax (37)", "Boardwalk (38)"
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
