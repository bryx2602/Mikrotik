import customtkinter

# Create the main window
root = customtkinter.CTk()

# Set the default color theme
customtkinter.set_default_color_theme("dark-blue")

# Create a button with custom background and foreground colors
button = customtkinter.CTkButton(root, text="Click Me", fg_color=("white", "black"), bg_color=("blue", "darkblue"))
button.pack(pady=20, padx=20)

# Run the application
root.mainloop()