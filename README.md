# Simple Number Guessing Game

This repository contains a small command-line game written in Python. The goal is to guess the secret number between 1 and 100 within seven attempts. After each guess, the game tells you whether you are too high or too low, and you can quit a round at any time.

## How to play

1. Ensure Python 3.10 or later is installed.
2. Run the game:

   ```bash
   python game.py
   ```
3. Follow the on-screen prompts to enter guesses or type `q` to leave the round. After each round, choose whether to play again.

You can also run a non-interactive demo round to see how the game works without typing input:

```bash
python game.py --guesses 20,50,75,63,68 --secret 68
```

### Command-line options

- `--lower` / `--upper`: Set the bounds for the secret number (defaults: 1–100).
- `--attempts`: Maximum number of attempts per round (default: 7).
- `--secret`: Provide a fixed secret number—handy for demonstrations or practice.
- `--guesses`: Comma-separated guesses for a scripted demo round (disables interactive prompts).

## Notes

- Input validation helps prevent crashes from invalid entries.
- The code is organized into small functions to make the flow easy to follow and adapt.
