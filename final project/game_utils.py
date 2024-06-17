from game_utils import buy_property, buy_house, buy_hotel

def computer_decision(player, board):
    """Make decisions for the computer player."""

    # If the player has more than $500, consider buying properties, houses, or hotels
    if player.money > 500:
        # Iterate over each square on the board
        for square in board:
            # Check if the square is a purchasable property and not already owned by the player
            if square['price'] > 0 and square['name'] not in [prop['name'] for prop in player.properties] and player.money >= square['price']:
                # Buy the property if the player has enough money
                buy_property(player, square)
                break  # Exit the loop after buying one property
        
        # Iterate over the player's properties
        for property in player.properties:
            # If the property has less than 4 houses, buy a house
            if player.houses[property['name']] < 4:
                buy_house(player, property['name'])
            # If the property has exactly 4 houses, buy a hotel
            elif player.houses[property['name']] == 4:
                buy_hotel(player, property['name'])

    # If the player has less than $200, consider mortgaging properties
    elif player.money < 200:
        # Iterate over the player's properties
        for property in player.properties:
            # If the property is not already mortgaged, mortgage it
            if property not in player.mortgaged_properties:
                player.mortgage(property['name'])
                break  # Exit the loop after mortgaging one property
