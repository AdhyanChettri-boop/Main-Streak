MONTHS = [
    "January", "March", "April", "June", "September", "October", "November",
]
WEATHERS = [
    "in hard rain", "under a colorless noon", "during a power cut",
    "while snow sticks to one side of the street only",
    "on a night when dogs will not bark", "just before a market opens",
]
OBJECTS = [
    "a house key", "a paper ticket", "a glove", "a cracked watch",
    "a library card", "a photograph", "a silver coin", "a child's shoe",
]
PLACES = [
    "under a theater seat", "in a borrowed coat", "behind a loose brick",
    "inside a piano", "at the bottom of a ferry stair",
    "in the pocket of a stranger", "beneath a church bench",
]
TURNS = [
    "They will not give it back.",
    "They will pretend they never saw it.",
    "Someone else has been looking for it longer.",
    "The owner will thank them with the wrong name.",
    "It will be warmer than it should be.",
    "A second one, identical, is already in their room.",
]


def seal(name):
    """Turn a name into one stable number. This is the entire trick."""
    n = 0
    for ch in name.strip().lower():
        n = (n * 33 + ord(ch)) % 1_000_003
    return n


def page_for(name):
    n = seal(name)
    page_no = 1000 + (n % 9000)

    def pick(options, shift):
        return options[(n // shift) % len(options)]

    month = pick(MONTHS, 7)
    day = (n % 27) + 1
    weather = pick(WEATHERS, 11)
    obj = pick(OBJECTS, 13)
    place = pick(PLACES, 17)
    turn = pick(TURNS, 19)
    who = name.strip().split()[0].upper()

    return page_no, (
        f"On {month} {day}, {weather}, {who} will find {obj}\n"
        f"{place}.\n"
        f"{turn}\n"
        f"The page was numbered before {who} was born."
    )


def main():
    print()
    print("  ALREADY WRITTEN")
    print("  a book with one page per name")
    print("  --------------------------------")
    print("  The pages do not change. Only the name you bring.")
    print()

    while True:
        name = input("  Name (or quit): ").strip()
        if name.lower() in {"quit", "exit", "q"}:
            print("  The book stays open.\n")
            break
        if not any(ch.isalpha() for ch in name):
            print("  That is not a name the book keeps.\n")
            continue

        number, text = page_for(name)
        print()
        print(f"  --------  PAGE {number}  --------")
        print()
        for line in text.splitlines():
            print(f"  {line}")
        print()
        print("  ------------------------------")
        print("  Ask someone else. Then ask them again tomorrow.")
        print()


if __name__ == "__main__":
    main()
