# Text Adventure Game - Escape the Castle

# Define the rooms and items
rooms = {
    "Courtyard": {
        "description": "You are in a dark courtyard with a massive gate to the north and a narrow path to the south.",
        "exits": {"North": "Gate", "South": "Narrow Path"},
        "items": ["Key"]
    },
    "Gate": {
        "description": "You are at the castle's gate, but it's locked. There's a keyhole on the gate.",
        "exits": {"South": "Courtyard"},
        "puzzle": {
            "type": "key",
            "solved": False
        }
    },
    "Narrow Path": {
        "description": "A narrow path leads to the west and a door to the east.",
        "exits": {"West": "Torture Chamber", "East": "Dining Hall"}
    },
    "Torture Chamber": {
        "description": "You find yourself in a gruesome torture chamber. There's a lever on the wall.",
        "exits": {"East": "Narrow Path"},
        "puzzle": {
            "type": "lever",
            "solved": False
        }
    },
    "Dining Hall": {
        "description": "You enter a grand dining hall with a large chandelier. The exit is to the west.",
        "exits": {"West": "Narrow Path"},
        "items": ["Candlestick"]
    }
}

inventory = []  # Player's inventory

# Main game loop
current_room = "Courtyard"
while current_room != "Outside":
    room = rooms[current_room]

    # Display room description
    print(room["description"])

    # Check for items in the room
    if "items" in room:
        for item in room["items"]:
            print(f"You see a {item} in the room.")

    # Ask for the player's command
    command = input("What do you want to do? ").lower()

    if command == "quit":
        break

    if command in ["north", "south", "east", "west"]:
        # Handle direction commands
        if command in room["exits"]:
            current_room = room["exits"][command]
        else:
            print("You can't go that way.")
    elif command == "inventory":
        # Display player's inventory
        if not inventory:
            print("Your inventory is empty.")
        else:
            print("Inventory: " + ", ".join(inventory))
    else:
        # Handle action commands (e.g., grab, eat, pull, push)
        if "puzzle" in room:
            puzzle = room["puzzle"]
            if command == "grab" and puzzle["type"] == "key":
                if "Key" in inventory:
                    print("You already have the key.")
                else:
                    inventory.append("Key")
                    print("You've grabbed the key.")
            elif command == "pull" and puzzle["type"] == "lever":
                if not puzzle["solved"]:
                    puzzle["solved"] = True
                    print("You pull the lever, and you hear a distant rumbling sound.")
                else:
                    print("You've already pulled the lever.")
            else:
                print("You can't do that here.")
        else:
            print("You can't do that here.")

# Game over
print("You've escaped the castle! Congratulations!")
