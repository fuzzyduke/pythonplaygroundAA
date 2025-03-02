def check_even_odd(number):
    """Check if a number is even or odd."""
    if number % 2 == 0:
        return f"{number} is even."
    else:
        return f"{number} is odd."


def print_numbers(limit):
    """Print numbers from 1 to the given limit using a for loop."""
    print("\nNumbers from 1 to", limit, ":")
    for i in range(1, limit + 1):
        print(i)


def start_program():
    """Main function to execute the script."""
    print("Welcome to the Python Practice Program!\n")

    # Get user input
    num = int(input("Enter a number to check if it's even or odd: "))
    print(check_even_odd(num))  # Check even or odd

    # Get limit for printing numbers
    limit = int(input("\nEnter a number to print all numbers from 1 to that number: "))
    print_numbers(limit)  # Print numbers using a loop

    print("\nThanks for using this program! Goodbye!")


# Run the program
if __name__ == "__main__":
    start_program()
