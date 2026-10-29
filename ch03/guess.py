# guess.py - guess the number, with a play-again loop and stats
import random

games = 0
total_guesses = 0
best = None

while True:
    secret = random.randint(1, 100)
    guesses = 0
    print("\nI'm thinking of a number from 1 to 100.")
    while True:
        text = input("Your guess: ")
        if not text.isdigit():
            print("Please type a whole number.")
            continue
        guess = int(text)
        guesses += 1
        if guess < secret:
            print("Too low.")
        elif guess > secret:
            print("Too high.")
        else:
            print(f"Correct! {guesses} guesses.")
            break
    games += 1
    total_guesses += guesses
    if best is None or guesses < best:
        best = guesses
        print("New best score!")
    again = input("Play again? (y/n) ").lower()
    if again != "y":
        break

print(f"\nGames: {games}  Average: {total_guesses / games:.1f}  Best: {best}")
