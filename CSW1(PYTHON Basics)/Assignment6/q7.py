# Define the Ticket class
class Ticket:
    def __init__(self, movie_name, show_time, seat_number, price):
        self.movie_name = movie_name
        self.show_time = show_time
        self.seat_number = seat_number
        self.price = price

    # Method to display ticket details
    def display_ticket(self):
        print("Movie Name :", self.movie_name)
        print("Show Time  :", self.show_time)
        print("Seat No    :", self.seat_number)
        print("Price      :", self.price)
        print("--------------------------")


# Function to calculate total price
def calculate_total(tickets):
    total = 0
    for ticket in tickets:
        total += ticket.price
    return total


# Main program
tickets = []

n = int(input("Enter number of tickets to book: "))

for i in range(n):
    print(f"\nEnter details for Ticket {i+1}")
    movie = input("Movie name: ")
    time = input("Show time: ")
    seat = input("Seat number: ")
    price = float(input("Ticket price: "))

    ticket = Ticket(movie, time, seat, price)
    tickets.append(ticket)

print("\n🎟 Ticket Details")
for ticket in tickets:
    ticket.display_ticket()

total_amount = calculate_total(tickets)
print("Total Amount to be Paid:", total_amount)
