class Player:
    def __init__(self, name, token, dice, initial_properties):
        # Player details such as name and token chosen
        self.name = name
        self.token = token

        # Money and properties in the game
        self.money = 1500
        self.properties_owned = initial_properties  # Assign the same initial properties to both players
        self.properties_mortgaged = []
        self.properties_unmortgaged = []

        # Player state and computer at start of the game
        self.position = 0
        self.in_jail = False
        self.jail_turns = 0
        self.get_out_of_jail_card = False
        self.bankrupt = False
        self.winner = False

        # Dice and rolling of player and computer
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
        self.net_worth = self.money + sum(self.properties_owned)
        self.net_worth_rent_mortgaged = self.money + sum(self.properties_mortgaged)
        self.net_worth_house_count = self.money + sum(self.properties_grouped_house_count.values())
        self.net_worth_hotel_count = self.money + sum(self.properties_grouped_hotel_count.values())
        self.net_worth_rent_unmortgaged = self.money + sum(self.properties_unmortgaged)
        self.net_worth_rent_unmortgaged_house_count = self.money + sum(self.properties_unmortgaged)
        self.net_worth_rent_unmortgaged_hotel_count = self.money + sum(self.properties_grouped_unmortgaged.values())
        self.net_worth_rent_mortgaged_house_count = self.money + sum(self.properties_mortgaged)
        self.net_worth_rent_mortgaged_hotel_count = self.money + sum(self.properties_mortgaged)
        self.net_worth_total = (self.net_worth +
                                self.net_worth_rent_mortgaged +
                                self.net_worth_house_count +
                                self.net_worth_hotel_count)
        return self.net_worth_total


# Define initial properties for both you and the computer
initial_properties = [500, 100, 50, 20, 10, 5, 1]  

# List of my 8 tokens
tokens = ["race car", "thimble", "shoe", "Scottie dog", "battleship", "top hat", "iron", "wheelbarrow"]

# method for either the comp or playerMe to choose a token
def selectToken(playerToken):
    while True:
        print("Available tokens:", ", ".join(tokens))
        token = input(f"{playerToken}, choose your token: ").strip().upper()
        if token in tokens:
            tokens.remove(token)  # Remove the selected token from the  token list
            #return token
        #print("Invalid choice. Please select a valid token.")

# User selects their token
playerToken = selectToken("my Token")

# Computer selects a random token from the remaining tokens
import random
computer_token = random.choice(tokens)
tokens.remove(computer_token)

# Create instances of the Player class for you and the computer with the same initial properties
player_me = Player("myName", playerToken, "Your Dice", initial_properties)
computer_player = Player("Computer", computer_token, "Computer Dice", initial_properties)

# Print the net worth of both players to verify
print(f"Player net worth: {player_me.net_worth}")
print(f"Computer net worth: {computer_player.net_worth}")

# Print selected tokens to verify
print(f"Player token: {player_me.token}")
print(f"Computer token: {computer_player.token}")

      