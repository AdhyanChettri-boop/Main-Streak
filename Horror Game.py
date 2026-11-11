import random
import sys
import os

# simple colour stuff - turn off if it looks weird in your terminal
USE_COLOR = True

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\n[Press Enter]")

def color(text, code):
    if not USE_COLOR:
        return text
    return f"\033[{code}m{text}\033[0m"

RED = "91"
GREEN = "92"
YELLOW = "93"
CYAN = "96"
MAGENTA = "95"
BOLD = "1"

def sep():
    print(color("─" * 42, CYAN))

def get_input(prompt, valid=None, lower=True):
    while True:
        raw = input(prompt).strip()
        if lower:
            raw = raw.lower()
        if valid is None or raw in valid or raw == "":
            return raw
        print(color("Invalid choice.", RED))


# ITEMS

ITEMS = {
    "Knife": {
        "damage": (8, 15),
        "crit": 20,
        "size": 1,
        "type": "weapon",
        "desc": "A rusted kitchen knife. Still sharp enough."
    },
    "Axe": {
        "damage": (15, 25),
        "crit": 10,
        "size": 2,
        "type": "weapon",
        "desc": "Heavy. Slow. Devastating."
    },
    "Revolver": {
        "damage": (20, 35),
        "crit": 25,
        "size": 2,
        "type": "weapon",
        "desc": "Three rounds left. Make them count."
    },
    "Rusty Pipe": {
        "damage": (10, 18),
        "crit": 15,
        "size": 2,
        "type": "weapon",
        "desc": "Clogged with something dark."
    },
    "Bone Saw": {
        "damage": (18, 28),
        "crit": 30,
        "size": 2,
        "type": "weapon",
        "desc": "Surgical. Precise. Wrong."
    },
    "Cursed Doll": {
        "damage": (25, 40),
        "crit": 35,
        "size": 1,
        "type": "weapon",
        "desc": "It whispers your name. High damage, but it drains you.",
        "cursed": True
    },
    "Medkit": {
        "heal": 30,
        "size": 1,
        "type": "heal",
        "desc": "Military surplus. Still sealed."
    },
    "Bandages": {
        "heal": 15,
        "size": 1,
        "type": "heal",
        "desc": "Better than nothing."
    },
    "Adrenaline": {
        "heal": 40,
        "size": 1,
        "type": "heal",
        "desc": "Burns going in. Keeps you moving."
    }
}


# ENEMIES

ENTITIES = {
    "Whispering Widow": {
        "health": 60,
        "damage": (8, 14),
        "intro": "A woman in a torn wedding dress steps from the fog. Her mouth never stops moving.",
        "flavor": [
            "She tilts her head too far.",
            "The whispers grow louder.",
            "She reaches for you."
        ]
    },
    "Crooked Child": {
        "health": 50,
        "damage": (6, 12),
        "intro": "Something small crawls out from under the stairs. Its limbs bend the wrong way.",
        "flavor": [
            "It giggles.",
            "Bones crack as it moves.",
            "It stares without blinking."
        ]
    },
    # boss gets special treatment later
    "The Smiling Man": {
        "health": 140,
        "damage": (14, 22),
        "intro": "A tall figure in a stained suit is already waiting. Its smile is far too wide.",
        "flavor": [
            "The smile never changes.",
            "It takes a single step closer.",
            "You hear wet breathing."
        ]
    }
}

AREA_FLAVOR = {
    "forest": [
        "The trees lean inward.",
        "Something moves just beyond the fog.",
        "You hear distant crying that stops when you listen.",
        "Roots look like fingers.",
        "The air smells of wet earth and old blood."
    ],
    "house": [
        "Wallpaper peels in long strips.",
        "A door somewhere slams shut.",
        "Footsteps echo from above, then stop.",
        "The lights flicker once.",
        "You smell mildew and something sweet."
    ],
    "asylum": [
        "Restraints hang from the walls.",
        "A wheelchair sits empty in the middle of the hall.",
        "Scratch marks cover the doorframes.",
        "You hear a gurney rolling somewhere far away.",
        "The air is thick with antiseptic and rot."
    ]
}


# PLAYER

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.weapon = None
        self.max_slots = 5
        self.run_fails = 0
        self.areas_cleared = set()
        self.kills = 0
        self.medkits_used = 0
        self.damage_taken = 0

    def used_slots(self):
        total = 0
        for item in self.inventory:
            total += ITEMS[item]["size"]
        return total

    def free_slots(self):
        return self.max_slots - self.used_slots()

    def show_status(self):
        sep()
        print(color(f" {self.name}", BOLD))
        hp_col = GREEN if self.health > 40 else RED
        print(f" HP: {color(str(self.health), hp_col)}/{self.max_health}")
        print(f" Weapon: {self.weapon or 'Fists'}")
        print(f"Slots: {self.used_slots()}/{self.max_slots}")
        print(f" Areas cleared: {len(self.areas_cleared)}/3")
        sep()

    def show_inventory(self):
        sep()
        print(color(f" {self.name}'s INVENTORY", BOLD))
        if not self.inventory:
            print("  (empty)")
        else:
            for i, item in enumerate(self.inventory, 1):
                mark = " *" if item == self.weapon else ""
                print(f"  {i}) {item}{mark}  [{ITEMS[item]['size']} slot]")
        print(f"\n Free slots: {self.free_slots()}")
        if self.weapon:
            print(f" Equipped: {self.weapon}")
        sep()

    def add_item(self, item_name):
        size = ITEMS[item_name]["size"]
        if self.used_slots() + size > self.max_slots:
            print(color("\nInventory full.", YELLOW))
            if get_input("Drop something first? (y/n): ", {"y", "n"}) == "y":
                self.drop_item()
                if self.used_slots() + size > self.max_slots:
                    print("Still not enough space.")
                    return False
            else:
                print("You leave it behind.")
                return False

        self.inventory.append(item_name)
        print(color(f"{self.name} picked up {item_name}.", GREEN))
        print(f"  {ITEMS[item_name]['desc']}")

        if ITEMS[item_name]["type"] == "weapon":
            if get_input("Equip it now? (y/n): ", {"y", "n"}) == "y":
                self.weapon = item_name
                print(f"{self.name} equipped the {item_name}.")
                if ITEMS[item_name].get("cursed"):
                    self.max_health = max(60, self.max_health - 15)
                    if self.health > self.max_health:
                        self.health = self.max_health
                    print(color("The doll tightens its grip. Max HP drops.", MAGENTA))
        return True

    def drop_item(self):
        self.show_inventory()
        if not self.inventory:
            return
        try:
            choice = int(get_input("Drop which number? (0 to cancel): ")) - 1
            if choice < 0:
                return
            removed = self.inventory.pop(choice)
            print(f"{self.name} dropped the {removed}.")
            if self.weapon == removed:
                self.weapon = None
                print("Weapon unequipped.")
        except (ValueError, IndexError):
            print("Invalid choice.")

    def equip_weapon(self):
        weapons = [i for i in self.inventory if ITEMS[i]["type"] == "weapon"]
        if not weapons:
            print("No weapons.")
            return
        print("\nWeapons:")
        for i, w in enumerate(weapons, 1):
            print(f"  {i}) {w}")
        try:
            choice = int(get_input("Equip which? (0 to cancel): ")) - 1
            if choice < 0:
                return
            self.weapon = weapons[choice]
            print(f"{self.name} equipped the {self.weapon}.")
            if ITEMS[self.weapon].get("cursed"):
                self.max_health = max(60, self.max_health - 15)
                if self.health > self.max_health:
                    self.health = self.max_health
                print(color("The curse settles deeper.", MAGENTA))
        except (ValueError, IndexError):
            print("Invalid choice.")

    def use_heal(self):
        heals = [i for i in self.inventory if ITEMS[i]["type"] == "heal"]
        if not heals:
            print("No healing items.")
            return
        print("\nHealing items:")
        for i, h in enumerate(heals, 1):
            print(f"  {i}) {h} (+{ITEMS[h]['heal']} HP)")
        try:
            choice = int(get_input("Use which? (0 to cancel): ")) - 1
            if choice < 0:
                return
            item = heals[choice]
            amount = ITEMS[item]["heal"]
            self.health = min(self.max_health, self.health + amount)
            self.inventory.remove(item)
            self.medkits_used += 1
            print(color(f"{self.name} used the {item}. HP now {self.health}.", GREEN))
        except (ValueError, IndexError):
            print("Invalid choice.")


# NORMAL COMBAT

def player_attack(player, enemy_name, enemy_hp):
    if player.weapon is None:
        dmg = random.randint(3, 7)
        print(f"\n{player.name} strikes with bare fists.")
    else:
        data = ITEMS[player.weapon]
        dmg = random.randint(data["damage"][0], data["damage"][1])
        if random.randint(1, 100) <= data["crit"]:
            dmg *= 2
            print(color("\nCRITICAL HIT!", YELLOW))
        print(f"\n{player.name} attacks with the {player.weapon}.")

    enemy_hp -= dmg
    print(f"{player.name} deals {color(str(dmg), YELLOW)} damage.")
    return max(0, enemy_hp)


def enemy_attack(player, enemy_name):
    data = ENTITIES[enemy_name]
    dmg = random.randint(data["damage"][0], data["damage"][1])
    player.health -= dmg
    player.damage_taken += dmg
    print(f"\n{enemy_name} attacks {player.name}.")
    print(random.choice(data["flavor"]))
    print(f"{player.name} takes {color(str(dmg), RED)} damage. HP: {player.health}")


def fight(player, enemy_name):
    # normal enemies go through here
    if enemy_name == "The Smiling Man":
        return boss_fight(player)

    enemy = ENTITIES[enemy_name]
    enemy_hp = enemy["health"]
    print(color(f"\n{enemy['intro']}", MAGENTA))
    pause()

    while enemy_hp > 0 and player.health > 0:
        sep()
        hp_col = GREEN if player.health > 40 else RED
        print(f" {player.name}'s HP: {color(str(player.health), hp_col)}")
        print(f" {enemy_name.upper()} HP: {enemy_hp}")
        sep()
        print(" [F]ight  [R]un  [I]nventory  [H]eal  [E]quip  [S]tatus")

        action = get_input("> ", {"f", "fight", "r", "run", "i", "inventory",
                                  "h", "heal", "e", "equip", "s", "status", ""})

        if action in ("f", "fight", ""):
            enemy_hp = player_attack(player, enemy_name, enemy_hp)
            if enemy_hp <= 0:
                print(color(f"\n{player.name} killed the {enemy_name}.", GREEN))
                player.kills += 1
                if random.random() < 0.6:
                    reward = random.choice(["Bandages", "Medkit", "Knife"])
                    print(f"{player.name} finds a {reward} on the body.")
                    player.add_item(reward)
                player.run_fails = 0
                return True

            enemy_attack(player, enemy_name)

        elif action in ("r", "run"):
            chance = max(25, 55 - player.run_fails * 15)
            if random.randint(1, 100) <= chance:
                print(color(f"\n{player.name} escapes into the dark.", GREEN))
                player.run_fails = 0
                return False
            else:
                print(color(f"\n{player.name} fails to get away.", RED))
                player.run_fails += 1
                enemy_attack(player, enemy_name)

        elif action in ("i", "inventory"):
            player.show_inventory()
        elif action in ("h", "heal"):
            player.use_heal()
        elif action in ("e", "equip"):
            player.equip_weapon()
        elif action in ("s", "status"):
            player.show_status()

        if player.health <= 0:
            print(color(f"\n{player.name} collapses. The last thing they see is the smile.", RED))
            print("GAME OVER")
            show_score(player, survived=False)
            sys.exit()

    return True


# BOSS FIGHT - The Smiling Man

def boss_fight(player):
    boss_name = "The Smiling Man"
    boss_hp = 140
    phase = 1

    print(color("\nThe lights die for a second.", MAGENTA))
    print(f"When they come back, The Smiling Man is already standing in front of {player.name}.")
    print(f'"Hello, {player.name}," it says without moving its mouth.')
    print("The smile just stretches a little wider.")
    pause()

    while boss_hp > 0 and player.health > 0:
        sep()
        hp_col = GREEN if player.health > 40 else RED
        print(f" {player.name}'s HP: {color(str(player.health), hp_col)}")
        print(f" THE SMILING MAN  HP: {boss_hp}")
        if phase == 2:
            print(color("  (ENRAGED)", RED))
        sep()
        print(" [F]ight  [R]un  [I]nventory  [H]eal  [E]quip  [S]tatus")

        action = get_input("> ", {"f", "fight", "r", "run", "i", "inventory",
                                  "h", "heal", "e", "equip", "s", "status", ""})

        if action in ("f", "fight", ""):
            # player turn
            if player.weapon is None:
                dmg = random.randint(3, 7)
                print(f"\n{player.name} hits it with bare fists. It barely notices.")
            else:
                data = ITEMS[player.weapon]
                dmg = random.randint(data["damage"][0], data["damage"][1])
                if random.randint(1, 100) <= data["crit"]:
                    dmg *= 2
                    print(color("\nCRITICAL HIT!", YELLOW))
                print(f"\n{player.name} swings the {player.weapon}.")

            boss_hp -= dmg
            print(f"{player.name} deals {color(str(dmg), YELLOW)} damage.")

            if boss_hp <= 0:
                break

            # phase change
            if phase == 1 and boss_hp <= 70:
                phase = 2
                print(color("\nThe Smiling Man stops moving.", MAGENTA))
                print(f'"You are taking too long, {player.name}."')
                print("Its neck cracks as the head tilts further than it should.")
                print(color("It is done playing.", RED))
                pause()

            # boss attack
            if phase == 1:
                # normal hits + occasional special
                if random.random() < 0.25:
                    print(f'\n"Look at me, {player.name}."')
                    print("The smile fills your vision for a moment.")
                    dmg = random.randint(18, 26)
                    player.health -= dmg
                    player.damage_taken += dmg
                    print(f"{player.name} reels. {color(str(dmg), RED)} damage. HP: {player.health}")
                else:
                    dmg = random.randint(14, 22)
                    player.health -= dmg
                    player.damage_taken += dmg
                    print(f"\nThe Smiling Man strikes {player.name}.")
                    print(random.choice(ENTITIES[boss_name]["flavor"]))
                    print(f"{player.name} takes {color(str(dmg), RED)} damage. HP: {player.health}")
            else:
                # phase 2 - meaner
                roll = random.random()
                if roll < 0.35:
                    print(f'\n"Stay still, {player.name}."')
                    print("It moves faster than anything that size should.")
                    dmg = random.randint(22, 32)
                    player.health -= dmg
                    player.damage_taken += dmg
                    print(f"Heavy hit. {color(str(dmg), RED)} damage. HP: {player.health}")
                elif roll < 0.55:
                    print(f'\n"I already know how this ends, {player.name}."')
                    print("A cold weight settles in your chest.")
                    # small max hp drain
                    drain = random.randint(4, 8)
                    player.max_health = max(50, player.max_health - drain)
                    if player.health > player.max_health:
                        player.health = player.max_health
                    print(color(f"Max HP reduced by {drain}.", MAGENTA))
                    print(f"Current HP: {player.health}/{player.max_health}")
                else:
                    dmg = random.randint(16, 24)
                    player.health -= dmg
                    player.damage_taken += dmg
                    print(f"\nThe Smiling Man lashes out at {player.name}.")
                    print(f"{player.name} takes {color(str(dmg), RED)} damage. HP: {player.health}")

        elif action in ("r", "run"):
            # boss is not easy to run from
            print(color(f"\n{player.name} tries to run.", YELLOW))
            if random.randint(1, 100) <= 15:
                print(color("Somehow, it works. You slam a door behind you and keep moving.", GREEN))
                return False
            else:
                print(f'The Smiling Man is already in front of {player.name} again.')
                print(f'"Running only makes it more fun."')
                dmg = random.randint(20, 28)
                player.health -= dmg
                player.damage_taken += dmg
                print(f"{player.name} takes {color(str(dmg), RED)} damage for the attempt. HP: {player.health}")

        elif action in ("i", "inventory"):
            player.show_inventory()
        elif action in ("h", "heal"):
            player.use_heal()
        elif action in ("e", "equip"):
            player.equip_weapon()
        elif action in ("s", "status"):
            player.show_status()

        if player.health <= 0:
            print(color(f"\n{player.name} falls.", RED))
            print(f'The last thing they hear is a soft voice:')
            print(f'"I told you I already knew, {player.name}."')
            print("GAME OVER")
            show_score(player, survived=False)
            sys.exit()

    # boss dead
    print(color(f"\nThe Smiling Man finally stops smiling.", GREEN))
    print(f"{player.name} stands over what is left of it.")
    print("For a second the corridors feel almost normal.")
    player.kills += 1

    # boss drop
    print(f"\nSomething cold is left behind.")
    if get_input("Take the Cursed Doll? (y/n): ", {"y", "n"}) == "y":
        player.add_item("Cursed Doll")
    else:
        print(f"{player.name} leaves it where it lies.")

    return True


# AREAS

def explore_area(player, area_name, enemy_name, steps=5):
    path = []
    monster_step = random.randint(1, steps - 1)

    print(color(f"\n{player.name} enters the {area_name}.", CYAN))
    if area_name == "forest":
        print("The fog closes behind them.")
    elif area_name == "house":
        print("The front door locks with a heavy click.")
    else:
        print("The gates seal shut. There is no going back the way they came.")

    for step in range(steps):
        print(f"\n--- {area_name.title()}  ·  Step {step + 1}/{steps} ---")
        print(random.choice(AREA_FLAVOR[area_name]))

        while True:
            choice = get_input(
                "Direction (left/right/forward) or [I]nventory / [S]tatus: ",
                {"left", "right", "forward", "l", "r", "f", "i", "inventory", "s", "status"}
            )
            if choice in ("i", "inventory"):
                player.show_inventory()
            elif choice in ("s", "status"):
                player.show_status()
            else:
                mapping = {"l": "left", "r": "right", "f": "forward"}
                choice = mapping.get(choice, choice)
                path.append(choice)
                break

        # random stuff on the ground
        roll = random.randint(1, 100)
        if roll <= 35:
            found = random.choice(list(ITEMS.keys()))
            print(f"\n{player.name} notices something on the ground: {found}")
            if get_input("Take it? (y/n): ", {"y", "n"}) == "y":
                player.add_item(found)
        elif roll <= 50:
            print(color("\nNothing but silence.", CYAN))

        if step == monster_step:
            print(color("\nSomething is here...", MAGENTA))
            fought = fight(player, enemy_name)
            if not fought:
                print(f"{player.name} slipped past it, but the path still waits.")

    print(color(f"\n{player.name} reaches the far side of the {area_name}.", GREEN))
    print("Now they must go back the way they came.")
    print(color("Remember: reverse the path. Left becomes right, right becomes left. Forward stays forward.", YELLOW))
    pause()

    return_path(player, path, area_name)
    player.areas_cleared.add(area_name)
    print(color(f"\n{player.name} escaped the {area_name}.", GREEN))
    return True


def return_path(player, original_path, area_name):
    needed = []
    for d in reversed(original_path):
        if d == "left":
            needed.append("right")
        elif d == "right":
            needed.append("left")
        else:
            needed.append("forward")

    print(color(f"\nThe {area_name} begins to shift around {player.name}...", MAGENTA))

    for i, correct in enumerate(needed, 1):
        print(f"\nReturn step {i}/{len(needed)}")
        answer = get_input("Which way? (left/right/forward): ",
                           {"left", "right", "forward", "l", "r", "f"})
        mapping = {"l": "left", "r": "right", "f": "forward"}
        answer = mapping.get(answer, answer)

        if answer != correct:
            print(color("\nWrong turn.", RED))
            if area_name == "forest":
                print(f"The trees close in. {player.name} is never seen again.")
            elif area_name == "house":
                print(f"{player.name} opens the wrong door. Something inside is already smiling.")
            else:
                print(f"The corridor folds. {player.name} becomes part of the walls.")
            print("GAME OVER")
            show_score(player, survived=False)
            sys.exit()

        print(color("Correct.", GREEN))


# HUB + ENDING

def show_score(player, survived=True):
    sep()
    print(color(" FINAL RECORD", BOLD))
    print(f" Name:          {player.name}")
    print(f" Survived:      {'Yes' if survived else 'No'}")
    print(f" Areas cleared: {len(player.areas_cleared)}/3")
    print(f" Kills:         {player.kills}")
    print(f" Healing used:  {player.medkits_used}")
    print(f" Damage taken:  {player.damage_taken}")
    score = (len(player.areas_cleared) * 100) + (player.kills * 40) + player.health - (player.damage_taken // 2)
    print(f" Score:         {max(0, score)}")
    sep()


def epilogue(player):
    print("\n...")
    if len(player.areas_cleared) == 3:
        print(f"{player.name} walked out of the nightmare.")
        if player.weapon and ITEMS.get(player.weapon, {}).get("cursed"):
            print(f"But the doll is still in {player.name}'s pocket. And it is still whispering.")
        elif player.health > 70:
            print(f"{player.name} barely looks back. Some people are just harder to break.")
        else:
            print(f"{player.name} will never sleep the same way again. But they are alive.")
    else:
        print(f"{player.name} found a way out, but the places they left behind are still waiting.")
    print()
    print(color(f"{player.name} survived the nightmare...", GREEN))


def hub(player):
    while True:
        clear()
        player.show_status()
        print(color(f" Where does {player.name} go?", BOLD))
        print("  1) Forest")
        print("  2) House")
        if len(player.areas_cleared) >= 2:
            print("  3) Asylum  (final)")
        print("  4) Inventory / Status")
        print("  5) Leave (end game)")

        choice = get_input("\nChoice: ", {"1", "2", "3", "4", "5"})

        if choice == "1":
            if "forest" in player.areas_cleared:
                print(f"{player.name} already escaped the forest.")
                pause()
                continue
            explore_area(player, "forest", "Whispering Widow")
            pause()
        elif choice == "2":
            if "house" in player.areas_cleared:
                print(f"{player.name} already escaped the house.")
                pause()
                continue
            explore_area(player, "house", "Crooked Child")
            pause()
        elif choice == "3":
            if len(player.areas_cleared) < 2:
                print(f"{player.name} is not ready.")
                pause()
                continue
            if "asylum" in player.areas_cleared:
                print("There is nothing left there.")
                pause()
                continue
            explore_area(player, "asylum", "The Smiling Man", steps=6)
            pause()
        elif choice == "4":
            player.show_inventory()
            player.show_status()
            pause()
        elif choice == "5":
            break

    epilogue(player)
    show_score(player, survived=True)


# START

def main():
    clear()
    print(color("══════════════════════════════", CYAN))
    print(color("     THE NIGHTMARE", BOLD))
    print(color("══════════════════════════════", CYAN))
    print("\nYou wake up between places that should not exist.")
    print("Inventory is limited. The path must be remembered.")
    print("Things are hunting you.\n")

    while True:
        start = get_input("Enter the nightmare? (y/n): ", {"y", "n"})
        if start == "y":
            break
        if start == "n":
            print(color("\nCOWARD.", RED))
            return

    name = input("\nYour name: ").strip() or "Stranger"
    player = Player(name)

    print(color(f"\nWelcome, {player.name}.", CYAN))
    print("Find a way through. Or become part of it.")
    pause()

    hub(player)


if __name__ == "__main__":
    main()
