# Juego STOP

This repository contains a simple Flask app for a STOP game.

## Gameplay

1. **Joining**: Open the application in your browser and enter your name to join the game lobby.
2. **Starting a Round**: Any player can press the *Nueva Ronda* button to generate a random letter.
3. **Scoring**: Fill each category with words that start with the selected letter. Every non‑empty answer is worth 10 points.
4. **Stopping**: When players finish a round you can simply refresh or close the page to end your session.

## Running the Application

Install dependencies and start the server:

```bash
pip install -r requirements.txt
python servidor.py
```

The app will be available at `http://localhost:5050/`.

## Running Tests

The project uses `pytest` for tests. After installing dependencies run:

```bash
pytest
```
