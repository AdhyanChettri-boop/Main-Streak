"""
SALTMERE
A small open world of islands. Walk it. The map only shows where you have been.

Commands: n s e w, look, map, take, talk, inv, help, quit
"""

ROWS = [
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    "~~~~~~~..T..~~~~~~~~~~~~~~~~~~~~",
    "~~~~~~..###..~~~~~~..F..~~~~~~~~",
    "~~~~~..#####..~~~~..FFFF..~~~~~~",
    "~~~~~~..###..~~~~~~..F..~~~~~~~~",
    "~~~~~~~..H..~~~~~~~~..C..~~~~~~~",
    "~~~~~~~~~~..~~~~~~~~~~..~~~~~~~~",
    "~~~~~~~~~~..~~..RR..~~~~..~~~~~~",
    "~~~~~~~~~..~~~~..R..~~~~~~..W~~~",
    "~~~~~~~~..~~~~~~....~~~~~~~~..~~",
    "~~~~~~~..S..~~~~~~~~~~~~~~..~~~~",
    "~~~~~~~~....~~~~~~~~~~~~~~..~~~~",
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
]

LEGEND = {
    "~": "open water",
    ".": "a wet path",
    "#": "black rock",
    "T": "the town of Saltmere",
    "H": "the harbor",
    "F": "pine wood",
    "C": "a sea cave",
    "R": "ruined cloister",
    "W": "the north watch",
    "S": "the drowned shrine",
}

BLOCKED = set("#~")
START = (10, 7)

ITEMS = {
    (8, 2): "brass bell",
    (22, 8): "iron bell",
    (10, 10): "glass bell",
}

NOTES = {
    "T": "Nets dry on lines. A clerk says the three tide-bells have walked off again.",
    "H": "Boats knock together. The harbormaster will pay if all three bells are returned.",
    "F": "The pines tick. Something small was dragged toward the cave.",
    "C": "The cave breathes cold air. A bell-note hangs in it, then stops.",
    "R": "Monks left in a flood year. Their well still tastes like coins.",
    "W": "From here the whole chain of islands is a gray comb in the water.",
    "S": "The shrine is knee-deep. Offerings are shells, all turned the same way.",
}


def in_bounds(x, y):
    return 0 <= y < len(ROWS) and 0 <= x < len(ROWS[0])


def tile(x, y):
    return ROWS[y][x]


class World:
    def __init__(self):
        self.x, self.y = START
        self.items = dict(ITEMS)
        self.bag = []
        self.seen = set()
        self.reveal()

    def reveal(self):
        for dy in range(-2, 3):
            for dx in range(-3, 4):
                nx, ny = self.x + dx, self.y + dy
                if in_bounds(nx, ny):
                    self.seen.add((nx, ny))

    def here(self):
        return tile(self.x, self.y)

    def move(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if not in_bounds(nx, ny):
            return "The chart ends there."
        if tile(nx, ny) in BLOCKED:
            kind = "water" if tile(nx, ny) == "~" else "rock"
            return f"You cannot walk through {kind}."
        self.x, self.y = nx, ny
        self.reveal()
        return self.describe()

    def describe(self):
        here = self.here()
        lines = [f"You are on {LEGEND.get(here, 'somewhere unnamed')}."]
        if here in NOTES:
            lines.append(NOTES[here])
        for (ix, iy), name in self.items.items():
            if (ix, iy) == (self.x, self.y):
                lines.append(f"On the ground: {name}.")
        near = []
        for dx, dy, word in ((0, -1, "north"), (0, 1, "south"), (-1, 0, "west"), (1, 0, "east")):
            nx, ny = self.x + dx, self.y + dy
            if in_bounds(nx, ny) and tile(nx, ny) not in BLOCKED:
                near.append(word)
        if near:
            lines.append("Paths lead " + ", ".join(near) + ".")
        return "\n".join(lines)

    def draw_map(self):
        lines = ["  SALTMERE", ""]
        for y, row in enumerate(ROWS):
            drawn = []
            for x, ch in enumerate(row):
                if (x, y) == (self.x, self.y):
                    drawn.append("@")
                elif (x, y) not in self.seen:
                    drawn.append(" ")
                else:
                    drawn.append(ch)
            lines.append("  " + "".join(drawn))
        lines.append("")
        lines.append("  @ you   . path   # rock   ~ water")
        lines.append("  T town  H harbor  F wood  C cave  R ruin  W watch  S shrine")
        return "\n".join(lines)

    def take(self):
        key = (self.x, self.y)
        if key not in self.items:
            return "There is nothing here to take."
        name = self.items.pop(key)
        self.bag.append(name)
        extra = "\nAll three bells. The harbor will want them." if self.bells() == 3 else ""
        return f"You take the {name}.{extra}"

    def bells(self):
        return sum(1 for name in self.bag if name.endswith("bell"))

    def talk(self):
        here = self.here()
        if here == "H":
            if self.bells() == 3:
                return (
                    "The harbormaster weighs the three bells and nods once.\n"
                    "\"Tide can have the rest. These stay.\"\n"
                    "He pays you in salt and a berth for the winter.\n"
                    "\n--- The chain is quiet. ---"
                )
            return "\"Three bells,\" the harbormaster says. \"Town, ruin, shrine. Don't swim.\""
        if here == "T":
            return "A child tells you the glass one sings only when it is carried, not when it is hung."
        if here == "W":
            return "The watcher points south-west. \"Shrine's drowning. Bell's still dry, somehow.\""
        if here == "S":
            return "No priest. The water ticks against the step like a patient clock."
        if here == "R":
            return "Graffiti in charcoal: WE RANG IT AND THE FOG CAME IN."
        if here == "C":
            return "If anyone lived here, they left. The dark does not answer."
        return "No one is here to talk to."


HELP = """
  n s e w   move
  look      describe where you are
  map       show the chart (blank until you have been nearby)
  take      pick up what is here
  talk      speak to whoever is around
  inv       what you carry
  help      this list
  quit      stop
"""


def main():
    world = World()
    print("\n  SALTMERE")
    print("  a chain of islands, and a map that starts blank")
    print("  Type help if you need the commands.\n")
    print(world.describe())
    print()

    while True:
        try:
            command = input("> ").strip().lower()
        except EOFError:
            print()
            break
        if command in ("quit", "q", "exit"):
            print("The tide goes on without you.")
            break
        elif command in ("n", "north"):
            print(world.move(0, -1))
        elif command in ("s", "south"):
            print(world.move(0, 1))
        elif command in ("e", "east"):
            print(world.move(1, 0))
        elif command in ("w", "west"):
            print(world.move(-1, 0))
        elif command in ("look", "l"):
            print(world.describe())
        elif command == "map":
            print(world.draw_map())
        elif command == "take":
            print(world.take())
        elif command == "talk":
            said = world.talk()
            print(said)
            if said.startswith("The harbormaster weighs"):
                break
        elif command in ("inv", "i", "inventory"):
            print("You carry: " + ", ".join(world.bag) + "." if world.bag else "You carry nothing.")
        elif command in ("help", "?"):
            print(HELP)
        elif command == "":
            continue
        else:
            print("Unknown command. Type help.")
        print()


if __name__ == "__main__":
    main()
