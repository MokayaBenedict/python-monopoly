import random
import json
import signal
import sys

# Define the Monopoly board
board = [
    "GO", "Mediterranean Avenue", "Community Chest", "Baltic Avenue", "Income Tax",
    "Reading Railroad", "Oriental Avenue", "Chance", "Vermont Avenue", "Connecticut Avenue",
    "Jail", "St. Charles Place", "Electric Company", "Virginia Avenue",
    "Pennsylvania Railroad", "St. James Place", "Community Chest", "Tennessee Avenue",
    "New York Avenue", "Free Parking", "Kentucky Avenue", "Chance", "Indiana Avenue",
    "Illinois Avenue", "B&O Railroad", "Atlantic Avenue", "Ventnor Avenue",
    "Water Works", "Marvin Gardens", "Go to Jail", "Pacific Avenue",
    "North Carolina Avenue", "Community Chest", "Pennsylvania Avenue",
    "Short Line Railroad", "Chance", "Park Place", "Luxury Tax", "Boardwalk"
]

property_prices = {
    "Mediterranean Avenue": 60, "Baltic Avenue": 60, "Reading Railroad": 200, 
    "Oriental Avenue": 100, "Vermont Avenue": 100, "Connecticut Avenue": 120, 
    "St. Charles Place": 140, "Electric Company": 150, "Virginia Avenue": 160, 
    "Pennsylvania Railroad": 200, "St. James Place": 180, "Tennessee Avenue": 180, 
    "New York Avenue": 200, "Kentucky Avenue": 220, "Indiana Avenue": 220, 
    "Illinois Avenue": 240, "B&O Railroad": 200, "Atlantic Avenue": 260, 
    "Ventnor Avenue": 260, "Water Works": 150, "Marvin Gardens": 280, 
    "Pacific Avenue": 300, "North Carolina Avenue": 300, "Pennsylvania Avenue": 320, 
    "Short Line Railroad": 200, "Park Place": 350, "Boardwalk": 400
}


# Define the Player class
class Player:
    def __init__(self, name, position=0, money=1500, properties=None):
        self.name = name
        self.position = position
        self.money = money
        self.properties = properties if properties is not None else []

    def to_dict(self):
         return {
            'name': self.name,
            'position': self.position,
            'money': self.money,
            'properties':self.properties
        }
    @staticmethod
    def from_dict(data):
        return Player(data['name'], data['position'], data['money'],data['properties'])
   


    def move(self, steps):
        self.position = (self.position + steps) % len(board)
        print(f"{self.name} moved to {board[self.position]}")

    def can_buy_property(self):
        property_name = board[self.position]
        if property_name in property_prices and property_name not in [p['name'] for p in self.properties]:
            return property_name
        return None

    def buy_property(self, property_name):
        if self.money >= property_prices[property_name]:
            self.money -= property_prices[property_name]
            self.properties.append({'name': property_name, 'price': property_prices[property_name]})
            print(f"{self.name} bought {property_name} for ${property_prices[property_name]}")
        else:
            print(f"{self.name} doesn't have enough money to buy {property_name}")

# Define the game functions
def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

def save_game(players, filename='try.json'):
    game_state = {
        'players': [player.to_dict() for player in players]
    }
    with open(filename, 'w') as file:
        json.dump(game_state, file)
    print("Your game has been saved successfully.")

def load_game(filename='try.json'):
    try:
        with open(filename, 'r') as file:
            game_state = json.load(file)
            players = [Player.from_dict(player) for player in game_state['players']]
            print("Your game has been loaded successfully.")
            return players
    except FileNotFoundError:
        print("No saved game found. Starting a new game.")
        return [Player("Player 1"), Player("The PC")]



def play_game():
      # Load the game state
    players = load_game()  # Load the saved game state

    if players is None:
        # If no saved game state found, start a new game
        players = [Player("Player 1"), Player("The PC")]
        
    current_player_index = 0

    def signal_handler(sig, frame):
        save_game(players)  # Save game state before exiting the terminal or termination the app.

        print("\nGame state saved. Exiting now...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        player = players[current_player_index]
        print(f"\n{player.name}'s turn.")
        
        if player.name == "Player 1":
            input("Press Enter to roll the die.")
        else:
            print("The PC is rolling the die...")
        
        dice1, dice2 = roll_dice()
        print(f"{player.name} rolled a {dice1} and a {dice2}.")
        player.move(dice1 + dice2)

        property_name = player.can_buy_property()
        if property_name:
            if player.name == "Player 1":
                decision = input(f"Do you want to buy {property_name} for ${property_prices[property_name]}? (yes/no) ").strip().lower()
                if decision == ['yes','YES' 'Yes']:
                    print("")   
                    player.buy_property(property_name)
           
                  
            else:
                if player.money >= property_prices[property_name]:
                    player.buy_property(property_name)

        # Add more game logic here (paying rent, handling special spaces, etc.)
        
        current_player_index = (current_player_index + 1) % len(players)
        save_game(players)
if __name__ == "__main__":
    play_game()
