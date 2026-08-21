# Arch Savings Tracker

> **Save money. Track progress. Stay in control.**

A minimal, terminal-based savings tracker inspired by the philosophy and aesthetic of Arch Linux.

No bloated dashboards. No subscriptions. No accounts. No unnecessary analytics.

Just your goals, your money, and a terminal.

---

## Why?

Saving money is easy to understand and surprisingly difficult to maintain.

Arch Savings Tracker is built around a simple idea: personal finance does not need to become another complicated application you have to manage.

Set a goal.

Save towards it.

Track your progress.

Repeat.

The terminal is fast, transparent, and already sitting in front of you. Might as well make it useful.

---

## Features

* **Savings Goals**
  Create and track financial goals with a defined target.

* **Contribution Tracking**
  Record savings contributions and keep your progress up to date.

* **Progress Visualization**
  See exactly how close you are to reaching your target.

* **Terminal-First Interface**
  Designed for people who would rather type a command than navigate twelve dashboard cards.

* **Arch-Inspired Design**
  A minimal interface influenced by Arch Linux and the Unix philosophy.

* **Local-First**
  Your financial data stays on your machine instead of becoming another entry in someone's database.

* **Lightweight**
  No unnecessary infrastructure for a program whose primary job is basic arithmetic.

---

## Philosophy

Arch Linux is built around a few ideas that translate surprisingly well to personal finance:

**Simplicity. Transparency. Control.**

The tracker follows the same approach.

You should always know:

```text
Target
Saved
Remaining
Progress
```

Nothing is hidden behind unnecessary abstractions.

No algorithm needs to "understand your spending personality."

No machine learning model needs to tell you that spending ₹4,000 while trying to save ₹3,000 is probably suboptimal.

The numbers are right there.

---

## Preview

```text
╭────────────────────────────────────────────╮
│          ARCH SAVINGS TRACKER              │
├────────────────────────────────────────────┤
│                                            │
│  Goal: New Guitar                          │
│                                            │
│  Target       ₹30,000                      │
│  Saved        ₹18,500                      │
│  Remaining    ₹11,500                      │
│                                            │
│  Progress     ████████████░░░░  61.7%      │
│                                            │
│  Status       Saving...                    │
│                                            │
╰────────────────────────────────────────────╯
```

Your terminal has never looked this financially responsible.

---

## Tech Stack

Built with:

* Python
* Terminal-based UI
* Local data persistence
* Standard Python tooling

The project intentionally keeps its dependency footprint small.

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

Depending on your environment, you may need to use `python3` instead.

---

## Usage

Launch the tracker and use the terminal interface to:

1. Create a savings goal.
2. Define the target amount.
3. Record contributions.
4. Monitor your progress.
5. Continue saving until the goal is reached.

Simple by design.

---

## Project Structure

```text
Arch-themed-savings-tracker/
│
├── main.py
├── LICENSE
├── .gitignore
└── README.md
```

The project is intentionally small and approachable.

There is no reason for a savings tracker to require an enterprise architecture diagram.

---

## Privacy

Your financial information is personal.

This project is designed around local usage rather than sending your financial activity to a remote service.

Your savings should remain your business.

---

## Roadmap

The project can naturally grow without losing its simplicity.

Potential improvements include:

* Multiple savings goals
* Expense tracking
* Monthly budgets
* Data export and import
* Rich terminal charts
* Custom themes
* Goal deadlines
* Savings projections
* Configuration files
* Automated testing
* Installable CLI packages

The objective is not to add features for the sake of having features.

The objective is to make the tracker more useful while keeping it lightweight.

---

## Contributing

Contributions, improvements, bug fixes, and ideas are welcome.

If you're extending the project, keep its core philosophy intact:

**Simple. Transparent. Useful.**

Fork the repository, make your changes, and open a pull request.

---

## License

This project is licensed under the **GNU General Public License v3.0**.

See [`LICENSE`](./LICENSE) for the full license text.

---

## Final Thought

There are thousands of budgeting applications competing to tell you that you spent too much money on coffee.

This one takes a different approach.

It gives you a goal, shows you the numbers, and gets out of the way.

**Open the terminal. Set the goal. Start saving.**

> *Keep it simple. Keep it yours.*
