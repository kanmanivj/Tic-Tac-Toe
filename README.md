 Tic-Tac-Toe

A  interactive Tic-Tac-Toe game built with Python and Tkinter. Play against a friend or challenge the computer powered by the minimax algorithm.

---

## Features

- Human vs Human — two players on the same machine
- Human vs Computer — face off against the AI
  - Easy— the computer picks random moves
  - Hard — the computer uses minimax and will never lose
- Live scoreboard tracking wins and draws across multiple rounds
- Replay rounds without losing your score
- Change players mid-session — keep scores if same people, reset if new players
- Colourful UI with gold winning cell highlights and colour-coded X / O

---

## Project Structure

```
tictactoe/
│
├── main.py          # Entry point — runs the app
├── ui.py            # All Tkinter screens and widgets
├── logic.py         # Game logic — win checking, AI, minimax
├── constants.py     # Colours, fonts, and WIN_CONDITIONS
└── README.md        # This file
```


## How to Play

1. Menu screen — choose Human vs Human or Human vs Computer

2. Setup screen*— enter player name(s). If playing vs Computer, choose Easy or Hard difficulty

3. Game screen — click any empty cell to place your symbol. Player 1 is always X and goes first.

Winning — get three of your symbols in a row horizontally, vertically, or diagonally.

After each round:
- Click New Round to play again with the same players and keep scores
- Click Change Players to switch modes or swap players
  - Same players → scores are kept
  - New players → scores reset

---

## How the AI Works

Easy mode: picks a random free cell every turn.

Hard mode: uses the minimax algorithm -> a recursive decision tree that simulates every possible future move and always picks the optimal one. It scores positions like this:

- AI wins → `+10` (adjusted for depth so faster wins score higher)
- Opponent wins → `-10`
- Draw → `0`

## Score Tracking

The scoreboard at the top of the game screen tracks wins and draws across all rounds in a session. Scores only reset when you select New Players is in the Change Players flow.

---

## File Purposes

| File | Responsibility |
|---|---|
| `main.py` | Launches the app — nothing else |
| `ui.py` | All screens (`MenuScreen`, `SetupScreen`, `GameScreen`) and the main `App` class |
| `logic.py` | `check_winner()`, `is_draw()`, `minimax()`, `best_ai_move()`, global counters |
| `constants.py` | All colour hex codes, font tuples, `WIN_CONDITIONS` |

