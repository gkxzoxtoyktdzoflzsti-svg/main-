"""
A simple number guessing game for the command line.

The player must guess a random number between 1 and 100
within a limited number of attempts. Invalid inputs are
handled gracefully, and the player can choose to play
multiple rounds.
"""

from __future__ import annotations

import random
from typing import Iterable


LOWER_BOUND = 1
UPPER_BOUND = 100
MAX_ATTEMPTS = 7


def prompt_for_guess(prompt: str) -> str:
    """Retrieve raw input from the player.

    Extracted for easier testing and reuse.
    """

    return input(prompt)


def get_guess_input() -> int | None:
    """Prompt the user for a guess.

    Returns the guess as an integer if it is valid, or ``None``
    if the player wants to quit the current round.
    """

    while True:
        raw = prompt_for_guess(
            f"Enter a number between {LOWER_BOUND} and {UPPER_BOUND} (or 'q' to quit): "
        ).strip().lower()

        if raw in {"q", "quit", "exit"}:
            return None

        try:
            guess = int(raw)
        except ValueError:
            print("That is not a valid number. Please try again.\n")
            continue

        if LOWER_BOUND <= guess <= UPPER_BOUND:
            return guess

        print(
            f"Your guess must be between {LOWER_BOUND} and {UPPER_BOUND}. Please try again.\n"
        )


def evaluate_guess(secret: int, guess: int) -> str:
    """Return feedback for a guess compared to the secret number."""

    if guess < secret:
        return "Too low!"
    if guess > secret:
        return "Too high!"
    return "Correct!"


def play_round(rng: Iterable[int] | None = None) -> bool:
    """Play a single round of the guessing game.

    Returns ``True`` if the player wants to play another round,
    ``False`` otherwise. The ``rng`` parameter exists only to
    allow deterministic testing by passing a custom iterable of
    numbers; in normal play the game uses :func:`random.randint`.
    """

    if rng is None:
        secret = random.randint(LOWER_BOUND, UPPER_BOUND)
    else:
        try:
            secret = next(iter(rng))
        except StopIteration:
            secret = random.randint(LOWER_BOUND, UPPER_BOUND)

    print("\nA new game has started!")
    print(f"You have {MAX_ATTEMPTS} attempts to guess the secret number between {LOWER_BOUND} and {UPPER_BOUND}.")

    attempts_left = MAX_ATTEMPTS
    while attempts_left > 0:
        print(f"Attempts left: {attempts_left}")
        guess = get_guess_input()
        if guess is None:
            print("You chose to exit the round. Better luck next time!\n")
            break

        feedback = evaluate_guess(secret, guess)
        print(feedback)

        if feedback == "Correct!":
            print("Congratulations, you guessed the number!\n")
            break

        attempts_left -= 1

    else:
        print(f"Out of attempts! The secret number was {secret}.\n")

    play_again = prompt_for_guess("Would you like to play again? (y/n): ").strip().lower()
    return play_again in {"y", "yes"}


def main() -> None:
    """Entry point for the command-line game."""

    print("Welcome to the Number Guessing Game!")

    continue_playing = True
    while continue_playing:
        continue_playing = play_round()

    print("Thanks for playing! Goodbye.")


if __name__ == "__main__":
    main()
