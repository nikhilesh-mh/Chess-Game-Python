Your README looks great and well-structured! Here are a few minor suggestions for finalizing it:

1. **Clarify the "Short Game" and "Full Game" distinction**:  
   Consider briefly explaining what the short game is and how it differs from the full game for better clarity. 
   
2. **Emphasize running the game**:  
   If players need to navigate into the `src` directory, mention it explicitly under **Usage**.

3. **Minor formatting fixes**:  
   Add the section where it mentions the file locations in a clearer format for those who may not notice the "src" directory.

Here's your final README with these minor adjustments:

---

# Chess-Game-Python  
![Version](https://img.shields.io/badge/version-1.0.0-g.svg)

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

- **prettytable**: Used to format the move history neatly in the [`moves_his.py`](src/moves_his.py).
- Inspired by classic chess games.

---

This version should be clear and polished for anyone visiting your project. Let me know if you'd like to adjust anything further!
