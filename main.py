import json
import os
import sys

DATA_FILE = 'savings_data.json'
CONFIG_FILE = 'tracker_config.json'

# 50 entries, all multiples of 10. (100+150+200+250+300 = 1000) * 10 = 10,000 total.
AMOUNTS = [100, 150, 200, 250, 300] * 10

# Available Currencies
CURRENCIES = [
    {"name": "Dollar", "symbol": "$"},
    {"name": "Euro", "symbol": "€"},
    {"name": "Rupee", "symbol": "₹"}
]

# Standard ANSI Code Controls
RESET = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'

# Arch Linux Inspired Color Themes (24-bit TrueColor ANSI)
THEMES = [
    {
        "name": "Arch Cyan (Official)",
        "primary": "\033[38;2;23;147;209m",    # Arch Linux Blue
        "accent": "\033[38;2;120;220;255m",   # Sky Cyan
        "success": "\033[38;2;80;250;123m",   # Neon Green
        "pending": "\033[38;2;255;85;85m",    # Coral Red
        "muted": "\033[38;2;98;114;164m",     # Slate Gray
        "text": "\033[38;2;248;248;242m",     # Bright White
    },
    {
        "name": "Nord Frost",
        "primary": "\033[38;2;136;192;208m",  # Frost Blue
        "accent": "\033[38;2;129;161;193m",   # Deep Frost
        "success": "\033[38;2;163;190;140m",  # Nord Green
        "pending": "\033[38;2;191;97;106m",   # Nord Red
        "muted": "\033[38;2;76;86;106m",      # Nord Slate
        "text": "\033[38;2;236;239;244m",    # Snow White
    },
    {
        "name": "Dracula",
        "primary": "\033[38;2;189;147;249m",  # Dracula Purple
        "accent": "\033[38;2;255;121;198m",   # Dracula Pink
        "success": "\033[38;2;80;250;123m",   # Dracula Green
        "pending": "\033[38;2;255;85;85m",    # Dracula Red
        "muted": "\033[38;2;98;114;164m",     # Slate Gray
        "text": "\033[38;2;248;248;242m",
    },
    {
        "name": "Gruvbox Retro",
        "primary": "\033[38;2;254;128;25m",   # Gruvbox Orange
        "accent": "\033[38;2;250;189;47m",    # Gruvbox Yellow
        "success": "\033[38;2;184;187;38m",   # Gruvbox Green
        "pending": "\033[38;2;251;73;52m",    # Gruvbox Red
        "muted": "\033[38;2;146;131;116m",   # Slate Gray
        "text": "\033[38;2;235;219;178m",
    },
    {
        "name": "Cyberpunk Neon",
        "primary": "\033[38;2;0;240;255m",    # Electric Blue
        "accent": "\033[38;2;255;0;85m",      # Neon Pink
        "success": "\033[38;2;57;255;20m",    # Neon Green
        "pending": "\033[38;2;255;100;0m",    # Neon Orange
        "muted": "\033[38;2;100;100;120m",
        "text": "\033[38;2;255;255;255m",
    }
]

# ==========================================
# CONFIGURATION & STATE
# ==========================================

def load_config():
    """Load config or create default settings."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                cfg = json.load(f)
                cfg.setdefault("currency_index", 0)
                cfg.setdefault("theme_index", 0)
                return cfg
        except Exception:
            pass
    default_config = {"currency_index": 0, "theme_index": 0}
    save_config(default_config)
    return default_config

def save_config(config):
    """Save user configuration."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def get_theme(config):
    """Retrieve active theme colors."""
    idx = config.get("theme_index", 0) % len(THEMES)
    return THEMES[idx]

def clear_screen():
    """Clear terminal screen for clean TUI redraws."""
    os.system('cls' if os.name == 'nt' else 'clear')

# ==========================================
# ARCH TUI RENDERERS
# ==========================================

def print_arch_header(config):
    """Render Arch Linux ASCII logo and header."""
    theme = get_theme(config)
    p = theme["primary"]
    a = theme["accent"]
    m = theme["muted"]
    t = theme["text"]

    logo = [
        f"       {p}/\\{RESET}         {BOLD}{t}ARCH SAVINGS TRACKER{RESET} {DIM}v3.0{RESET}",
        f"      {p}/  \\{RESET}        {m}===================================={RESET}",
        f"     {p}/  /\\{RESET}       {a}OS Host:{RESET} {t}Arch Linux CLI (TUI Engine){RESET}",
        f"    {p}/  /  \\{RESET}      {a}Target:{RESET}  {t}50-Tile Grid (Goal: 10,000){RESET}",
        f"   {p}/  /__  \\{RESET}     {a}Theme:{RESET}   {theme['name']}",
        f"  {p}/______  \\{RESET}    {m}------------------------------------{RESET}",
        f" {p}/        \\  \\{RESET}"
    ]
    for line in logo:
        print(line)

def draw_progress_bar(saved_amount, total_goal, theme, width=40):
    """Render a terminal progress bar."""
    ratio = min(max(saved_amount / total_goal, 0.0), 1.0) if total_goal > 0 else 0
    filled_len = int(width * ratio)
    bar = '█' * filled_len + '░' * (width - filled_len)
    percentage = ratio * 100
    
    color = theme["success"] if ratio == 1.0 else theme["accent"]
    print(f"{BOLD}{theme['text']}Progress:[{color}{bar}{theme['text']}] {color}{percentage:5.1f}%{RESET}")

# ==========================================
# DATABASE OPERATIONS
# ==========================================

def create_database():
    """Initialize JSON data file if missing."""
    if not os.path.exists(DATA_FILE):
        data = [
            {"id": i, "amount": amount, "saved": False}
            for i, amount in enumerate(AMOUNTS, 1)
        ]
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

def read_progress(config):
    """Display the 50-item grid in an Excel-like layout."""
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    theme = get_theme(config)
    sym = CURRENCIES[config["currency_index"]]["symbol"]
    
    total_goal = sum(item["amount"] for item in data)
    total_saved = sum(item["amount"] for item in data if item["saved"])

    print(f"\n{BOLD}{theme['primary']}--- SAVINGS PROGRESS GRID ---{RESET}")
    draw_progress_bar(total_saved, total_goal, theme)
    print()

    # Calculate row width based on 5 columns
    col_width = 23
    divider = theme["muted"] + "+" + ("-" * (col_width + 1)) * 5 + "+" + RESET

    print(divider)
    header_row = theme["muted"] + "|" + RESET
    for _ in range(5):
        header_row += f" {BOLD}{theme['accent']}ID{RESET} | {BOLD}{theme['accent']}Amt{RESET}    | {BOLD}{theme['accent']}State{RESET} {theme['muted']}|{RESET}"
    print(header_row)
    print(divider)

    for i in range(0, len(data), 5):
        row = data[i:i+5]
        row_str = theme["muted"] + "|" + RESET
        for house in row:
            if house["saved"]:
                status = f"{theme['success']}[✓]{RESET}"
            else:
                status = f"{theme['pending']}[ ]{RESET}"
                
            amt_str = f"{sym}{house['amount']}"
            cell = f" {house['id']:>2} | {amt_str:<6} | {status} "
            row_str += cell + theme["muted"] + "|" + RESET
            
        print(row_str)
        print(divider)

    show_summary(data, sym, config)

def update_entry(config):
    """Toggle or mark an entry as saved."""
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    theme = get_theme(config)
    try:
        raw_input = input(f"\n{BOLD}{theme['accent']}Enter ID to mark as SAVED (1-{len(data)}): {RESET}")
        house_id = int(raw_input)
        if 1 <= house_id <= len(data):
            if data[house_id - 1]["saved"]:
                print(f"{theme['muted']}ID {house_id} is already marked as saved.{RESET}")
            else:
                data[house_id - 1]["saved"] = True
                with open(DATA_FILE, 'w') as f:
                    json.dump(data, f, indent=4)
                print(f"{theme['success']}✔ Success! ID {house_id} marked as SAVED.{RESET}")
        else:
            print(f"{theme['pending']}Invalid ID range.{RESET}")
    except ValueError:
        print(f"{theme['pending']}Invalid input. Please enter a number.{RESET}")

def delete_entry(config):
    """Unmark an entry or wipe progress."""
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    theme = get_theme(config)
    print(f"\n{BOLD}{theme['primary']}Modify / Reset Options:{RESET}")
    print(f"  {theme['accent']}[1]{RESET} Unmark a specific ID")
    print(f"  {theme['accent']}[2]{RESET} Reset ENTIRE tracker")
    choice = input(f"\n{BOLD}Select Option: {RESET}")

    if choice == '1':
        try:
            house_id = int(input(f"Enter ID to unmark (1-{len(data)}): "))
            if 1 <= house_id <= len(data):
                data[house_id - 1]["saved"] = False
                with open(DATA_FILE, 'w') as f:
                    json.dump(data, f, indent=4)
                print(f"{theme['success']}ID {house_id} reset to unsaved.{RESET}")
            else:
                print(f"{theme['pending']}Invalid ID.{RESET}")
        except ValueError:
            print(f"{theme['pending']}Invalid input.{RESET}")
    elif choice == '2':
        confirm = input(f"{theme['pending']}Are you sure you want to delete ALL progress? (y/N): {RESET}")
        if confirm.lower() == 'y':
            for house in data:
                house["saved"] = False
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"{theme['success']}All progress wiped.{RESET}")

def switch_theme(config):
    """Theme picker menu."""
    print(f"\n{BOLD}Available Color Themes:{RESET}")
    for idx, t in enumerate(THEMES):
        current_tag = f" {BOLD}(Active){RESET}" if idx == config["theme_index"] else ""
        print(f"  [{idx + 1}] {t['primary']}{t['name']}{RESET}{current_tag}")
    
    try:
        sel = int(input(f"\n{BOLD}Select Theme Number: {RESET}")) - 1
        if 0 <= sel < len(THEMES):
            config["theme_index"] = sel
            save_config(config)
            print(f"{THEMES[sel]['success']}Theme updated to {THEMES[sel]['name']}!{RESET}")
        else:
            print(f"{THEMES[config['theme_index']]['pending']}Invalid selection.{RESET}")
    except ValueError:
        print("Invalid input.")

def switch_currency(config):
    """Cycle currency setting."""
    config["currency_index"] = (config["currency_index"] + 1) % len(CURRENCIES)
    save_config(config)
    theme = get_theme(config)
    new_curr = CURRENCIES[config["currency_index"]]
    print(f"\n{theme['success']}Currency switched to {new_curr['name']} ({new_curr['symbol']}){RESET}")

def show_summary(data=None, sym="$", config=None):
    """Display financial overview."""
    if not data:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            
    theme = get_theme(config) if config else THEMES[0]
    total_goal = sum(item["amount"] for item in data)
    total_saved = sum(item["amount"] for item in data if item["saved"])
    remaining = total_goal - total_saved
    completed_tiles = sum(1 for item in data if item["saved"])

    print(f"\n{theme['muted']}=================== STATS SUMMARY ==================={RESET}")
    print(f"{BOLD}Total Saved:{RESET} {theme['success']}{sym}{total_saved:,}{RESET} / {theme['text']}{sym}{total_goal:,}{RESET}")
    print(f"{BOLD}Remaining  :{RESET} {theme['pending']}{sym}{remaining:,}{RESET}")
    print(f"{BOLD}Tiles Done :{RESET} {theme['accent']}{completed_tiles}{RESET} of {len(data)} completed")
    print(f"{theme['muted']}====================================================={RESET}")

# ==========================================
# MAIN INTERACTIVE LOOP
# ==========================================

def main():
    create_database()
    config = load_config()

    while True:
        theme = get_theme(config)
        curr_name = CURRENCIES[config["currency_index"]]["name"]
        
        clear_screen()
        print_arch_header(config)
        
        print(f"\n{BOLD}{theme['primary']}MENU OPTIONS:{RESET}")
        print(f"  {theme['accent']}[1]{RESET} View Progress Grid")
        print(f"  {theme['accent']}[2]{RESET} Mark Tile as Saved")
        print(f"  {theme['accent']}[3]{RESET} View Financial Summary")
        print(f"  {theme['accent']}[4]{RESET} Unmark Tile / Reset All")
        print(f"  {theme['accent']}[5]{RESET} Change Currency {theme['muted']}(Active: {curr_name}){RESET}")
        print(f"  {theme['accent']}[6]{RESET} Change Color Theme {theme['muted']}(Active: {theme['name']}){RESET}")
        print(f"  {theme['accent']}[7]{RESET} Exit")
        
        prompt_str = f"\n{BOLD}{theme['primary']}[user@arch-savings ~]$ {RESET}"
        choice = input(prompt_str).strip()

        if choice == '1':
            read_progress(config)
            input(f"\n{theme['muted']}Press Enter to return to menu...{RESET}")
        elif choice == '2':
            update_entry(config)
            input(f"\n{theme['muted']}Press Enter to return to menu...{RESET}")
        elif choice == '3':
            sym = CURRENCIES[config["currency_index"]]["symbol"]
            show_summary(sym=sym, config=config)
            input(f"\n{theme['muted']}Press Enter to return to menu...{RESET}")
        elif choice == '4':
            delete_entry(config)
            input(f"\n{theme['muted']}Press Enter to return to menu...{RESET}")
        elif choice == '5':
            switch_currency(config)
            input(f"\n{theme['muted']}Press Enter to return to menu...{RESET}")
        elif choice == '6':
            switch_theme(config)
            input(f"\n{theme['muted']}Press Enter to return to menu...{RESET}")
        elif choice == '7':
            print(f"\n{theme['success']}Keep saving! Bye!{RESET}\n")
            sys.exit(0)

if __name__ == "__main__":
    main()