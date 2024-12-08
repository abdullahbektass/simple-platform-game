# Python Platformer Game

This is a simple platformer game written in Python using the `pgzrun` module. The player controls a hero who must avoid dangers by jumping over them while the background scrolls continuously. The game features animations, background music, and sound effects.

## Features
- **Hero Controls**: Move left, right, or jump to avoid dangers.
- **Dangers**: Enemies spawn randomly and move toward the hero.
- **Scrolling Background**: Provides a dynamic and immersive game environment.
- **Sound Effects**: Background music and jump sounds.
- **Game States**: Main menu, playing, and game over screens.

## Prerequisites
- Python 3.7 or later
- `pgzrun` (part of the `pygame-zero` package)
- `pygame` library

## Installation

1. Clone the repository or download the game files:
   ```bash
   git clone [<repository_url>](https://github.com/abdullahbektass/simple-platform-game)
   cd simple-platform-game
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the required asset folders and files are present:
   - **Images**:
     - `assets/images/empty_bg.png`
     - `assets/images/bg_playing.png`
     - `assets/images/hero_sheet.png`
     - `assets/images/danger_sheet.png`
   - **Sounds**:
     - `assets/sounds/bg.wav`
     - `assets/sounds/jump.wav`

## How to Run

1. Navigate to the project directory:
   ```bash
   cd simple-platform-game
   ```

2. Run the game using the following command:
   ```bash
   python game.py
   ```

## Controls
- **SPACE**: Jump
- **Arrow Keys (LEFT/RIGHT)**: Move left or right
- **1/SPACE in Menu**: Start the game
- **2 in Menu**: Toggle music on/off
- **3 in Menu**: Exit the game
- **SPACE in Game Over Screen**: Restart the game

## Game States
- **Menu**: The player can start the game or toggle music.
- **Playing**: Control the hero to avoid dangers and score points.
- **Game Over**: Displays the final score and allows restarting.

## Assets
All assets (images and sounds) are located in the `assets` folder. Ensure that these files are in the correct directory structure as specified.

## Troubleshooting
- If you encounter `No module named 'pgzrun'`, ensure that `pygame-zero` is correctly installed.
- Ensure all asset files are in the specified directories.
- If the music or sound effects do not play, verify the file paths and formats.

## License
This project is released under the [MIT License](LICENSE).

---

Enjoy the game!

