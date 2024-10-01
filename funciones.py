import sys

# This is the initial state
INIT_GAME_STATE = {
    "current_room": tower, #The game starts in this room
    "solved_riddles": [], #List of solved riddles   
    "target": outside,
    "dungeon": gameover,
}

# The game initial state
game_state = INIT_GAME_STATE.copy()

def linebreak():
    """
    Imprime un salto de línea
    """
    print("\n\n")

# Personalized error message
class CustomValueError(ValueError):
    def __init__(self, message="NO! We've said a number!"):
        self.message = message
        super().__init__(self.message)

def finalInputErrors(prompt, min_value, max_value):
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        try:
            final_input = int(input(prompt))
            # Check if the number is out of range
            if final_input < min_value or final_input > max_value:
                print(f"The number {final_input} is out of range.")
            elif final_input == 14:
                print(f"Correct. The answer is: {final_input}")
                next_room = outside  
                play_room(next_room)  
                return final_input
            else:
                if attempts < max_attempts - 1:  # Only show for non-final attempts
                    print("Incorrect answer, try again.")
                    print("Good try! You're one step closer to the final answer.")
        except ValueError:
            print(CustomValueError())  # Custom error message
        finally:
            attempts += 1
            if attempts >= max_attempts:
                print("No more attempts left. Your chance to escape has vanished.")
                sys.exit()

    return None

#The inital situation is presented to the player

def start_game():
    print("Good morning, princess!\n"
    "Like every morning, you wake up in your tower.\n"
    "But in your heart you feel it, today is the day you will escape your prison forever.\n"
    "Do you want to explore your room?\n"
    "Explore to find out what is in the room.")
    play_room(game_state["current_room"])


def play_room(room):
    """
    Play a room. Check if the room being played is the target room.
    If it is, the player wins. If not, the player will explore
    (present all items in this room) or examine an item found here.
    """

    game_state["current_room"] = room
    if game_state["current_room"] == game_state["target"]:
        print("Congrats! You escaped the room!")
        sys.exit()
    elif game_state["current_room"] == dungeon:
        print("Too bad! You died!")
        sys.exit()
    else:
        print("You are now in " + room["name"])
        intended_action = input(
            "What would you like to do? Type 'explore' or 'examine'?"
        ).strip()
        if intended_action == "explore":
            explore_room(room)
            play_room(room)
        elif intended_action == "examine":
            examine_item(input("What would you like to examine?").strip())
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(room)
        linebreak()


def explore_room(room):
    """
    Look around the room. Visualize all items found in this room.
    """

    items = [i["name"] for i in object_relations[room["name"]]]
    print(
        "You explore the room. This is "
        + room["name"]
        + ". You find "
        + ", ".join(items)
    )


def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """

    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if room != current_room:
            return room
        
def examine_item(item_name):
    """
    Examine the possible items in the room.
    The type options are: door, object and clue.
    Make sure the item belongs to the current room.
    Then check if the item is a door. Tell player if the door is locked.
    If it is locked, tell them to find and solve the riddle.
    If the riddle has been solved, update the game state and ask the player
    if they want to move to the next room.
    If the riddle has not been solved, try again.
    In the game there are different traps that either lead to Game Over
    or return you to the beginning.
    If the player solves all the riddles and avoids all traps, they win!
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]:
        if item["name"] == item_name:
            output = "You examine " + item_name + ". "
            if item["type"] == "clueTower":
                print(item["text"])
                answer = input("What is your answer?").lower().strip()
                if answer == item["answer"]:
                    game_state["solved_riddles"].append(item_name)
                    output = "The door is unlocked "
                    next_room = library  # Update the next room
                    play_room(next_room)  # Play the next room
                else:
                    print("Incorrect answer")
            elif item["type"] == "clueliving_room":
                print(item["text"])
                answer = finalInputErrors(
                    "What is your answer? Please, write a number between 1 and 20: ",
                    1,
                    20,
                )
                if answer == 14:
                    item_found = item["target"]
                    print(item_found)
                    game_state["solved_riddles"].append(item_found)
                    output += "The door is unlocked "
                else:
                    print("Incorrect answer")
            elif item["type"] == "library_clue":
                print(item["text"])
                answer = input("What is your answer?")
                if answer == item["answerA"]:
                    item_found = "library_riddleA"
                    game_state["solved_riddles"].append(item_found)
                    print("The blue door makes a noise")
                    print("Would you like to examine the blue door?")
                    if input("Enter 'yes' or 'no'").strip().lower() == "yes":
                        next_room = living_room
                        play_room(next_room)
                elif answer == item["answerB"]:
                    item_found = "library_riddleB"
                    game_state["solved_riddles"].append(item_found)
                    print("The red door makes a noise")
                    print("Would you like to examine the red door?")
                    if input("Enter 'yes' or 'no'").strip().lower() == "yes":
                        print(next_room)
                        next_room = dungeon
                        play_room(next_room)
                elif answer == item["answerC"]:
                    item_found = "library_riddleC"
                    game_state["solved_riddles"].append(item_found)
                    print("The yellow door makes a noise")
                    if input("Enter 'yes' or 'no'").strip().lower() == "yes":
                        next_room = kitchen
                        play_room(next_room)
                else:
                    print("Incorrect answer")
            elif item["type"] == "door":
                solved_riddles = False
                for key in game_state["solved_riddles"]:
                    if isinstance(key, dict) and key.get("target") == item:
                        solved_riddles = True
                if solved_riddles:
                    output += "The door is unlocked."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "The door is locked."
            elif item["type"] == "trap":
                output += "You've eaten the cake"
            else:
                output += "There isn't anything interesting about it."
            print(output)
            break

    if output is None:
        print("The item you requested is not found in the current room.")
    if item_name == "cake":
        print("You feel dizzy and find yourself back at the tower")
        play_room(tower)
    elif (
        next_room
        and input("Do you want to go to the next room? Enter 'yes' or 'no'")
        .strip()
        .lower()
        == "yes"
    ):
        play_room(next_room)
    else:
        play_room(current_room)

# Game play starts here
start_game()