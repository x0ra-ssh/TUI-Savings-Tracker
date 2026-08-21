import curses
import json
import os
import tempfile

DATA_FILE = "savings_data.json"
CONFIG_FILE = "tracker_config.json"

APP_NAME = "TUI SAVINGS TRACKER"
VERSION = "4.0"

AMOUNTS = [100, 150, 200, 250, 300] * 10

CURRENCIES = [
    {"name": "Dollar", "symbol": "$"},
    {"name": "Euro", "symbol": "€"},
    {"name": "Rupee", "symbol": "₹"},
]

THEMES = [
    {
        "name": "Arch Cyan",
        "primary": 39,
        "accent": 51,
        "success": 46,
        "warning": 214,
        "danger": 203,
        "muted": 103,
        "text": 255,
        "background": -1,
    },
    {
        "name": "Nord Frost",
        "primary": 110,
        "accent": 117,
        "success": 108,
        "warning": 179,
        "danger": 131,
        "muted": 60,
        "text": 255,
        "background": -1,
    },
    {
        "name": "Dracula",
        "primary": 141,
        "accent": 212,
        "success": 84,
        "warning": 222,
        "danger": 204,
        "muted": 61,
        "text": 255,
        "background": -1,
    },
    {
        "name": "Gruvbox Retro",
        "primary": 208,
        "accent": 220,
        "success": 142,
        "warning": 214,
        "danger": 167,
        "muted": 102,
        "text": 223,
        "background": -1,
    },
    {
        "name": "Cyberpunk Neon",
        "primary": 51,
        "accent": 201,
        "success": 118,
        "warning": 208,
        "danger": 196,
        "muted": 103,
        "text": 255,
        "background": -1,
    },
]


# ============================================================
# PERSISTENCE
# ============================================================

def atomic_write(path, data):
    """
    Write JSON atomically.

    Prevents a partially-written JSON file if the program is
    interrupted while saving.
    """
    directory = os.path.dirname(os.path.abspath(path)) or "."
    fd, temp_path = tempfile.mkstemp(
        prefix=".tui_tracker_",
        suffix=".tmp",
        dir=directory,
        text=True,
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            file.write("\n")

        os.replace(temp_path, path)

    except Exception:
        try:
            os.remove(temp_path)
        except OSError:
            pass
        raise


def default_data():
    return [
        {
            "id": index,
            "amount": amount,
            "saved": False,
        }
        for index, amount in enumerate(AMOUNTS, 1)
    ]


def load_data():
    if not os.path.exists(DATA_FILE):
        data = default_data()
        atomic_write(DATA_FILE, data)
        return data

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Savings data must be a list.")

        for item in data:
            if not all(key in item for key in ("id", "amount", "saved")):
                raise ValueError("Savings data contains an invalid entry.")

        return data

    except (json.JSONDecodeError, ValueError, OSError) as error:
        raise RuntimeError(
            f"Unable to load {DATA_FILE}: {error}"
        ) from error


def default_config():
    return {
        "currency_index": 0,
        "theme_index": 0,
    }


def load_config():
    if not os.path.exists(CONFIG_FILE):
        config = default_config()
        atomic_write(CONFIG_FILE, config)
        return config

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            config = json.load(file)

        if not isinstance(config, dict):
            raise ValueError("Configuration must be an object.")

        config.setdefault("currency_index", 0)
        config.setdefault("theme_index", 0)

        config["currency_index"] %= len(CURRENCIES)
        config["theme_index"] %= len(THEMES)

        return config

    except (json.JSONDecodeError, ValueError, OSError):
        config = default_config()
        atomic_write(CONFIG_FILE, config)
        return config


def save_config(config):
    atomic_write(CONFIG_FILE, config)


def save_data(data):
    atomic_write(DATA_FILE, data)


# ============================================================
# DATA / CALCULATIONS
# ============================================================

def total_goal(data):
    return sum(item["amount"] for item in data)


def total_saved(data):
    return sum(
        item["amount"]
        for item in data
        if item["saved"]
    )


def completed_tiles(data):
    return sum(
        1
        for item in data
        if item["saved"]
    )


def progress_ratio(data):
    goal = total_goal(data)

    if goal <= 0:
        return 0.0

    return min(max(total_saved(data) / goal, 0.0), 1.0)


# ============================================================
# CURSES / COLORS
# ============================================================

PAIR_PRIMARY = 1
PAIR_ACCENT = 2
PAIR_SUCCESS = 3
PAIR_WARNING = 4
PAIR_DANGER = 5
PAIR_MUTED = 6
PAIR_TEXT = 7
PAIR_SELECTED = 8
PAIR_BORDER = 9


def setup_colors(theme):
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(
        PAIR_PRIMARY,
        theme["primary"],
        theme["background"],
    )

    curses.init_pair(
        PAIR_ACCENT,
        theme["accent"],
        theme["background"],
    )

    curses.init_pair(
        PAIR_SUCCESS,
        theme["success"],
        theme["background"],
    )

    curses.init_pair(
        PAIR_WARNING,
        theme["warning"],
        theme["background"],
    )

    curses.init_pair(
        PAIR_DANGER,
        theme["danger"],
        theme["background"],
    )

    curses.init_pair(
        PAIR_MUTED,
        theme["muted"],
        theme["background"],
    )

    curses.init_pair(
        PAIR_TEXT,
        theme["text"],
        theme["background"],
    )

    curses.init_pair(
        PAIR_SELECTED,
        theme["background"],
        theme["accent"],
    )

    curses.init_pair(
        PAIR_BORDER,
        theme["muted"],
        theme["background"],
    )


def color(pair, attributes=0):
    return curses.color_pair(pair) | attributes


# ============================================================
# SAFE DRAWING
# ============================================================

def add_text(window, y, x, text, style=0):
    """
    Draw text without crashing when the terminal is resized
    or the string reaches the screen edge.
    """
    try:
        window.addstr(y, x, text, style)
    except curses.error:
        pass


def horizontal_line(window, y, x, width, style):
    if width <= 0:
        return

    add_text(window, y, x, "─" * width, style)


# ============================================================
# UI COMPONENTS
# ============================================================

def draw_header(stdscr, width, theme):
    title = f" {APP_NAME} "
    version = f"v{VERSION}"

    add_text(
        stdscr,
        0,
        1,
        title,
        color(PAIR_PRIMARY, curses.A_BOLD),
    )

    add_text(
        stdscr,
        0,
        max(1, width - len(version) - 2),
        version,
        color(PAIR_MUTED),
    )

    horizontal_line(
        stdscr,
        1,
        0,
        width,
        color(PAIR_BORDER),
    )


def draw_progress(stdscr, data, y, width, theme):
    saved = total_saved(data)
    goal = total_goal(data)
    ratio = progress_ratio(data)

    label = "PROGRESS"
    percentage = f"{ratio * 100:5.1f}%"

    add_text(
        stdscr,
        y,
        2,
        label,
        color(PAIR_ACCENT, curses.A_BOLD),
    )

    bar_x = 13
    percentage_x = max(bar_x + 5, width - len(percentage) - 3)
    bar_width = max(10, percentage_x - bar_x - 2)

    filled = int(bar_width * ratio)

    bar = (
        "█" * filled
        + "░" * (bar_width - filled)
    )

    bar_style = (
        color(PAIR_SUCCESS, curses.A_BOLD)
        if ratio >= 1.0
        else color(PAIR_ACCENT)
    )

    add_text(
        stdscr,
        y,
        bar_x,
        bar,
        bar_style,
    )

    add_text(
        stdscr,
        y,
        percentage_x,
        percentage,
        color(PAIR_TEXT, curses.A_BOLD),
    )

    stats = (
        f"{saved:,} / {goal:,}"
    )

    add_text(
        stdscr,
        y + 1,
        2,
        stats,
        color(PAIR_MUTED),
    )


def draw_stat_panel(
    stdscr,
    data,
    config,
    x,
    y,
    width,
    height,
):
    if width < 20 or height < 5:
        return

    sym = CURRENCIES[
        config["currency_index"]
    ]["symbol"]

    saved = total_saved(data)
    goal = total_goal(data)
    remaining = goal - saved
    tiles = completed_tiles(data)

    right = x + width - 1
    bottom = y + height - 1

    # Border
    add_text(
        stdscr,
        y,
        x,
        "┌" + "─" * (width - 2) + "┐",
        color(PAIR_BORDER),
    )

    for row in range(y + 1, bottom):
        add_text(
            stdscr,
            row,
            x,
            "│",
            color(PAIR_BORDER),
        )

        add_text(
            stdscr,
            row,
            right,
            "│",
            color(PAIR_BORDER),
        )

    add_text(
        stdscr,
        bottom,
        x,
        "└" + "─" * (width - 2) + "┘",
        color(PAIR_BORDER),
    )

    add_text(
        stdscr,
        y + 1,
        x + 2,
        "SUMMARY",
        color(PAIR_ACCENT, curses.A_BOLD),
    )

    rows = [
        ("SAVED", f"{sym}{saved:,}", PAIR_SUCCESS),
        ("GOAL", f"{sym}{goal:,}", PAIR_TEXT),
        ("REMAIN", f"{sym}{remaining:,}", PAIR_WARNING),
        ("TILES", f"{tiles}/{len(data)}", PAIR_ACCENT),
        (
            "THEME",
            THEMES[config["theme_index"]]["name"],
            PAIR_PRIMARY,
        ),
        (
            "CURRENCY",
            CURRENCIES[
                config["currency_index"]
            ]["name"],
            PAIR_TEXT,
        ),
    ]

    current_y = y + 3

    for label, value, pair in rows:
        if current_y >= bottom - 1:
            break

        add_text(
            stdscr,
            current_y,
            x + 2,
            f"{label:<9}",
            color(PAIR_MUTED),
        )

        max_value_width = width - 14

        if len(value) > max_value_width:
            value = value[:max_value_width]

        add_text(
            stdscr,
            current_y,
            x + 12,
            value,
            color(pair, curses.A_BOLD),
        )

        current_y += 2


def calculate_grid(
    data_count,
    available_width,
):
    """
    Dynamically choose the number of columns.

    This is what makes it feel like a real TUI instead of a
    screenshot trapped in a terminal.
    """
    min_cell_width = 12

    columns = max(
        1,
        min(
            5,
            available_width // min_cell_width,
        ),
    )

    rows = (
        data_count + columns - 1
    ) // columns

    return columns, rows


def draw_tile(
    stdscr,
    item,
    x,
    y,
    width,
    selected,
):
    if width < 7:
        return

    amount = item["amount"]
    item_id = item["id"]
    saved = item["saved"]

    if selected:
        style = color(
            PAIR_SELECTED,
            curses.A_BOLD,
        )
    elif saved:
        style = color(
            PAIR_SUCCESS,
            curses.A_BOLD,
        )
    else:
        style = color(
            PAIR_TEXT,
            curses.A_NORMAL,
        )

    if saved:
        symbol = "✓"
    else:
        symbol = "·"

    top = "┌" + "─" * (width - 2) + "┐"
    middle = f"│ {symbol} {item_id:02d}"
    bottom = "└" + "─" * (width - 2) + "┘"

    middle += " " * max(
        0,
        width - len(middle) - 1,
    )

    middle += "│"

    add_text(
        stdscr,
        y,
        x,
        top,
        style,
    )

    add_text(
        stdscr,
        y + 1,
        x,
        middle,
        style,
    )

    amount_text = f"{amount:,}"

    amount_text = amount_text[
        : max(1, width - 4)
    ]

    add_text(
        stdscr,
        y + 2,
        x,
        f"│ {amount_text:>{width - 4}} │",
        style,
    )

    add_text(
        stdscr,
        y + 3,
        x,
        bottom,
        style,
    )


def draw_grid(
    stdscr,
    data,
    selected_index,
    x,
    y,
    width,
    height,
):
    if width < 12 or height < 6:
        return

    columns, rows = calculate_grid(
        len(data),
        width,
    )

    cell_width = width // columns

    visible_rows = max(
        1,
        (height - 1) // 5,
    )

    selected_row = selected_index // columns

    # Simple vertical scrolling.
    scroll_row = max(
        0,
        selected_row - visible_rows + 1,
    )

    start_index = scroll_row * columns
    end_index = min(
        len(data),
        start_index + visible_rows * columns,
    )

    current_y = y

    for index in range(start_index, end_index):
        relative_index = index - start_index

        row = relative_index // columns
        column = relative_index % columns

        tile_x = x + column * cell_width
        tile_y = current_y + row * 5

        draw_tile(
            stdscr,
            data[index],
            tile_x,
            tile_y,
            cell_width - 1,
            index == selected_index,
        )


def draw_footer(stdscr, height, width):
    footer_y = height - 2

    if footer_y < 0:
        return

    horizontal_line(
        stdscr,
        footer_y,
        0,
        width,
        color(PAIR_BORDER),
    )

    controls = (
        "↑↓←→ Navigate   "
        "Enter Save   "
        "r Unmark   "
        "R Reset   "
        "t Theme   "
        "c Currency   "
        "q Quit"
    )

    if len(controls) > width - 2:
        controls = (
            "Arrows Navigate   Enter Save   "
            "r Unmark   R Reset   t Theme   "
            "c Currency   q Quit"
        )

    controls = controls[: max(0, width - 2)]

    add_text(
        stdscr,
        height - 1,
        1,
        controls,
        color(PAIR_MUTED),
    )


def draw_status(stdscr, message, height, width):
    if not message:
        return

    y = height - 3

    if y < 0:
        return

    message = message[: max(0, width - 4)]

    add_text(
        stdscr,
        y,
        2,
        message,
        color(PAIR_ACCENT, curses.A_BOLD),
    )


# ============================================================
# CONFIRMATION
# ============================================================

def confirm_reset(stdscr, data):
    height, width = stdscr.getmaxyx()

    message = "Reset ALL savings progress? [y/N]"

    box_width = min(
        max(len(message) + 6, 40),
        width - 4,
    )

    box_height = 5

    start_y = max(
        0,
        (height - box_height) // 2,
    )

    start_x = max(
        0,
        (width - box_width) // 2,
    )

    win = curses.newwin(
        box_height,
        box_width,
        start_y,
        start_x,
    )

    win.keypad(True)

    win.bkgd(" ", color(PAIR_TEXT))

    win.border(
        "│",
        "│",
        "─",
        "─",
        "╭",
        "╮",
        "╰",
        "╯",
    )

    add_text(
        win,
        1,
        2,
        "RESET TRACKER",
        color(PAIR_DANGER, curses.A_BOLD),
    )

    add_text(
        win,
        2,
        2,
        message[:box_width - 4],
        color(PAIR_TEXT),
    )

    add_text(
        win,
        3,
        2,
        "Press y to confirm, any other key to cancel.",
        color(PAIR_MUTED),
    )

    win.refresh()

    key = win.getch()

    del win

    return key in (ord("y"), ord("Y"))


# ============================================================
# NAVIGATION
# ============================================================

def move_selection(
    selected,
    key,
    item_count,
    columns,
):
    if item_count <= 0:
        return 0

    row = selected // columns
    column = selected % columns

    if key == curses.KEY_LEFT:
        column -= 1

    elif key == curses.KEY_RIGHT:
        column += 1

    elif key == curses.KEY_UP:
        row -= 1

    elif key == curses.KEY_DOWN:
        row += 1

    else:
        return selected

    row = max(0, row)
    column = max(0, column)

    new_index = row * columns + column

    if new_index >= item_count:
        new_index = item_count - 1

    return new_index


# ============================================================
# MAIN TUI
# ============================================================

def run_app(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    try:
        stdscr.timeout(250)
    except curses.error:
        pass

    data = load_data()
    config = load_config()

    selected = 0
    status = ""

    while True:
        height, width = stdscr.getmaxyx()

        theme = THEMES[
            config["theme_index"]
        ]

        setup_colors(theme)

        stdscr.erase()

        if width < 70 or height < 20:
            add_text(
                stdscr,
                max(0, height // 2 - 1),
                max(0, (width - 48) // 2),
                "Terminal too small for TUI.",
                color(PAIR_WARNING, curses.A_BOLD),
            )

            add_text(
                stdscr,
                max(0, height // 2 + 1),
                max(0, (width - 54) // 2),
                "Resize to at least 70x20.",
                color(PAIR_MUTED),
            )

            stdscr.refresh()

            key = stdscr.getch()

            if key in (
                ord("q"),
                ord("Q"),
            ):
                break

            continue

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        draw_header(
            stdscr,
            width,
            theme,
        )

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        draw_progress(
            stdscr,
            data,
            3,
            width,
            theme,
        )

        horizontal_line(
            stdscr,
            5,
            0,
            width,
            color(PAIR_BORDER),
        )

        # ----------------------------------------------------
        # MAIN AREA
        # ----------------------------------------------------

        main_y = 6
        main_height = height - main_y - 4

        sidebar_width = min(
            29,
            max(24, width // 4),
        )

        grid_width = width - sidebar_width - 3

        draw_grid(
            stdscr,
            data,
            selected,
            1,
            main_y,
            grid_width,
            main_height,
        )

        draw_stat_panel(
            stdscr,
            data,
            config,
            grid_width + 2,
            main_y,
            sidebar_width,
            main_height,
        )

        # ----------------------------------------------------
        # STATUS + FOOTER
        # ----------------------------------------------------

        draw_status(
            stdscr,
            status,
            height,
            width,
        )

        draw_footer(
            stdscr,
            height,
            width,
        )

        stdscr.refresh()

        key = stdscr.getch()

        if key == -1:
            continue

        # ----------------------------------------------------
        # QUIT
        # ----------------------------------------------------

        if key in (ord("q"), ord("Q")):
            break

        # ----------------------------------------------------
        # NAVIGATION
        # ----------------------------------------------------

        elif key in (
            curses.KEY_LEFT,
            curses.KEY_RIGHT,
            curses.KEY_UP,
            curses.KEY_DOWN,
        ):
            columns, _ = calculate_grid(
                len(data),
                grid_width,
            )

            selected = move_selection(
                selected,
                key,
                len(data),
                columns,
            )

            status = ""

        # ----------------------------------------------------
        # TOGGLE SAVED
        # ----------------------------------------------------

        elif key in (
            curses.KEY_ENTER,
            10,
            13,
        ):
            item = data[selected]

            item["saved"] = not item["saved"]

            save_data(data)

            if item["saved"]:
                status = (
                    f"Tile {item['id']:02d} saved "
                    f"({item['amount']:,})."
                )
            else:
                status = (
                    f"Tile {item['id']:02d} marked unsaved."
                )

        # ----------------------------------------------------
        # UNMARK SELECTED
        # ----------------------------------------------------

        elif key in (ord("r"), ord("R")):
            if key == ord("R"):
                if confirm_reset(
                    stdscr,
                    data,
                ):
                    for item in data:
                        item["saved"] = False

                    save_data(data)

                    selected = 0
                    status = "All savings progress reset."

            else:
                item = data[selected]

                if item["saved"]:
                    item["saved"] = False
                    save_data(data)

                    status = (
                        f"Tile {item['id']:02d} unmarked."
                    )
                else:
                    status = (
                        f"Tile {item['id']:02d} is already empty."
                    )

        # ----------------------------------------------------
        # THEME
        # ----------------------------------------------------

        elif key in (ord("t"), ord("T")):
            config["theme_index"] = (
                config["theme_index"] + 1
            ) % len(THEMES)

            save_config(config)

            status = (
                f"Theme: "
                f"{THEMES[config['theme_index']]['name']}"
            )

        # ----------------------------------------------------
        # CURRENCY
        # ----------------------------------------------------

        elif key in (ord("c"), ord("C")):
            config["currency_index"] = (
                config["currency_index"] + 1
            ) % len(CURRENCIES)

            save_config(config)

            currency = CURRENCIES[
                config["currency_index"]
            ]

            status = (
                f"Currency display: "
                f"{currency['name']} "
                f"({currency['symbol']})"
            )

        # ----------------------------------------------------
        # RESIZE
        # ----------------------------------------------------

        elif key == curses.KEY_RESIZE:
            status = "Layout resized."


def main():
    try:
        curses.wrapper(run_app)

    except RuntimeError as error:
        print(f"TUI Savings Tracker: {error}")

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
