# Arch Savings Tracker

> **A 10,000-unit savings challenge for the terminal.**

A minimal, Arch-inspired terminal savings tracker built with Python.

The concept is deliberately simple: **50 savings tiles, one fixed goal, and a terminal interface that makes watching the number go up considerably more satisfying than it has any right to be.**

No accounts. No cloud dashboard. No subscription.

Just save a tile, watch the grid fill up, and eventually discover that apparently small amounts of money do, in fact, become real money when you stop spending them.

---

## The Idea

Arch Savings Tracker is built around a simple **50-tile savings challenge**.

The tracker contains 50 tiles with values ranging from **100 to 300**, adding up to a total savings target of **10,000**.

Each tile represents one contribution.

Mark a tile as saved, and your progress increases.

Fill the grid, and you've completed the challenge.

```text
50 Tiles
    |
    v
Save a Tile
    |
    v
Progress Updates
    |
    v
10,000 Goal
```

It's intentionally more visual than a conventional expense tracker.

Instead of staring at a balance and wondering whether you're making progress, you can watch the grid gradually disappear into completion.

---

## Features

### 50-Tile Savings Grid

The core of the application is a 50-entry savings challenge.

Each tile has a fixed contribution amount and can be marked as saved when you've completed it.

The grid provides an immediate overview of what you've completed and what remains.

### Live Progress Bar

The tracker calculates your current savings progress and displays it as a terminal progress bar.

```text
Progress:[████████████████████░░░░░░░░░░░░░░░░] 50.0%
```

### Financial Summary

Get a compact overview of:

* Total saved
* Total goal
* Remaining amount
* Completed tiles

Because sometimes you just need the numbers without a motivational TED Talk.

### Multiple Currencies

Choose between:

```text
$
€
₹
```

The currency setting is stored locally and persists between sessions.

### Five Terminal Themes

Choose from five built-in color schemes:

* Arch Cyan
* Nord Frost
* Dracula
* Gruvbox Retro
* Cyberpunk Neon

The interface uses ANSI TrueColor formatting to give the terminal a proper themed experience rather than dumping plain text into a shell and calling it a UI.

### Local Persistence

The tracker stores its state locally using JSON.

Two files are used:

```text
savings_data.json
tracker_config.json
```

Your progress and interface preferences survive application restarts without requiring an account or external service.

---

## Preview

```text
       /\         ARCH SAVINGS TRACKER v3.0
      /  \        ====================================
     /  /\       OS Host: Arch Linux CLI (TUI Engine)
    /  /  \      Target:  50-Tile Grid (Goal: 10,000)
   /  /__  \     Theme:   Arch Cyan (Official)
  /______  \
 /        \  \

--- SAVINGS PROGRESS GRID ---

Progress:[████████████████████████░░░░░░░░] 61.0%

+-----------------------+-----------------------+
| ID | Amt    | State  | ID | Amt    | State  |
+-----------------------+-----------------------+
|  1 | ₹100   | [✓]    |  2 | ₹150   | [✓]    |
+-----------------------+-----------------------+

=================== STATS SUMMARY ===================
Total Saved: ₹6,100 / ₹10,000
Remaining  : ₹3,900
Tiles Done : 30 of 50 completed
=====================================================
```

---

## Interface

The main menu provides seven operations:

```text
[1] View Progress Grid
[2] Mark Tile as Saved
[3] View Financial Summary
[4] Unmark Tile / Reset All
[5] Change Currency
[6] Change Color Theme
[7] Exit
```

The interface is intentionally menu-driven.

You don't need to remember a command hierarchy just to mark a tile as saved. The terminal tells you what to do.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/x0ra-ssh/Arch-themed-savings-tracker.git
cd Arch-themed-savings-tracker
```

Run:

```bash
python main.py
```

On systems where Python is invoked as `python3`:

```bash
python3 main.py
```

No external database or server is required.

---

## How It Works

The application initializes a local JSON database containing the 50 savings tiles.

Each tile has three properties:

```json
{
    "id": 1,
    "amount": 100,
    "saved": false
}
```

When a tile is marked as saved, its state changes:

```json
{
    "id": 1,
    "amount": 100,
    "saved": true
}
```

The application then calculates:

```text
Total Goal = Sum of all tile amounts

Total Saved = Sum of saved tile amounts

Remaining = Total Goal - Total Saved

Progress = Total Saved / Total Goal
```

Nothing mysterious.

Just a small amount of arithmetic wearing a very serious terminal interface.

---

## Project Structure

```text
Arch-themed-savings-tracker/
│
├── main.py
├── savings_data.json       # Generated local progress data
├── tracker_config.json     # Generated configuration
├── .gitignore
├── LICENSE
└── README.md
```

The application itself is intentionally contained in a single Python entry point.

For a small terminal utility, that's a feature rather than an architectural crime.

---

## Design Philosophy

The project takes inspiration from the Unix and Arch Linux approach to software:

**Keep it simple. Keep it understandable. Keep the user in control.**

There is no backend.

There is no authentication system.

There is no telemetry.

There is no account creation flow.

There is no web application pretending that calculating a percentage requires a distributed architecture.

The tracker does one thing and tries to do it cleanly.

---

## Roadmap

Possible future improvements include:

* Custom savings goals
* User-defined tile amounts
* Multiple challenges
* Savings history
* Contribution timestamps
* Data export/import
* Richer terminal visualizations
* Command-line arguments
* Automated tests
* Configurable themes
* Installable Python package

The challenge is to expand the utility without destroying the simplicity that makes it useful in the first place.

---

## Contributing

Contributions are welcome.

If you want to improve the project, fork the repository, make your changes, and open a pull request.

Keep the core principle intact:

> **More useful, not merely more complicated.**

---

## License

This project is licensed under the **GNU General Public License v3.0**.

See [`LICENSE`](./LICENSE) for the complete license text.

---

## Final Note

Personal finance apps love dashboards.

Graphs. Notifications. Recommendations. Accounts. Syncing. Twelve different ways to tell you that you spent too much money.

Arch Savings Tracker takes the opposite route.

**Fifty tiles. Ten thousand. One terminal.**

Save the tile.

Fill the grid.

Finish the challenge.

> **Keep it simple. Keep it yours.**
