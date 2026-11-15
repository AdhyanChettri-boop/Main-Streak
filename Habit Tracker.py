import json
from datetime import datetime, timedelta
import os

FILENAME = "habits.json"

def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=2)

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

def calculate_streak(dates):
    if not dates:
        return 0, 0

    dates = sorted(set(dates), reverse=True)
    today = datetime.now().date()
    current_streak = 0
    longest_streak = 0
    temp_streak = 0

    # Current streak
    check_date = today
    for d in dates:
        date_obj = datetime.strptime(d, "%Y-%m-%d").date()
        if date_obj == check_date:
            current_streak += 1
            check_date -= timedelta(days=1)
        elif date_obj < check_date:
            break

    # Longest streak
    dates_sorted = sorted([datetime.strptime(d, "%Y-%m-%d").date() for d in dates])
    for i, date in enumerate(dates_sorted):
        if i == 0:
            temp_streak = 1
        else:
            if (date - dates_sorted[i-1]).days == 1:
                temp_streak += 1
            else:
                longest_streak = max(longest_streak, temp_streak)
                temp_streak = 1
    longest_streak = max(longest_streak, temp_streak)

    return current_streak, longest_streak

def main():
    data = load_data()

    while True:
        print("\n===== Habit Tracker =====")
        print("1. Add new habit")
        print("2. Mark habit as done today")
        print("3. View all habits & streaks")
        print("4. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            name = input("Habit name: ").strip()
            if name and name not in data:
                data[name] = []
                save_data(data)
                print(f"Habit '{name}' added!")
            else:
                print("Invalid or already exists.")

        elif choice == "2":
            if not data:
                print("No habits yet.")
                continue
            print("\nYour habits:")
            for i, habit in enumerate(data.keys(), 1):
                print(f"{i}. {habit}")
            try:
                idx = int(input("Select habit number: ")) - 1
                habit = list(data.keys())[idx]
                today = get_today()
                if today not in data[habit]:
                    data[habit].append(today)
                    save_data(data)
                    print(f"Marked '{habit}' as done today!")
                else:
                    print("Already marked today.")
            except:
                print("Invalid choice.")

        elif choice == "3":
            if not data:
                print("No habits yet.")
                continue
            print("\n===== Your Habits =====")
            for habit, dates in data.items():
                current, longest = calculate_streak(dates)
                print(f"\n{habit}")
                print(f"  Current Streak : {current} days")
                print(f"  Longest Streak : {longest} days")
                print(f"  Total Days     : {len(dates)}")

        elif choice == "4":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
