# Hexcells Infinite Cheating Bot

[pyautogui](https://github.com/asweigart/pyautogui) bot for [Hexcells Infinite](http://store.steampowered.com/app/304410/). Clicks on all cells to gather info, then restarts and solves the puzzle. [See in action](https://youtu.be/JxS-W3wf76M).

Run when the puzzle screen is visible in 1280x720 windowed resolution:
```
py hexcells.py [option]
```

Options:
- Regular mode. Solve all the puzzles in a chapter, and then waits for the user input. All six chapters can be solved under 25 minutes.
- "-u": Unlimited mode. Keeps solving randomly generated puzzles.
- "-f": 'Fast' mode, keeps solving the same puzzle. '60 down 999,999,940 to go' achievement can be unlocked under 15 minutes.
