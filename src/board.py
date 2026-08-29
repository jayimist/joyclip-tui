import json, subprocess as subproc
from pathlib import Path

clipsfile = Path(__file__).parent.parent / "clips.json"



# Helpers
def runproc(args: tuple[str, ...]):
    subproc.Popen(args, stdout=subproc.DEVNULL, stderr=subproc.DEVNULL)



# Main class
class Board:
    def __init__(self):
        self.clips = self.read()
        self.visibleclips = []
        self.pointer = 0 # Pointer to self.clips
        self.visiblepointer = 0 # Pointer to self.visibleclips
        self.searchtext = ""

        self.search()

    def clampointer(self):
        self.visiblepointer = max(0, min(self.visiblepointer, len(self.visibleclips) - 1))

    def write(self):
        with open(clipsfile, "w") as f:
            json.dump(self.clips, f, indent=2)

    def read(self):
        with open(clipsfile, "r") as f:
            return json.load(f)

    def move(self, dir: int):
        if dir > 0:
            self.visiblepointer -= 1
        elif dir < 0:
            self.visiblepointer += 1

        self.clampointer()
        self.pointer = self.visibleclips[self.visiblepointer]

    def copy(self):
        runproc(("wl-copy", self.clips[self.pointer]))

    def add(self, text: str=""):
        if not text: return
        self.clips.insert(0, text)
        self.search(self.searchtext)
        self.move(-1)
        self.write()

    def delete(self):
        self.clips.pop(self.pointer)
        self.search(self.searchtext)
        self.clampointer()
        self.write()

    def search(self, text: str=""):
        self.searchtext = text
        self.visibleclips = []

        for i, clip in enumerate(self.clips):
            if text == "" or text in clip:
                self.visibleclips.append(i)



# Demo
# b = Board()
# b.add("HELLO")
# b.add("WORLD")
# b.move(-1)
# b.delete()
