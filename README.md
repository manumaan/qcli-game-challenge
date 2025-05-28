# Movie Hangman Game

A Pygame-based hangman game where players guess movie titles to save a kangaroo from a noose. I created this game using Q CLI. 

## Game Description

In this game, players must guess the letters of a movie title within 2 minutes. If you guess the title correctly, you save the kangaroo. If time runs out, the kangaroo remains sad on the noose. We used to play a flash version of this game while I was studying in College of Engineering, Trivandrum. 

The game features:
- 100+ popular movie titles to guess
- A worried kangaroo character that needs saving
- Visual feedback with happy/sad kangaroo based on outcome
- Retro-style blinking text for game controls
- A 2-minute countdown timer

## Installation

### Prerequisites
- Python 3.13 or compatible version
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd qcli-game-challenge
```

### Step 2: Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
```

Activate the virtual environment:
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Game

### Using the Run Script
The easiest way to run the game is to use the provided shell script:

```bash
./run_game.sh
```

### Running Directly with Python
```bash
python movie_hangman.py
```

## How to Play

1. When the game starts, you'll see a movie title represented by empty boxes (one box per letter)
2. Type letters (a-z) on your keyboard to guess the letters in the title
3. Correct guesses will reveal the letter in all its positions
4. You have 2 minutes to guess the entire movie title
5. If you guess the title correctly, the kangaroo will be happy and saved
6. If time runs out, the kangaroo will be sad

### Game Controls
- **Letter keys (a-z)**: Guess letters
- **R key**: Restart the game after it ends
- **Q key**: Quit the game

## Project Structure

- `movie_hangman.py`: Main game file
- `requirements.txt`: List of Python dependencies
- `run_game.sh`: Shell script to run the game
- Image files:
  - `happy_kangaroo.png`
  - `sad_kangaroo.png`
  - `worried_kangaroo.png`
  - `noose.png`

## Troubleshooting

If you encounter any issues:

1. **Images not loading**: Make sure all image files are in the same directory as the game script
2. **Pygame installation issues**: Try installing Pygame with `pip install pygame==2.6.1`
3. **Display problems**: Ensure your system supports the game's resolution (1000x700 pixels)

## Credits

- Game developed using [Pygame](https://www.pygame.org/news)
- Kangaroo character images and game concept created using AI for educational purposes

## License

This project is available for personal and educational use.
