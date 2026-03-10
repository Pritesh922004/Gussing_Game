import random


def choose_difficulty():
    difficulties = {
        "easy": {"attempts": 10, "range": 50},
        "medium": {"attempts": 7, "range": 100},
        "hard": {"attempts": 5, "range": 200},
    }

    print("\nChoose a difficulty: easy, medium, or hard")

    while True:
        choice = input("Enter difficulty: ").strip().lower()
        if choice in difficulties:
            return choice, difficulties[choice]
        print("Invalid choice. Please type easy, medium, or hard.")


def get_valid_guess(lower_bound, upper_bound):
    while True:
        guess = input(f"Enter your guess ({lower_bound}-{upper_bound}): ").strip()

        if not guess.isdigit():
            print("Please enter a valid whole number.")
            continue

        guess = int(guess)
        if lower_bound <= guess <= upper_bound:
            return guess

        print(f"Your guess must be between {lower_bound} and {upper_bound}.")


def play_round():
    difficulty_name, settings = choose_difficulty()
    max_attempts = settings["attempts"]
    upper_bound = settings["range"]
    secret_number = random.randint(1, upper_bound)

    print(f"\nYou selected {difficulty_name.title()} mode.")
    print(f"I picked a number between 1 and {upper_bound}.")
    print(f"You have {max_attempts} attempts to guess it.\n")

    for attempt in range(1, max_attempts + 1):
        guess = get_valid_guess(1, upper_bound)

        if guess == secret_number:
            print(f"\nCorrect! You guessed the number in {attempt} attempt(s).")
            return

        remaining_attempts = max_attempts - attempt

        if guess < secret_number:
            print("Too low!")
        else:
            print("Too high!")

        if remaining_attempts > 0:
            hint = "You are very close!" if abs(guess - secret_number) <= 5 else "Try again."
            print(f"{hint} Attempts left: {remaining_attempts}\n")
        else:
            print(f"\nGame over! The number was {secret_number}.")


def ask_to_play_again():
    while True:
        answer = input("\nDo you want to play again? (y/n): ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter y or n.")


def main():
    print("Welcome to the Number Guessing Game!")
    print("Try to guess the secret number in as few attempts as possible.")

    while True:
        play_round()
        if not ask_to_play_again():
            print("\nThanks for playing. Goodbye!")
            break


if __name__ == "__main__":
    main()