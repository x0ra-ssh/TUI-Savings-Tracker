# TUI Savings Tracker

> **A terminal-native approach to disciplined saving.**

TUI Savings Tracker is a lightweight, keyboard-driven savings challenge built for the terminal.

It takes a deliberately simple premise: saving money is easier to understand when progress is visible, interaction is immediate, and the software stays out of the way.

The application provides a 50-tile savings challenge with a total target of 10,000 units, persistent local state, configurable themes, and a dashboard designed around the information that actually matters.

No account system. No cloud dependency. No financial dashboard pretending it needs machine learning.

Just the numbers.

---

## Philosophy

TUI Savings Tracker takes inspiration from the design philosophy of serious terminal applications such as `btop`:

* information should be visible at a glance
* interaction should be keyboard-first
* the interface should remain responsive
* configuration should belong to the user
* visual design should support information rather than compete with it

The result is less of a traditional command-line utility and more of a small, self-contained terminal workspace.

---

## The 10,000 Challenge

The tracker contains **50 savings tiles** distributed across five contribution values:

```text
100
150
200
250
300
```

Each value appears ten times.

That produces:

```text
50 tiles
×
2,000 total per five-value set
×
5 sets
=
10,000 total
```

More simply:

```text
100 + 150 + 200 + 250 + 300 = 1,000

1,000 × 10 = 10,000
```

Every tile represents one contribution.

Complete the grid, and the challenge is complete.

---

## Interface

The application is designed as a persistent dashboard rather than a sequence of numbered menus.

The interface is built around several ideas:

```text
┌─────────────────────────────────────────────────────────────┐
│                    TUI SAVINGS TRACKER                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PROGRESS        ███████████████████░░░░░░░░░░   47.5%      │
│                  4,750 / 10,000                             │
│                                                             │
├──────────────────────────────────────┬──────────────────────┤
│                                      │ SUMMARY              │
│  SAVINGS GRID                        │                      │
│                                      │ SAVED      ₹4,750    │
│  ┌────────┐ ┌────────┐ ┌────────┐   │ GOAL       ₹10,000   │
│  │ ✓ 01   │ │ · 02   │ │ ✓ 03   │   │ REMAIN     ₹5,250    │
│  │    100 │ │    150 │ │    200 │   │ TILES      20 / 50   │
│  └────────┘ └────────┘ └────────┘   │                      │
│                                      │ THEME      Arch Cyan │
│                                      │                      │
├──────────────────────────────────────┴──────────────────────┤
│ ↑↓←→ Navigate   Enter Save   r Unmark   R Reset   t Theme  │
│ c Currency   q Quit                                           │
└─────────────────────────────────────────────────────────────┘
```

The exact layout adapts to the available terminal dimensions.

---

## Interaction

The interface is keyboard-first.

| Key       | Action                           |
| --------- | -------------------------------- |
| `↑ ↓ ← →` | Navigate the savings grid        |
| `Enter`   | Mark or unmark the selected tile |
| `r`       | Unmark the selected tile         |
| `R`       | Reset the entire tracker         |
| `t`       | Cycle through themes             |
| `c`       | Change the displayed currency    |
| `q`       | Exit                             |

There is no need to type a tile ID into a prompt every time you want to update your progress.

Select the tile.

Press `Enter`.

Move on.

---

## Themes

TUI Savings Tracker separates the application's visual identity from its underlying logic.

Available themes include:

* **Arch Cyan**
* **Nord Frost**
* **Dracula**
* **Gruvbox Retro**
* **Cyberpunk Neon**

The default aesthetic is inspired by the visual language of Linux terminals and Arch Linux, while the application itself remains platform-agnostic.

The theme system is intentionally data-driven, allowing new themes to be introduced without rewriting the rendering logic.

---

## Currency Display

The interface supports three display currencies:

```text
$   Dollar
€   Euro
₹   Rupee
```

This setting controls the **display symbol**, not exchange-rate conversion.

A tile worth `100` therefore remains `100`; only its presentation changes.

---

## Persistence

The application stores state locally in JSON files:

```text
savings_data.json
tracker_config.json
```

The savings file contains the state of each tile.

The configuration file stores interface preferences such as:

* selected theme
* displayed currency

No external service is required.

Your financial data stays where the application runs.

---

## Technical Design

The application is written in Python and uses the standard library for its core functionality.

Its architecture is intentionally lightweight:

```text
Input
  │
  ▼
Application State
  │
  ├── Savings Data
  ├── Selected Tile
  ├── Theme
  └── Currency
  │
  ▼
Renderer
  │
  ▼
Terminal
```

Persistent state is written atomically so that an interrupted write is less likely to leave the tracker with a partially-written data file.

Configuration is validated when loaded, and malformed configuration falls back to safe defaults.

---

## Why a TUI?

A graphical interface is not inherently better.

For a small utility that primarily displays structured information and responds to a handful of commands, a terminal interface has some useful properties:

* it starts instantly
* it consumes very little system resources
* it works well over SSH
* it remains usable without a desktop environment
* it encourages deliberate interaction
* it keeps the application's information density high

The terminal is not merely the environment here.

It is the interface.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/x0ra-ssh/Arch-themed-savings-tracker.git
cd Arch-themed-savings-tracker
```

Run the application:

```bash
python main.py
```

On systems where Python 3 is exposed as `python3`:

```bash
python3 main.py
```

The application uses the Python standard library and does not require an external database.

---

## Requirements

* Python 3
* A terminal capable of running `curses`
* UTF-8 terminal support recommended

Linux and Unix-like environments provide the most natural experience for the application.

Windows users may require a compatible curses implementation such as `windows-curses`.

---

## Data Model

Each savings tile is represented by a small JSON object:

```json
{
    "id": 1,
    "amount": 100,
    "saved": false
}
```

The tracker derives the important values from this state:

```text
Total Goal
Total Saved
Remaining
Completed Tiles
Progress Percentage
```

There is no separate "progress percentage" value to become stale.

It is calculated from the underlying state.

---

## Project Structure

```text
TUI Savings Tracker/
│
├── main.py
├── savings_data.json
├── tracker_config.json
├── README.md
├── LICENSE
└── .gitignore
```

The current implementation deliberately keeps the project compact. Complexity is introduced only when it earns its place.

---

## Roadmap

The current application is intentionally focused. Future development can extend the tracker without turning it into a miniature banking platform.

Potential directions include:

* contribution history
* timestamps for completed tiles
* savings velocity
* historical progress graphs
* custom savings challenges
* user-defined tile values
* multiple goals
* data export and import
* richer terminal widgets
* configurable layouts
* automated tests
* installable Python packaging

The guiding rule remains simple:

> **Make the interface more capable without making it more complicated.**

---

## Contributing

Contributions are welcome.

When proposing changes, prioritize:

**clarity, reliability, usability, and restraint.**

A feature should solve a real problem before it earns a place in the interface.

---

## License

This project is licensed under the **GNU General Public License v3.0**.

See [`LICENSE`](./LICENSE) for the complete license text.

---

## Closing

Most budgeting software tries to become a financial command center.

TUI Savings Tracker does not.

It gives you a fixed objective, a visible representation of progress, and a quiet place to keep moving toward it.

**50 tiles. 10,000 units. One terminal.**

That is enough.
