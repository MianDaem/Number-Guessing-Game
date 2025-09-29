# number_guess_advanced.py
import random
import math
import sys

def choose_difficulty():
    print("Choose difficulty: (E)asy (M)edium (H)ard")
    choice = input(">").lower().strip()
    if choice.startswith('e'):
        return 1, 20   # 1..20, 20 tries? (we'll compute tries dynamically)
    if choice.startswith('m'):
        return 1, 100  # 1..100
    return 1, 1000     # Hard: 1..1000

def max_tries_for_range(max_value):
    # sensible limit based on binary search (ceil(log2(range))) * 1.5 to give some leniency
    return max(3, math.ceil(math.log2(max_value)) * 1)

def get_int(prompt, low=None, high=None):
    while True:
        val = input(prompt).strip()
        if val.lower() in ('q','quit','exit'):
            print("Exiting game. Bye!")
            sys.exit(0)
        if val.lstrip('-').isdigit():
            iv = int(val)
            if (low is None or iv >= low) and (high is None or iv <= high):
                return iv
            else:
                rng = ""
                if low is not None and high is not None:
                    rng = f" between {low} and {high}"
                elif low is not None:
                    rng = f" >= {low}"
                elif high is not None:
                    rng = f" <= {high}"
                print(f"Please enter an integer{rng}.")
        else:
            print("Please enter a valid integer (or type 'q' to quit).")

def play_round():
    low, high = choose_difficulty()
    secret = random.randint(low, high)
    max_tries = max_tries_for_range(high - low + 1)

    print(f"\nI'm thinking of a number between {low} and {high}.")
    print(f"You have {max_tries} guesses. Type 'quit' to exit anytime.")
    tries = 0

    while tries < max_tries:
        guess = get_int(f"Guess #{tries+1}: ", low, high)
        tries += 1

        if guess == secret:
            score = max(0, (max_tries - tries + 1)) * 10
            print(f"Nice! You got it in {tries} tries. Score: {score}")
            return score
        elif guess < secret:
            hint = "higher"
            diff = secret - guess
        else:
            hint = "lower"
            diff = guess - secret

        # give a helpful hint about closeness
        if diff <= max(1, (high - low) // 20):
            closeness = "very close"
        elif diff <= max(2, (high - low) // 10):
            closeness = "close"
        else:
            closeness = "far"

        remaining = max_tries - tries
        print(f"Nope — try {hint}. You're {closeness}. {remaining} guesses left.")

    print(f"Out of guesses! The number was {secret}.")
    return 0

def main():
    print("=== Number Guessing Game ===")
    total_score = 0
    rounds = 0
    while True:
        score = play_round()
        total_score += score
        rounds += 1

        again = input("\nPlay again? (Y/n) ").strip().lower()
        if again and again[0] == 'n':
            break

    print(f"\nThanks for playing! Rounds: {rounds}, Total score: {total_score}")

if __name__ == "__main__":
    main()
