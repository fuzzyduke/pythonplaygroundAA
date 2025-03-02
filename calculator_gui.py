import tkinter as tk

def calculate():
    """Performs the calculation based on user input."""
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operator = operator_var.get()

        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 != 0:
                result = num1 / num2
            else:
                result = "Error! Division by zero."
        else:
            result = "Invalid operator!"

        result_label.config(text=f"Result: {result}")

    except ValueError:
        result_label.config(text="Error! Enter valid numbers.")

# Create the main window
root = tk.Tk()
root.title("Simple Calculator")

# Create input fields
tk.Label(root, text="Enter first number:").grid(row=0, column=0)
entry_num1 = tk.Entry(root)
entry_num1.grid(row=0, column=1)

tk.Label(root, text="Enter second number:").grid(row=1, column=0)
entry_num2 = tk.Entry(root)
entry_num2.grid(row=1, column=1)

# Operator selection
tk.Label(root, text="Select Operator:").grid(row=2, column=0)
operator_var = tk.StringVar(root)
operator_var.set("+")  # Default operator
operators_menu = tk.OptionMenu(root, operator_var, "+", "-", "*", "/")
operators_menu.grid(row=2, column=1)

# Calculate button
calc_button = tk.Button(root, text="Calculate", command=calculate)
calc_button.grid(row=3, columnspan=2)

# Result label
result_label = tk.Label(root, text="Result: ")
result_label.grid(row=4, columnspan=2)

# Run the GUI loop
root.mainloop()
