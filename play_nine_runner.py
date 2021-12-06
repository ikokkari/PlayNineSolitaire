from random import Random
import play_nine_player as pnp

# SETTINGS THAT STUDENTS CAN CHANGE DURING THE DEVELOPMENT OF THEIR AGENT START HERE:
# -----------------------------------------------------------------------------------

# How many hands are played in total to compute the final score.
TOTAL_HANDS = 1

# Whether the hand actions are printed out, instead of just the final score.
VERBOSE = True

# The seed value for the rng used to draw cards.
SEED = 4242

# ------------------------------------------------------------------------
# END OF SETTINGS FOR STUDENTS: DO NOT MODIFY ANYTHING BELOW THIS LINE!!!!

# The minimum and maximum number of columns for playing one hand.
MIN_COLUMNS = 4
MAX_COLUMNS = 4

# The frequencies of cards in the infinite deck.
DECK_FREQ = [-5, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12]

# The frequencies of cards as the top card of the kitty.
KITTY_FREQ = [5, 0, 1, 2, 3, 4, 5, 6, 6, 7, 7, 8, 8, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12]


# Compute the score for the finished hand.

def score_hand(top_cards, bottom_cards):
    total = 0
    pos_match = dict()
    for (t, b) in zip(top_cards, bottom_cards):
        if t != b:
            total += (t + b)
        else:
            pos_match[t] = pos_match.get(t, 0) + 1
            total += -10 if t == -5 else 0
    for value in pos_match:
        count = pos_match[value]
        mul = -5 if value == -5 else -5
        total += mul * count if count > 1 else 0
    return total


# Some examples of hand scoring.

assert score_hand([4, 3, 12, 6], [4, 1, 12, 6]) == 4
assert score_hand([4, 4, 2, 10], [4, 4, -5, 9]) == 6
assert score_hand([5, 2, 12, 4], [8, 2, 3, 1]) == 33
assert score_hand([1, -5, 10, 2], [6, -5, 10, 3]) == 2
assert score_hand([6, 2, 6, 1], [6, 9, 6, 3]) == 5
assert score_hand([2, -5, -5, 4], [10, -5, -5, 5]) == -9


# Create a masked version of the cards in the hand, based on what has been revealed.

def conceal_cards(top_cards, bottom_cards, top_revealed, bottom_revealed):
    top_row = [card if reveal else '*' for (card, reveal) in zip(top_cards, top_revealed)]
    bottom_row = [card if reveal else '*' for (card, reveal) in zip(bottom_cards, bottom_revealed)]
    return top_row, bottom_row


# Print out the current state of the hand.

def output_cards(top_cards, bottom_cards, top_revealed, bottom_revealed):
    top_row, bottom_row = conceal_cards(top_cards, bottom_cards, top_revealed, bottom_revealed)
    top_print = " ".join(f"{str(card):>3}" for card in top_row)
    bottom_print = " ".join(f"{str(card):>3}" for card in bottom_row)
    print(f"Row 0: [{top_print} ]")
    print(f"Row 1: [{bottom_print} ]")


# Play one hand with the given rng, with n cards per row for a given number of draws.

def play_one_hand(rng, columns, draws_left):
    top_cards = [rng.choice(DECK_FREQ) for _ in range(columns)]
    bottom_cards = [rng.choice(DECK_FREQ) for _ in range(columns)]
    top_revealed = [False for _ in range(columns)]
    bottom_revealed = [False for _ in range(columns)]
    top_revealed[rng.choice(range(columns))] = True
    bottom_revealed[rng.choice(range(columns))] = True

    # Keep playing as long as there are draws left and some cards are still face down.
    while draws_left > 0 and (False in top_revealed or False in bottom_revealed):
        kitty_card = rng.choice(KITTY_FREQ)
        if VERBOSE:
            draw_string = f"are {draws_left} draws" if draws_left > 1 else "is one draw"
            print(f"There {draw_string} remaining. Kitty card is {kitty_card}.")
            output_cards(top_cards, bottom_cards, top_revealed, bottom_revealed)
        top_concealed, bottom_concealed = conceal_cards(top_cards, bottom_cards, top_revealed, bottom_revealed)
        action = pnp.choose_drawing_action(top_concealed, bottom_concealed, draws_left, kitty_card)
        assert len(action) == 1 and action in "kKdR", f"Illegal action {action}"
        draws_left -= 1
        current_card = kitty_card if action in "kK" else rng.choice(DECK_FREQ)
        if VERBOSE:
            print(f"You are holding a {current_card}.")
        (action, row, column) = pnp.choose_replacement_action(top_concealed, bottom_concealed, draws_left, current_card)
        assert row in range(2), f"Illegal row {row}"
        assert column in range(columns), f"Illegal column {column}"
        if action in "tT":  # You can only turn over cards that were face down.
            if row == 0:
                assert not top_revealed[column], f"Card at {row}, {column} already face up"
            else:
                assert not bottom_revealed[column], f"Card at {row}, {column} already face up"
        if action in "rR":  # Any card on the board can be replaced, be it either face up or face down.
            if row == 0:
                top_cards[column] = current_card
            else:
                bottom_cards[column] = current_card
        if row == 0:  # Either way, that card is now revealed.
            top_revealed[column] = True
        else:
            bottom_revealed[column] = True

    top_revealed = [True for _ in range(columns)]
    bottom_revealed = [True for _ in range(columns)]
    output_cards(top_cards, bottom_cards, top_revealed, bottom_revealed)
    hand_score = score_hand(top_cards, bottom_cards)
    if VERBOSE:
        print(f"The score for the completed hand is {hand_score}.")
    return hand_score


# Play the entire game of all the hands.

def play_all_hands():
    rng, total_score = Random(SEED), 0
    for hand in range(TOTAL_HANDS):
        columns = rng.randint(MIN_COLUMNS, MAX_COLUMNS)
        draws = 2 * columns + rng.randint(1, 3)
        if VERBOSE:
            print(f"\nStarting hand #{hand + 1} with {columns} columns on board.")
        try:
            current_score = play_one_hand(rng, columns, draws)
        except Exception as e:
            print(f"Crash with error: {e}")
            print("Game play terminated.")
            return None
        total_score += current_score
    return total_score


if __name__ == "__main__":
    print("Play Nine Solitaire runner, version December 6, 2021, Ilkka Kokkarinen.")
    author_name, author_id = pnp.get_author_info()
    final_score = play_all_hands()
    print(f"{author_name}, {author_id}: {final_score}")
