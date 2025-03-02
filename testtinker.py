import tkinter as tk

# Create a root window
root = tk.Tk()

# Set window title
root.title("Tkinter Test Window")

# Set window size
root.geometry("300x200")

# Create a simple label inside the window
label = tk.Label(root, text="Tkinter is working!", font=("Arial", 14))
label.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
