# PathwayPaver

Pathway Paver is a puzzle game where the player must guide cars to their destinations by placing road tiles on a grid. The game challenges players to use limited resources (tiles and turns) to solve increasingly complex levels while avoiding obstacles like trees.

This project was created by [onetwothreefourfivesixe](https://github.com/onetwothreefourfivesixe) and [NHere24](https://github.com/NHere24) for the 2025 McLean Hackathon where we won first place.

## Features

- **Multiple Levels:** Progress through predefined levels with unique layouts and challenges.
- **Tile Placement:** Strategically place road tiles to create paths for cars.
- **Turn Limit:** Complete each level within a limited number of turns.
- **Obstacles:** Avoid trees (dark green tiles) that block road placement.
- **Dynamic Cars:** Cars move in order, and their direction is indicated by a blue windshield.
- **Destination Houses:** Cars must reach their color-matched houses (represented as houses on the grid).
- **Level Selection:** Replay completed levels or select unlocked levels from the level selection screen.
- **Help Screen:** Learn how to play with an accessible help screen.

## Win/Lose Conditions

- **Win:** Guide all cars to their destinations.
- **Lose:** Cars collide, a car is missing, or you run out of turns.

## How to Play

**Objective:**  
Guide all cars to their destinations (houses with matching colors).

**Controls:**
- **Mouse:** Place or remove road tiles by clicking on the grid.
- **Spacebar:** Start the cars' movement once the path is ready.

**Rules:**
- Cars follow the shortest path to their destination.
- You have a limited number of tiles and turns.
- Avoid obstacles like trees (dark green tiles).
- Cars cannot occupy the same tile at the same time.

**Win Condition:**  
All cars must reach their destinations without collisions or missing cars.

**Lose Condition:**
- Cars collide or a car is missing from the grid.
- You run out of turns.
- A car is not connected to its house when prompted to move.

## Installation and Setup

### Requirements

- Python 3.x
- pygame library

### Install pygame

Run the following command in your terminal or command prompt:

```bash
pip install pygame
```

### Run the Game

Execute the `PathwayPaver.py` file.

---

## Known Issues and Future Improvements

- **Additional Cars and Houses**: Add more cars and houses per level
- **Level Editor**: Add a feature to create custom levels.
- **Enhanced Graphics**: Improve visuals for cars, houses, and obstacles.
- **Sound Effects**: Add audio feedback for actions and events.

---

## Credits

- **Developers**: [onetwothreefourfivesixe](https://github.com/onetwothreefourfivesixe) and [NHere24](https://github.com/NHere24) 
- **Event**: Created for the 2025 McLean Hackathon  
- **Libraries Used**: `pygame`

---

## License

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute the code.

---

**Enjoy playing Pathway Paver! 🚗🏠**
