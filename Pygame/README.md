# Monster Runner

Monster Runner is a simple side-scrolling endless runner game built using **Pygame**. The player must jump over obstacles to survive as long as possible, accumulating a score based on time survived.

## Features

- **Player Character**
  - Animates between running frames
  - Can jump when pressing the spacebar
  - Falls back to the ground with gravity
  - Collision detection with obstacles

- **Obstacles**
  - Randomly generated (either snails or flies)
  - Moves from right to left
  - Disappears when off-screen

- **Game Mechanics**
  - Background music loops continuously
  - Jump sound effect when the player jumps
  - Displays score based on survival time
  - Game over screen with final score displayed
  - Restart game by pressing spacebar

![Screenshot 2025-02-01 113014](https://github.com/user-attachments/assets/7bd3b787-9cac-4635-8c63-9bb9195e0ee6)

![Screenshot 2025-02-01 113054](https://github.com/user-attachments/assets/90f8ea82-f010-418c-9981-d3afbe054a56)

## Installation

Ensure you have Python installed, then install Pygame if you haven't already:
```sh
pip install pygame
```

## Running the Game
Run the script using:
```sh
python game.py
```

## Controls
- **Spacebar** - Jump
- **Close Button** - Quit the game

## File Structure
```
PixelRunner/
│-- graphics/
│   │-- player/
│   │   ├── player_walk_1.png
│   │   ├── player_walk_2.png
│   │   ├── jump.png
│   │   └── player_stand.png
│   │-- snail/
│   │   ├── snail1.png
│   │   ├── snail2.png
│   │-- fly/
│   │   ├── fly1.png
│   │   ├── fly2.png
│   ├── Sky.png
│   ├── ground.png
│-- audio/
│   ├── jump.mp3
│   ├── music.wav
│-- font/
│   ├── Pixeltype.ttf
│-- game.py  # Main game script
│-- README.md  # Game documentation
```

## Future Enhancements
- Add difficulty levels
- Implement power-ups for the player
- Add more diverse obstacles
- Improve animations and UI elements

## License
This project is open-source and available for modification and distribution.

Enjoy playing **Monster Runner**! 🚀


