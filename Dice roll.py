import random

def roll_dice():
    print("Dice Roller")
    print("Available dice: D4, D6, D8, D10, D12, D20")
    
    while True:
        choice = input("\nEnter dice type (or 'quit'): ").upper()
        
        if choice == "QUIT":
            break
            
        dice = {
            "D4": 4, "D6": 6, "D8": 8,
            "D10": 10, "D12": 12, "D20": 20
        }
        
        if choice in dice:
            result = random.randint(1, dice[choice])
            print(f"You rolled a {choice}: {result}")
        else:
            print("Invalid dice type!")

roll_dice()
