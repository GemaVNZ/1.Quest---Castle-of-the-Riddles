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