import calendar

def show_calendar():
    print("Calendar")
    year = int(input("Enter year: "))
    month = int(input("Enter month (1-12): "))
    
    print("\n" + calendar.month(year, month))

show_calendar()
