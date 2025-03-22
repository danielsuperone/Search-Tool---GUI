import os
import sys
import tkinter as tk
from tkinter import messagebox


def get_data_file_path():
    """Get the file path for the data file, extracting it to a temporary location if needed."""
    if getattr(sys, 'frozen', False):
        # for running as a packaged executable
        data_file_path = os.path.join(sys._MEIPASS, 'example.txt') # set this to the name of the file where the data is stored
    else:
        # If running as a script (during development)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(script_dir, 'example.txt')

    return data_file_path


def parse_data(data):
    """Parse the data and display the results."""
    results_text.delete("1.0", tk.END)  # clears previous results
    results_text.insert(tk.END, f"{'Phone':<20}{'Name':<25}{'Location':<20}{'Occupation':<20}\n")
    results_text.insert(tk.END, "-" * 85 + "\n")

    found = False
    for line in data.splitlines():
        parts = line.strip().split(":")

        if len(parts) > 8:  # make sure enough data is parsed
            phone = parts[0]
            first_name = parts[2]
            last_name = parts[3]
            name = f"{first_name} {last_name}"
            location = parts[5] or "N/A"
            occupation = parts[8] or "N/A"

            # shows country code correctly with the + sign
            formatted_phone = f"+{phone.strip()}"

            # search for appropriate data
            if (search_query.lower() in phone.lower() or 
                search_query.lower() in name.lower() or 
                search_query.lower() in location.lower() or 
                search_query.lower() in occupation.lower() or
                search_query.lower() in formatted_phone.lower()):
                
                results_text.insert(tk.END, f"{formatted_phone:<20}{name:<25}{location:<20}{occupation:<20}\n")
                found = True

    if not found:
        results_text.insert(tk.END, "No results found.\n")


def load_file():
    """Load the file and parse the data."""
    try:
        file_path = get_data_file_path()

        if not os.path.exists(file_path):
            messagebox.showerror("Error", "data.txt not found.")
            return

        with open(file_path, "r", encoding="utf-8") as file:
            parse_data(file.read())
    except FileNotFoundError:
        messagebox.showerror("Error", "data.txt not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")


def search_data():
    """Search for the entered query."""
    global search_query
    search_query = search_entry.get().strip()
    load_file()


def center_window(window):
    """Center the window on the screen."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 800
    window_height = 600
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    window.resizable(False, False)


# GUI
window = tk.Tk()
window.title("OSINT - MLT")
center_window(window)

# Search Bar
search_frame = tk.Frame(window)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Search:")
search_label.pack(side="left", padx=5)

search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side="left", padx=5)

search_button = tk.Button(search_frame, text="Search", command=search_data)
search_button.pack(side="left", padx=5)

# Results Box with Scrollbar
results_frame = tk.Frame(window)
results_frame.pack(fill="both", expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(results_frame)
scrollbar.pack(side="right", fill="y")

results_text = tk.Text(results_frame, wrap="none", yscrollcommand=scrollbar.set, font=("Courier", 10))
results_text.pack(fill="both", expand=True)
scrollbar.config(command=results_text.yview)

# Default Search, this is so it won't automatically display all results as it will cause lag on lower-end systems so we pre-define example search query
search_query = "Name"
load_file()

# Run the application
window.mainloop()
