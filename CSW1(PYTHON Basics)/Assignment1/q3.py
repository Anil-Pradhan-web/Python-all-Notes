# Step 1: Take month name from user
month = input("Enter the name of a month: ").capitalize()
# Step 2: Dictionary mapping months to days (default days, Feb handled separately)
month_days = {
    "January": 31,
    "February": 28,   # will update if leap year
    "March": 31,
    "April": 30,
    "May": 31,
    "June": 30,
    "July": 31,
    "August": 31,
    "September": 30,
    "October": 31,
    "November": 30,
    "December": 31
}
# Step 3: Check if month is valid
if month not in month_days:
    print("Error: Invalid month name! Please enter a valid month.")
else:
    # Step 4: Handle February separately for leap year check
    if month == "February":
        year = int(input("Enter a year: "))
        # Leap year condition
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            days = 29
        else:
            days = 28

        print(f"{month} {year} has {days} days")

    else:
        # For other months, just display days
        print(f"{month} has {month_days[month]} days")
