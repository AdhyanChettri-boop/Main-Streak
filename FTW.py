import random
import time
import os
import json


# ====================== UTILITY ======================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def slow_print(text, delay=0.01):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


# ====================== DATA ======================

ENEMY_TYPES = [
    {'name': 'Goblin', 'hp': 30, 'attack': 5, 'gold': 10, 'xp': 15},
    {'name': 'Skeleton', 'hp': 40, 'attack': 8, 'gold': 18, 'xp': 25},
    {'name': 'Orc', 'hp': 60, 'attack': 12, 'gold': 30, 'xp': 45},
    {'name': 'Shadow Knight', 'hp': 90, 'attack': 18, 'gold': 60, 'xp': 80}
]

ITEMS = {
    'Small Potion': 25,
    'Large Potion': 60,
    'Iron Sword': 120,
    'Steel Armor': 180,
    'Magic Ring': 250
}

LOCATIONS = [
    'Ancient Forest', 'Crystal Cave', 'Dark Dungeon', 'Forgotten Temple',
    'Abandoned Village', 'Frozen Mountain', 'Burning Desert', 'Ruined Castle'
]

QUESTS = [
    'Defeat 3 Goblins',
    'Collect 100 Gold',
    'Reach Level 5',
    'Defeat the Shadow Knight',
    'Survive 10 Battles'
]


# ====================== CLASSES ======================

class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.defense = 5
        self.gold = 50
        self.xp = 0
        self.inventory = []
        self.location = 'Town'
        self.quests = []
        self.quest_progress = {
            'goblin_kills': 0,
            'shadow_knight_kills': 0,
            'battles_survived': 0,
            'gold_earned': 0
        }
        self.kills = 0
        self.steps = 0
        self.owned_equipment = set()  # Prevents buying same equipment multiple times

    def show_stats(self):
        print('\n========== PLAYER STATS ==========')
        print(f'Name      : {self.name}')
        print(f'Level     : {self.level}')
        print(f'HP        : {self.hp}/{self.max_hp}')
        print(f'Attack    : {self.attack}')
        print(f'Defense   : {self.defense}')
        print(f'Gold      : {self.gold}')
        print(f'XP        : {self.xp}/{self.level * 100}')
        print(f'Kills     : {self.kills}')
        print(f'Steps     : {self.steps}')
        print(f'Location  : {self.location}')
        print('==================================')

    def gain_xp(self, amount):
        self.xp += amount
        print(f'+{amount} XP')

        # Support multiple level-ups
        while self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 25
        self.attack += 4
        self.defense += 2
        self.hp = self.max_hp
        print('\n*** LEVEL UP! ***')
        print(f'You are now level {self.level}!')
        self.check_quests()

    def heal(self, amount):
        old_hp = self.hp
        self.hp = min(self.hp + amount, self.max_hp)
        healed = self.hp - old_hp
        print(f'Healed {healed} HP.')

    def take_damage(self, amount):
        reduced = max(1, amount - self.defense)
        self.hp -= reduced
        print(f'{self.name} took {reduced} damage!')

    def add_item(self, item):
        self.inventory.append(item)
        print(f'Added {item} to inventory.')

    def show_inventory(self):
        print('\n========== INVENTORY ==========')
        if not self.inventory:
            print('Inventory is empty.')
        else:
            for i, item in enumerate(self.inventory, start=1):
                print(f'{i}. {item}')
        print('================================')

    def check_quests(self):
        completed = []

        for quest in self.quests[:]:
            if quest == 'Defeat 3 Goblins' and self.quest_progress['goblin_kills'] >= 3:
                completed.append(quest)
                self.gold += 80
                self.gain_xp(40)
                print(f'\n*** QUEST COMPLETE: {quest} ***')
                print('+80 gold')

            elif quest == 'Collect 100 Gold' and self.gold >= 100:
                completed.append(quest)
                self.gold += 50
                self.gain_xp(30)
                print(f'\n*** QUEST COMPLETE: {quest} ***')
                print('+50 gold')

            elif quest == 'Reach Level 5' and self.level >= 5:
                completed.append(quest)
                self.gold += 150
                self.gain_xp(50)
                print(f'\n*** QUEST COMPLETE: {quest} ***')
                print('+150 gold')

            elif quest == 'Defeat the Shadow Knight' and self.quest_progress['shadow_knight_kills'] >= 1:
                completed.append(quest)
                self.gold += 200
                self.gain_xp(100)
                print(f'\n*** QUEST COMPLETE: {quest} ***')
                print('+200 gold')

            elif quest == 'Survive 10 Battles' and self.quest_progress['battles_survived'] >= 10:
                completed.append(quest)
                self.gold += 120
                self.gain_xp(60)
                print(f'\n*** QUEST COMPLETE: {quest} ***')
                print('+120 gold')

        for q in completed:
            self.quests.remove(q)


class Enemy:
    def __init__(self, data):
        self.name = data['name']
        self.hp = data['hp']
        self.attack = data['attack']
        self.gold = data['gold']
        self.xp = data['xp']

    def take_damage(self, amount):
        self.hp -= amount


# ====================== SAVE / LOAD ======================

def save_game(player):
    data = {
        'name': player.name,
        'level': player.level,
        'hp': player.hp,
        'max_hp': player.max_hp,
        'attack': player.attack,
        'defense': player.defense,
        'gold': player.gold,
        'xp': player.xp,
        'inventory': player.inventory,
        'location': player.location,
        'quests': player.quests,
        'quest_progress': player.quest_progress,
        'kills': player.kills,
        'steps': player.steps,
        'owned_equipment': list(player.owned_equipment)
    }
    with open('savegame.json', 'w') as file:
        json.dump(data, file, indent=2)
    print('Game saved successfully.')


def load_game():
    try:
        with open('savegame.json', 'r') as file:
            data = json.load(file)

        player = Player(data['name'])
        player.level = data['level']
        player.hp = data['hp']
        player.max_hp = data['max_hp']
        player.attack = data['attack']
        player.defense = data['defense']
        player.gold = data['gold']
        player.xp = data['xp']
        player.inventory = data['inventory']
        player.location = data['location']
        player.quests = data['quests']
        player.quest_progress = data.get('quest_progress', {
            'goblin_kills': 0,
            'shadow_knight_kills': 0,
            'battles_survived': 0,
            'gold_earned': 0
        })
        player.kills = data['kills']
        player.steps = data['steps']
        player.owned_equipment = set(data.get('owned_equipment', []))

        print('Save loaded successfully.')
        return player
    except FileNotFoundError:
        print('No save file found.')
        return None
    except Exception as e:
        print(f'Failed to load save: {e}')
        return None


# ====================== EXPLORATION & EVENTS ======================

def explore(player):
    clear_screen()
    location = random.choice(LOCATIONS)
    player.location = location
    player.steps += 1
    slow_print(f'You travel to {location}...')

    event = random.randint(1, 5)
    if event == 1:
        find_gold(player)
    elif event == 2:
        battle(player)
    elif event == 3:
        discover_item(player)
    elif event == 4:
        mysterious_event(player)
    else:
        peaceful_event(player)


def find_gold(player):
    amount = random.randint(10, 100)
    player.gold += amount
    player.quest_progress['gold_earned'] += amount
    print(f'You found {amount} gold!')
    player.check_quests()


def discover_item(player):
    item = random.choice(list(ITEMS.keys()))
    player.add_item(item)


def mysterious_event(player):
    print('A mysterious traveler approaches you...')
    outcome = random.randint(1, 3)
    if outcome == 1:
        player.heal(30)
        print('The traveler healed you.')
    elif outcome == 2:
        stolen = min(player.gold, 25)
        player.gold -= stolen
        print(f'The traveler stole {stolen} gold!')
    else:
        player.attack += 1
        print('The traveler trained you. Attack +1!')


def peaceful_event(player):
    print('The area is peaceful today.')
    print('You rest beside a campfire.')
    player.heal(15)


# ====================== COMBAT ======================

def battle(player):
    if player.hp <= 0:
        print('You are too weak to fight...')
        return

    enemy_data = random.choice(ENEMY_TYPES)
    enemy = Enemy(enemy_data)
    print(f'\nA wild {enemy.name} appeared!')

    while enemy.hp > 0 and player.hp > 0:
        print('\n========== BATTLE ==========')
        print(f'{enemy.name} HP: {enemy.hp}')
        print(f'{player.name} HP: {player.hp}/{player.max_hp}')
        print('============================')
        print('1. Attack')
        print('2. Use Potion')
        print('3. Run')

        choice = input('Choose: ').strip()

        if choice == '1':
            damage = player.attack + random.randint(1, 6)
            enemy.take_damage(damage)
            print(f'You dealt {damage} damage!')

        elif choice == '2':
            used = use_potion(player)
            if not used:
                continue  # Don't waste turn if no potion

        elif choice == '3':
            if random.randint(1, 2) == 1:
                print('You escaped successfully.')
                return
            else:
                print('Escape failed!')
        else:
            print('Invalid choice.')
            continue

        if enemy.hp > 0:
            player.take_damage(enemy.attack)

    if player.hp <= 0:
        game_over(player)
    else:
        print(f'\nYou defeated the {enemy.name}!')
        player.gold += enemy.gold
        player.gain_xp(enemy.xp)
        player.kills += 1
        player.quest_progress['battles_survived'] += 1

        if enemy.name == 'Goblin':
            player.quest_progress['goblin_kills'] += 1
        elif enemy.name == 'Shadow Knight':
            player.quest_progress['shadow_knight_kills'] += 1

        print(f'+{enemy.gold} gold')
        player.check_quests()


def use_potion(player):
    potions = []
    if 'Mega Potion' in player.inventory:
        potions.append(('Mega Potion', 100))
    if 'Large Potion' in player.inventory:
        potions.append(('Large Potion', 60))
    if 'Small Potion' in player.inventory:
        potions.append(('Small Potion', 30))

    if not potions:
        print('No potions available.')
        return False

    # Prefer the strongest potion available
    potion_name, heal_amount = potions[0]
    player.inventory.remove(potion_name)
    player.heal(heal_amount)
    print(f'Used {potion_name}.')
    return True


# ====================== SHOP ======================

def shop(player):
    while True:
        print('\n========== SHOP ==========')
        print(f'Gold: {player.gold}')
        print('==========================')

        for i, item in enumerate(ITEMS, start=1):
            owned = ' (Owned)' if item in player.owned_equipment else ''
            print(f'{i}. {item} - {ITEMS[item]} gold{owned}')

        print('0. Exit Shop')
        choice = input('Choose item: ').strip()

        if choice == '0':
            break

        try:
            index = int(choice) - 1
            item_name = list(ITEMS.keys())[index]
            price = ITEMS[item_name]

            # Prevent buying equipment more than once
            if item_name in ['Iron Sword', 'Steel Armor', 'Magic Ring']:
                if item_name in player.owned_equipment:
                    print('You already own this equipment.')
                    continue

            if player.gold >= price:
                player.gold -= price
                player.add_item(item_name)

                if item_name == 'Iron Sword':
                    player.attack += 5
                    player.owned_equipment.add(item_name)
                elif item_name == 'Steel Armor':
                    player.defense += 4
                    player.owned_equipment.add(item_name)
                elif item_name == 'Magic Ring':
                    player.max_hp += 20
                    player.hp = player.max_hp
                    player.owned_equipment.add(item_name)

                print('Purchase successful.')
            else:
                print('Not enough gold.')
        except (ValueError, IndexError):
            print('Invalid selection.')


# ====================== QUESTS ======================

def quest_board(player):
    while True:
        print('\n========== QUEST BOARD ==========')
        for i, quest in enumerate(QUESTS, start=1):
            status = ' (Active)' if quest in player.quests else ''
            print(f'{i}. {quest}{status}')
        print('0. Exit')

        choice = input('Accept quest: ').strip()
        if choice == '0':
            break

        try:
            quest = QUESTS[int(choice) - 1]
            if quest not in player.quests:
                player.quests.append(quest)
                print(f'Accepted quest: {quest}')
            else:
                print('Quest already active.')
        except (ValueError, IndexError):
            print('Invalid quest.')


def show_quests(player):
    print('\n========== ACTIVE QUESTS ==========')
    if not player.quests:
        print('No active quests.')
    else:
        for quest in player.quests:
            print(f'- {quest}')
            if quest == 'Defeat 3 Goblins':
                print(f'  Progress: {player.quest_progress["goblin_kills"]}/3')
            elif quest == 'Survive 10 Battles':
                print(f'  Progress: {player.quest_progress["battles_survived"]}/10')
            elif quest == 'Defeat the Shadow Knight':
                print(f'  Progress: {player.quest_progress["shadow_knight_kills"]}/1')
    print('===================================')


# ====================== MINI GAMES ======================

def dice_game(player):
    print('\nWelcome to Dice Duel!')
    try:
        bet = int(input('Enter gold to bet: '))
        if bet <= 0:
            print('Bet must be positive.')
            return
        if bet > player.gold:
            print('Not enough gold.')
            return

        player_roll = random.randint(1, 6)
        enemy_roll = random.randint(1, 6)
        print(f'You rolled {player_roll}')
        print(f'Enemy rolled {enemy_roll}')

        if player_roll > enemy_roll:
            player.gold += bet
            print(f'You won {bet} gold!')
        elif player_roll < enemy_roll:
            player.gold -= bet
            print(f'You lost {bet} gold!')
        else:
            print('Draw.')
    except ValueError:
        print('Invalid amount.')


def guessing_game(player):
    number = random.randint(1, 20)
    print('\nGuess the Number! (1-20)')
    tries = 5

    while tries > 0:
        try:
            guess = int(input('Your guess: '))
            if guess == number:
                reward = 50
                player.gold += reward
                print(f'Correct! You earned {reward} gold.')
                return
            elif guess < number:
                print('Too low.')
            else:
                print('Too high.')
            tries -= 1
            print(f'Tries left: {tries}')
        except ValueError:
            print('Invalid number.')

    print(f'You lost. The number was {number}.')


# ====================== OTHER FEATURES ======================

def achievements(player):
    print('\n========== ACHIEVEMENTS ==========')
    unlocked = False
    if player.level >= 5:
        print('✔ Experienced Adventurer')
        unlocked = True
    if player.gold >= 500:
        print('✔ Wealth Collector')
        unlocked = True
    if player.kills >= 10:
        print('✔ Monster Hunter')
        unlocked = True
    if player.steps >= 20:
        print('✔ Explorer')
        unlocked = True
    if not unlocked:
        print('No achievements unlocked yet.')


def arena(player):
    if player.hp <= 0:
        print('You are too weak to enter the arena.')
        return

    print('\n========== ARENA ==========')
    print('Fight consecutive enemies for increasing rewards.')
    wins = 0

    while True:
        enemy_data = random.choice(ENEMY_TYPES)
        enemy = Enemy(enemy_data)
        print(f'\nArena Enemy: {enemy.name}')

        while enemy.hp > 0 and player.hp > 0:
            damage = player.attack + random.randint(1, 10)
            enemy.take_damage(damage)
            print(f'You hit {enemy.name} for {damage}')

            if enemy.hp > 0:
                player.take_damage(enemy.attack)

        if player.hp <= 0:
            print('Arena defeat!')
            game_over(player)
            return

        wins += 1
        reward = wins * 25
        player.gold += reward
        player.kills += 1
        player.quest_progress['battles_survived'] += 1
        print(f'Victory! Reward: {reward} gold')

        cont = input('Continue arena? (y/n): ').strip().lower()
        if cont != 'y':
            break

    player.check_quests()


def crafting(player):
    print('\n========== CRAFTING ==========')
    print('1. Craft Mega Potion (Requires 2x Small Potion)')
    print('2. Craft Fire Blade (Requires Iron Sword)')
    print('3. Exit')

    choice = input('Choose: ').strip()

    if choice == '1':
        if player.inventory.count('Small Potion') >= 2:
            player.inventory.remove('Small Potion')
            player.inventory.remove('Small Potion')
            player.add_item('Mega Potion')
            print('Crafted Mega Potion!')
        else:
            print('Need 2 Small Potions.')

    elif choice == '2':
        if 'Iron Sword' in player.inventory:
            player.inventory.remove('Iron Sword')
            player.add_item('Fire Blade')
            player.attack += 10
            # Remove from owned so it can't be re-bought, or keep it
            if 'Iron Sword' in player.owned_equipment:
                player.owned_equipment.discard('Iron Sword')
            print('Crafted Fire Blade! Attack +10')
        else:
            print('Need Iron Sword.')


def boss_fight(player):
    if player.hp <= 0:
        print('You are too weak to challenge the boss.')
        return

    print('\n========== FINAL BOSS ==========')
    boss = Enemy({
        'name': 'Ancient Dragon',
        'hp': 250,
        'attack': 25,
        'gold': 500,
        'xp': 300
    })

    while boss.hp > 0 and player.hp > 0:
        print(f'\nBoss HP: {boss.hp}')
        print(f'Your HP: {player.hp}/{player.max_hp}')
        print('1. Attack')
        print('2. Use Potion')

        choice = input('Choose: ').strip()

        if choice == '1':
            damage = player.attack + random.randint(5, 15)
            boss.take_damage(damage)
            print(f'You dealt {damage} damage!')
        elif choice == '2':
            use_potion(player)
        else:
            print('Invalid choice.')
            continue

        if boss.hp > 0:
            player.take_damage(boss.attack)

    if player.hp <= 0:
        print('The Ancient Dragon defeated you...')
        game_over(player)
    else:
        print('\n*** YOU DEFEATED THE ANCIENT DRAGON! ***')
        player.gold += boss.gold
        player.gain_xp(boss.xp)
        player.kills += 1
        print(f'+{boss.gold} gold')


def game_over(player):
    print('\n========== GAME OVER ==========')
    print(f'{player.name} has fallen.')
    print(f'Level Reached  : {player.level}')
    print(f'Gold Collected : {player.gold}')
    print(f'Enemies Killed : {player.kills}')
    print('================================')
    exit()


# ====================== MAIN MENU ======================

def main_menu(player):
    while True:
        if player.hp <= 0:
            game_over(player)

        print('\n========== MAIN MENU ==========')
        print('1. Explore')
        print('2. Stats')
        print('3. Inventory')
        print('4. Shop')
        print('5. Quest Board')
        print('6. Active Quests')
        print('7. Dice Game')
        print('8. Guessing Game')
        print('9. Achievements')
        print('10. Arena')
        print('11. Crafting')
        print('12. Boss Fight')
        print('13. Save Game')
        print('14. Exit')

        choice = input('Choose option: ').strip()

        if choice == '1':
            explore(player)
        elif choice == '2':
            player.show_stats()
        elif choice == '3':
            player.show_inventory()
        elif choice == '4':
            shop(player)
        elif choice == '5':
            quest_board(player)
        elif choice == '6':
            show_quests(player)
        elif choice == '7':
            dice_game(player)
        elif choice == '8':
            guessing_game(player)
        elif choice == '9':
            achievements(player)
        elif choice == '10':
            arena(player)
        elif choice == '11':
            crafting(player)
        elif choice == '12':
            boss_fight(player)
        elif choice == '13':
            save_game(player)
        elif choice == '14':
            print('Thanks for playing!')
            break
        else:
            print('Invalid option.')


def intro():
    clear_screen()
    print('========================================')
    print('        EPIC TERMINAL WORLD')
    print('========================================')
    print('1. New Game')
    print('2. Load Game')
    print('3. Exit')


def main():
    while True:
        intro()
        choice = input('Choose: ').strip()

        if choice == '1':
            name = input('Enter your hero name: ').strip()
            if not name:
                name = 'Hero'
            player = Player(name)
            main_menu(player)
        elif choice == '2':
            player = load_game()
            if player:
                main_menu(player)
        elif choice == '3':
            print('Goodbye.')
            break
        else:
            print('Invalid option.')


if __name__ == '__main__':
    main()