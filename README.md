# Target Aim Trainer

A simple interactive aim-training game built using **Python and Pygame**. The game challenges the player to click targets as quickly and accurately as possible while they appear at random positions and gradually shrink over time.

The project demonstrates real-time game rendering, event handling, collision detection, scoring, accuracy tracking, difficulty levels, game states, and sound feedback.

---

## Features

- 🎯 Randomly positioned targets
- 📉 Targets gradually shrink while active
- 🖱️ Accurate click-based collision detection
- ✅ Hit detection and scoring
- ❌ Miss detection, including timed-out targets
- 📊 Live score and accuracy tracking
- ⏱️ Countdown round timer
- 🏁 Game Over screen with final results
- 🔄 Replay functionality
- 🎚️ Easy, Medium, and Hard difficulty levels
- 🔊 Sound feedback for hits, misses, and round completion
- 🎮 Interactive Pygame-based graphical interface

---

## How the Game Works

A target appears at a random location on the screen and gradually becomes smaller as time passes.

- Clicking directly on the target registers a **hit**.
- Clicking outside the target registers a **miss**.
- If the target shrinks completely before being clicked, it is also counted as a **miss**.
- A new target appears after each successful hit or missed target.
- The player's score and accuracy are updated throughout the round.
- When the round timer reaches zero, the final score and accuracy are displayed.
- The player can then select a difficulty and replay or exit the game.

---

## Difficulty Levels

The game provides three difficulty levels:

| Difficulty | Description |
|---|---|
| Easy | Longer target lifespan and easier targets |
| Medium | Balanced target speed and lifespan |
| Hard | Shorter target lifespan and more challenging gameplay |

---

## Technologies Used

- **Python 3**
- **Pygame**
- Object-Oriented Programming
- Real-time event handling
- 2D graphics rendering
- Collision detection
- Game state management

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd target-aim-trainer
```

### 2. Install the required dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the game

```bash
python main.py
```

---

## Project Structure

```text
target-aim-trainer/
├── main.py
├── requirements.txt
├── README.md
└── game/
    ├── game_engine.py
    └── target.py
```

### File Description

**`main.py`**  
Entry point of the application. Initializes and runs the game.

**`game/game_engine.py`**  
Contains the main game logic, including game states, scoring, accuracy, difficulty selection, input handling, rendering, sound effects, and the game loop.

**`game/target.py`**  
Handles the target's properties, position, size, lifespan, and behavior.

**`requirements.txt`**  
Contains the Python dependencies required to run the project.

---

## Running the Project

After installing the dependencies, start the game using:

```bash
python main.py
```

Follow the on-screen instructions to select a difficulty and begin playing.

---

## Project Status

**Completed and working successfully.**

The project has been tested and the required gameplay features, difficulty levels, scoring, accuracy tracking, Game Over screen, replay functionality, collision detection, and sound feedback are implemented.

---
