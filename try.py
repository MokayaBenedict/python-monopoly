import random

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
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 1500

        self.properties = []

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

def play_game():
    players = [Player("Player 1"), Player("The PC")]
    current_player_index = 0

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
                    print("You bought")   
                    player.buy_property(property_name)
           
                  
            else:
                if player.money >= property_prices[property_name]:
                    player.buy_property(property_name)

        # Add more game logic here (paying rent, handling special spaces, etc.)

        current_player_index = (current_player_index + 1) % len(players)

if __name__ == "__main__":
    play_game()
