class Player:
    def __init__(self, name, token, dice, initial_properties):
        # Player details such as name and token chosen
        self.name = name
        self.token = token

        # Money and properties in the game
        self.money = 1500
        # Assign the same initial properties to both player and 
        #the computer
        self.properties_owned = initial_properties  
      
        #PC
        self.properties_mortgaged = []
        self.properties_unmortgaged = []

        # Player state and PC at start of the game
        self.position = 0
        self.in_jail = False
        self.jail_turns = 0
        self.get_out_of_jail_card = False
        self.bankrupt = False
        self.winner = False

        # Dice and rolling of player and PC
        self.dice = dice
        self.rolled_double = False
        self.rolled_double_count = 0

        # Cards in the game
        self.community_chest_cards = []
        self.chance_cards = []

        # Properties grouped by color
        self.properties_grouped = {
            'brown': 0,
            'lightblue': 0,
            'pink': 0,
            'yellow': 0,
            'green': 0,
            'darkblue': 0,
            'red': 0,
            'orange': 0
        }
        self.properties_grouped_count = {
            'brown': 0,
            'lightblue': 0,
            'pink': 0,
            'yellow': 0,
            'green': 0,
            'darkblue': 0,
            'red': 0,
            'orange': 0
        }
        self.properties_grouped_owned = {
            'brown': [],
            'lightblue': [],
            'pink': [],
            'yellow': [],
            'green': [],
            'darkblue': [],
            'red': [],
            'orange': []
        }
        self.properties_grouped_unmortgaged = {
            'brown': [],
            'lightblue': [],
            'pink': [],
            'yellow': [],
            'green': [],
            'darkblue': [],
            'red': [],
            'orange': []
        }
        self.properties_grouped_mortgaged = {
            'brown': [],
            'lightblue': [],
            'pink': [],
            'yellow': [],
            'green': [],
            'darkblue': [],
            'red': [],
            'orange': []
        }
        self.properties_grouped_rent = {
            'brown': 0,
            'lightblue': 0,
            'pink': 0,
            'yellow': 0,
            'green': 0,
            'darkblue': 0,
            'red': 0,
            'orange': 0
        }
        self.properties_grouped_rent_unmortgaged = {
            'brown': 0,
            'lightblue': 0,
            'pink': 0,
            'yellow': 0,
            'green': 0,
            'darkblue': 0,
            'red': 0,
            'orange': 0
        }
        self.properties_grouped_rent_mortgaged = {
            'brown': 0,
            'lightblue': 0,
            'pink': 0,
            'yellow': 0,
            'green': 0,
            'darkblue': 0,
            'red': 0,
            'orange': 0
        }
        self.properties_grouped_house_count = {
            'brown': 0,
            'lightblue': 0,
            'pink': 0,
            'yellow': 0,
            'green': 0,
            'darkblue': 0,
            'red': 0,
            'orange': 0
        }
        self.properties_grouped_hotel_count = {
            'brown': 0,
            'lightblue': 0,
            'pink': 0,
            'yellow': 0,
            'green': 0,
            'darkblue': 0,
            'red': 0,
            'orange': 0
        }

        self.net_worth = self.calculate_net_worth()

    def calculate_net_worth(self):
        # Calculate net worth based on money and properties gained in the game
        properties_value = sum(self.properties_owned)
        self.net_worth = self.money + properties_value
        return self.net_worth


# Define initial properties for both you and the PC
initial_properties = [500, 100, 50, 20, 10, 5, 1]  

# List of tokens
tokens = ["race car", "thimble", "shoe", "Scottie dog", "battleship", "top hat", "iron", "wheelbarrow"]

# Method for either the comp or player to choose a token
def selectToken(player_name):
    while True:
        print("Available tokens:", ", ".join(tokens))
        token = input(f"{player_name}, choose your token: ").strip().lower()
        if token in tokens:
            tokens.remove(token)  # Remove the selected token from the token list if token is selected
            return token
        print("Invalid choice. Please select a valid token.")

# Player selects their token
player_token = selectToken("Your Token")

# PC selects a random token from the remaining tokens
import random
computer_token = random.choice(tokens)
tokens.remove(computer_token)

# Create instances of the Player class for you and the PC with the same initial properties
player_me = Player("Player", player_token, "Your Dice", initial_properties)
computer_player = Player("Computer", computer_token, "Computer Dice", initial_properties)

# Print the net worth of both players to verify
print(f"Player net worth: {player_me.net_worth}")
print(f"Computer net worth: {computer_player.net_worth}")

# Print selected tokens to verify
print(f"Player token is: {player_me.token}")
print(f"Computer token is: {computer_player.token}")
