# Python Blackjack Game

A command-line and GUI implementation of the classic Blackjack (21) card game in Python.

## Features

- Play Blackjack against a computer dealer
- Both command-line interface and graphical user interface (Tkinter) available
- Proper card values and scoring rules:
  - Number cards are worth their face value
  - Face cards (J, Q, K) are worth 10
  - Aces can be 1 or 11 (automatically calculated)
- Game options:
  - Play multiple rounds
  - Hit or Stand decisions
  - Automatic win/loss detection
  - Score tracking

## Requirements

- Python 3.x
- tkinter (usually comes with Python standard library)

## How to Run

### Command Line Version

Uncomment the following lines in `main.py`:

```python
# g = Game()
# g.play()
```

Then run:

```bash
python main.py
```

### GUI Version (Default)

The GUI version runs by default. Simply execute:

```bash
python main.py
```

## Game Rules

- The goal is to have a hand value as close to 21 as possible without going over
- The dealer must hit on 16 and stand on 17
- Blackjack (an Ace and a 10-value card) pays 3:2
- If you go over 21, you bust and lose your bet
- If the dealer busts, all remaining players win
- If neither busts, the hand closest to 21 wins

## Controls (GUI Version)

- **Hit**: Draw another card
- **Stand**: Keep your current hand
- **New Game**: Start a new round

## Project Structure

- `Card`: Represents a playing card with suit and rank
- `Deck`: Manages a 52-card deck with shuffle and deal functionality
- `Hand`: Manages a player's or dealer's hand, including score calculation
- `Game`: Implements the main game logic and flow
- `BlackjackGUI`: Provides a graphical user interface for the game

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created by [Your Name]
