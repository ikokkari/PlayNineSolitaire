# An example player agent for the

# Returns a tuple of two strings, the name and the student ID of the author.

def get_author_info():
    return "Ilkka Kokkarinen", "123456789"


# Choose the drawing action for the current draw.

def choose_drawing_action(top_concealed, bottom_concealed, draws, kitty_card):
    action = "xxx"
    while len(action) != 1 or action not in "kdKD":
        action = input("Will you take the (k)itty card or (d)raw from deck? ")
    return action


# Choose the replacement action for the current card. The return value of this function
# must be a triple of the form (action, row, column) where
# - action is one of the characters "rRtT", "r" for replace and "t" for turn over
# - row is the row number of the card subject to chosen action
# - column is the column number of the card subject to chosen action

def choose_replacement_action(top_concealed, bottom_concealed, draws, current_card):
    action = "xxx"
    while len(action) != 1 or action not in "rRtT":
        action = input(f"Will you (r)eplace or (t)urn over a board card? ")
    action_verb = "replace" if action in "rR" else "turn over"
    row = int(input(f"Enter row number of card to {action_verb}: "))
    column = int(input(f"Enter column number of card to {action_verb}: "))
    return action, row, column
