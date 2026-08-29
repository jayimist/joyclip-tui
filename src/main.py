import sys, json, sys, tty, termios
from board import Board

VERSION = "0.1.1-alpha"
BLOATED_HEADER = False
args = sys.argv
program_state = "main"
board = Board()



# Helpers
def clear():
    print("\033[H\033[2J", end="")

def print_header(more_info: bool=False):
    print(f'''JoyClip-TUI • jayimist@github • v{VERSION}
A generic Joyful Clipboard TUI program. (You may find bugs n' stuff in this.)
''')
    if BLOATED_HEADER and not more_info:
        print('''How to use the TUI:
  [Q] Copy [W] Up   [E] Delete [Ctrl+C] Exit
  [A] Add  [S] Down [D] Search (SEMI-IMPLEMENTED BUGGY!)
''')
    elif more_info:
        print('''CLI arguments:
  • help / h - Shows more info of JoyClip-TUI
  • version / v - Shows the version of JoyClip-TUI

How to use the TUI:
  • You are in a list of text clips, navigate with the pointer and interact with a clip. Copy, delete, add, search for clips.
  • Controls
    • W - Move the pointer up.
    • S - Move the pointer down.
    • Q - Copies a clip.
    • A - Adds a clip manually.
    • E - Deletes clip.
    • D - Searches for a clip. (SEMI-IMPLEMENTED BUGGY!)
    • Ctrl+C - Exits the program.
  • In search mode to clear searching go into the search bar and press enter to default to all clips shown.
''')

def print_board():
    print("Board - No action. (Action status not fully implemented.)")

    for i, clip_index in enumerate(board.visibleclips):
        text = board.clips[clip_index]

        if i == board.visiblepointer:
            print(f" >  {text}")
            continue

        print(f" - {text}")

def print_version():
    print(f"JoyClip-TUI • jayimist@github • v{VERSION}")

def getkey():
    fd = sys.stdin.fileno()
    old_stgs = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_stgs)




# CLI
if len(args) > 1:
    if args[1] in ("help", "h"):
        print_header(True)
        exit(0)
    if args[1] in ("version", "v"):
        print_version()
        exit(0)



# Main interface
while program_state:
    clear()
    print_header()

    if program_state == "main":
        print_board()
        key = getkey()

        if key == "w":
            board.move(1)
        elif key == "s":
            board.move(-1)
        elif key == "q":
            board.copy()
        elif key == "a":
            program_state = "adding"
        elif key == "e":
            board.delete()
        elif key == "d":
            program_state = "searching"
        elif key == "\x03": # ctrl+c
            program_state = False

        continue

    elif program_state == "adding":
        text = input("Board - Add: ")
        board.add(text)

    elif program_state == "searching":
        text = input("Board - Search: ")
        board.search(text)
    else:
        break

    program_state = "main"
