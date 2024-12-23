---

# Chess-Game-Python  
![Version](https://img.shields.io/badge/version-1.0.0-g.svg)
![License](https://img.shields.io/badge/license-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/NikMehraDev/Chess-Game-Python)
![Languages](https://img.shields.io/github/languages/top/NikMehraDev/Chess-Game-Python)
![Python](https://img.shields.io/badge/python-3.6+-blue)
![Issues](https://img.shields.io/github/issues/NikMehraDev/Chess-Game-Python)
![Dependencies](https://img.shields.io/badge/dependencies-up--to--date-brightgreen)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen)
![Build Status](https://img.shields.io/github/actions/workflow/status/NikMehraDev/Chess-Game-Python/chessboard_.py)


![GitHub stars](https://img.shields.io/github/stars/NikMehraDev/Chess-Game-Python)
![Repo Size](https://img.shields.io/github/repo-size/NikMehraDev/Chess-Game-Python)

A Python-based chess game designed with a command-line interface (CLI) for clear visual presentation. This project utilizes **prettytable** for formatting the move history, avoiding the use of large libraries. It provides a straightforward two-player chess experience with efficient and readable board rendering in the terminal.

---

## Features  
- **Two-player game**: Classic chess with no AI—played between two players.  
- **Board Rendering**: Efficient and clear board rendering using basic text formatting.  
- **Move History**: Track and display the history of moves using the `prettytable` library.  
- **Simple and Lightweight**: No heavy dependencies; designed to work with only necessary packages.  

For more information, check this [FEATURES.md](FEATURES.md).

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NikMehraDev/Chess-Game-Python.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Chess-Game-Python
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   - The only dependency for this project is **`prettytable`**, which is used for displaying the move history neatly.
   - Ensure you are using Python 3.6 or later.
   - It's recommended to use a virtual environment for managing dependencies.

---

## Usage

1. **For Short Game Example.**
   - ***Run the short game*** (found in the `src` directory):
      ```bash
      python src/chessboard_.py
      ```

   - ***Playing the game***:
      - The game will prompt players with the message: "Mission: Find a move for a checkmate." You just have to enter the moves "g8" and then "f7".
      - The game will end once the checkmate is executed.

2. **For Full Game Example.**
   - ***Run the full game*** (found in the `src` directory):
      ```bash
      python src/chessboard_usage.py
      ```
   - ***Playing the game***:
      - The game will prompt players to enter moves in standard chess notation (e.g., "e2" and then "e4").
      - The board will be displayed after each move.
      - Players can see the history of their moves formatted in a table.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **prettytable**: Used to format the move history neatly in the [`moves_his.py`](src/moves_his.txt) file.
- Inspired by classic chess games.

---
