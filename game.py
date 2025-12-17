"""
A simple number guessing game for the command line.

The player must guess a random number between 1 and 100
within a limited number of attempts. Invalid inputs are
handled gracefully, and the player can choose to play
multiple rounds.
"""

from __future__ import annotations

import argparse
import random
from typing import Iterable, Sequence


DEFAULT_LOWER_BOUND = 1
DEFAULT_UPPER_BOUND = 100
DEFAULT_MAX_ATTEMPTS = 7


def prompt_for_guess(prompt: str) -> str:
    """Retrieve raw input from the player.

    Extracted for easier testing and reuse.
    """

    return input(prompt)


def get_guess_input(
    lower_bound: int, upper_bound: int, *, input_func=prompt_for_guess
) -> int | None:
    """Prompt the user for a guess.

    Returns the guess as an integer if it is valid, or ``None``
    if the player wants to quit the current round.
    """

    while True:
        raw = input_func(
            f"Enter a number between {lower_bound} and {upper_bound} (or 'q' to quit): "
        ).strip().lower()

        if raw in {"q", "quit", "exit"}:
            return None

        try:
            guess = int(raw)
        except ValueError:
            print("That is not a valid number. Please try again.\n")
            continue

        if lower_bound <= guess <= upper_bound:
            return guess

        print(
            f"Your guess must be between {lower_bound} and {upper_bound}. Please try again.\n"
        )


def evaluate_guess(secret: int, guess: int) -> str:
    """Return feedback for a guess compared to the secret number."""

    if guess < secret:
        return "Too low!"
    if guess > secret:
        return "Too high!"
    return "Correct!"


def play_round(
    *,
    lower_bound: int,
    upper_bound: int,
    max_attempts: int,
    rng: Iterable[int] | None = None,
    secret: int | None = None,
) -> bool:
    """Play a single round of the guessing game.

    Returns ``True`` if the player wants to play another round,
    ``False`` otherwise. The ``rng`` parameter exists only to
    allow deterministic testing by passing a custom iterable of
    numbers; in normal play the game uses :func:`random.randint`.
    """

    if secret is None:
        if rng is None:
            secret_value = random.randint(lower_bound, upper_bound)
        else:
            try:
                secret_value = next(iter(rng))
            except StopIteration:
                secret_value = random.randint(lower_bound, upper_bound)
    else:
        secret_value = secret

    print("\nA new game has started!")
    print(
        "You have "
        f"{max_attempts} attempts to guess the secret number between {lower_bound} and {upper_bound}."
    )

    attempts_left = max_attempts
    while attempts_left > 0:
        print(f"Attempts left: {attempts_left}")
        guess = get_guess_input(lower_bound, upper_bound)
        if guess is None:
            print("You chose to exit the round. Better luck next time!\n")
            break

        feedback = evaluate_guess(secret_value, guess)
        print(feedback)

        if feedback == "Correct!":
            print("Congratulations, you guessed the number!\n")
            break

        attempts_left -= 1

    else:
        print(f"Out of attempts! The secret number was {secret_value}.\n")

    play_again = prompt_for_guess("Would you like to play again? (y/n): ").strip().lower()
    return play_again in {"y", "yes"}


def play_scripted_round(
    guesses: Sequence[int],
    *,
    lower_bound: int,
    upper_bound: int,
    max_attempts: int,
    secret: int | None = None,
) -> None:
    """Play a non-interactive round using predefined guesses."""

    secret_value = secret if secret is not None else random.randint(lower_bound, upper_bound)

    print("\nScripted demo round")
    print(
        f"Secret number is between {lower_bound} and {upper_bound} with up to {max_attempts} attempts."
    )

    attempts_left = max_attempts
    for guess in guesses:
        if attempts_left <= 0:
            break

        if not lower_bound <= guess <= upper_bound:
            print(
                f"Guess {guess} is outside the allowed range. It does not count against your attempts.\n"
            )
            continue

        print(f"Attempt {max_attempts - attempts_left + 1}: {guess}")
        feedback = evaluate_guess(secret_value, guess)
        print(feedback)

        if feedback == "Correct!":
            print("Congratulations, the scripted guesses found the number!\n")
            return

        attempts_left -= 1

    if attempts_left <= 0:
        print(f"Out of attempts! The secret number was {secret_value}.\n")
    else:
        print(
            f"Scripted guesses finished with {attempts_left} attempts remaining. The secret number was {secret_value}.\n"
        )


def main() -> None:
    """Entry point for the command-line game."""

    parser = argparse.ArgumentParser(description="Play a number guessing game.")
    parser.add_argument(
        "--lower",
        type=int,
        default=DEFAULT_LOWER_BOUND,
        help="Lower bound for the secret number (inclusive).",
    )
    parser.add_argument(
        "--upper",
        type=int,
        default=DEFAULT_UPPER_BOUND,
        help="Upper bound for the secret number (inclusive).",
    )
    parser.add_argument(
        "--attempts",
        type=int,
        default=DEFAULT_MAX_ATTEMPTS,
        help="Maximum number of attempts per round.",
    )
    parser.add_argument(
        "--secret",
        type=int,
        help="Optional fixed secret number (useful for demos).",
    )
    parser.add_argument(
        "--guesses",
        type=str,
        help="Comma-separated list of guesses to run a scripted, non-interactive round.",
    )

    args = parser.parse_args()

    if args.lower >= args.upper:
        raise SystemExit("The lower bound must be less than the upper bound.")
    if args.attempts <= 0:
        raise SystemExit("Attempts must be a positive integer.")
    if args.secret is not None and not (args.lower <= args.secret <= args.upper):
        raise SystemExit("Secret must be within the provided bounds.")

    if args.guesses:
        guesses = [int(value.strip()) for value in args.guesses.split(",") if value.strip()]
        if not guesses:
            raise SystemExit("Provide at least one guess when using --guesses.")
        play_scripted_round(
            guesses,
            lower_bound=args.lower,
            upper_bound=args.upper,
            max_attempts=args.attempts,
            secret=args.secret,
        )
        return

    print("Welcome to the Number Guessing Game!")

    continue_playing = True
    while continue_playing:
        continue_playing = play_round(
            lower_bound=args.lower,
            upper_bound=args.upper,
            max_attempts=args.attempts,
            secret=args.secret,
        )

    print("Thanks for playing! Goodbye.")


if __name__ == "__main__":
    main()
