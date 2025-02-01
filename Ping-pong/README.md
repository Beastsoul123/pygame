# Ping-Pong Game

This is a simple **Ping-Pong** game created using **Pygame**. The game allows two players to control paddles and hit a bouncing ball. The goal is to score points by making the opponent miss the ball.

## Features

- **Two-Player Mode:** One player controls the right paddle, and the other controls the left paddle.
- **Ball Physics:** The ball moves at a constant speed and bounces off the walls and paddles.
- **Scoring System:** The score increases when the opponent fails to return the ball.
- **Background Music:** A looping background sound plays during the game.

![image](https://github.com/user-attachments/assets/a1a4267b-1305-4fdd-b396-c8fdf4cf18a1)


## Installation

Ensure you have Python and Pygame installed. If you haven't installed Pygame, run:
```sh
pip install pygame
```

## Running the Game
Execute the script using:
```sh
python game.py
```

## Controls
- **Player 1 (Right Paddle):**
  - `UP ARROW` → Move Up
  - `DOWN ARROW` → Move Down

- **Player 2 (Left Paddle):**
  - `W` → Move Up
  - `S` → Move Down

## Game Mechanics
- The ball bounces off the top and bottom walls.
- When the ball collides with a paddle, it changes direction.
- If a player misses the ball, the opponent gains a point, and the ball resets to the center.

## File Structure
```
PingPongGame/
│-- assets/
│   ├── music.mp3  # Background sound
│-- game.py  # Main game script
│-- README.md  # Game documentation
│-- Pixeltype.ttf  # Game font
```

## Future Enhancements
- Implement AI-controlled opponent mode.
- Add more sound effects for ball collisions.
- Introduce difficulty levels with increasing ball speed.
- Improve visuals with enhanced animations.

## License
This project is open-source and available for modification and distribution.

Enjoy playing **Ping-Pong**! 🏓

