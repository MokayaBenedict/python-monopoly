
# computer.py

from game_utils import buy_property, buy_house, buy_hotel

def computer_decision(player, board):
    """Make decisions for the computer player."""
    if player.money > 500:
        for square in board:
            if square['price'] > 0 and square['name'] not in [prop['name'] for prop in player.properties] and player.money >= square['price']:
                buy_property(player, square)
                break
        for property in player.properties:
            if player.houses[property['name']] < 4:
                buy_house(player, property['name'])
            elif player.houses[property['name']] == 4:
                buy_hotel(player, property['name'])
    elif player.money < 200:
        for property in player.properties:
            if property not in player.mortgaged_properties:
                player.mortgage(property['name'])
                break