import tkinter as tk
from tkinter import ttk, font
import csv
import os
import copy

# Folder to save CSV files to
output_dir = "exports"

# --- Load Users from CSV ---
qr_to_user = {}
with open("users_and_items/users.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = row["keys"].strip()
        name = row["user"].strip()
        if key in qr_to_user or name in qr_to_user.values():
            raise ValueError(f"Duplicate user or key: {name} / {key}")
        qr_to_user[key] = name

# --- Load Items from CSV ---
qr_to_item = {}
with open("users_and_items/items.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = row["keys"].strip()
        item = row["items"].strip()
        if key in qr_to_item or item in qr_to_item.values():
            raise ValueError(f"Duplicate item or key: {item} / {key}")
        qr_to_item[key] = item

# --- Load Hardcoded Actions from CSV ---
hardcoded_actions = {}
with open("users_and_items/no_touch/hardcoded_actions.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = row["keys"].strip()
        action = row["action"].strip()
        if key in hardcoded_actions or action in hardcoded_actions.values():
            raise ValueError(f"Duplicate action or key: {action} / {key}")
        hardcoded_actions[key] = action

# --- Read existing user actions from CSV if it exists ---
previous_user_actions = {}
if os.path.exists(output_dir):
    for filename in os.listdir(output_dir):
        if filename.startswith("user_actions") and filename.endswith(".csv"):
            # Read conent of csv file and built a dict of user actions
            with open(os.path.join(output_dir, filename), newline="", encoding="utf-8-sig") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    user = row["User"]
                    if user not in previous_user_actions:
                        previous_user_actions[user] = {a: 0 for a in qr_to_item.values()}
                    for action in qr_to_item.values():
                        count = int(row.get(action, 0))
                        previous_user_actions[user][action] += count

# Nested dictionary to track actions per user
user_actions = copy.deepcopy(previous_user_actions) if previous_user_actions else {}

# Track current user waiting for action
current_user = None
action_couter = 0

# --- Functions ---
def handle_scan(event):
    """Handle a scan from the USB scanner. Determine if it's a user, an item, or a hardcoded action, and update the state accordingly."""
    global current_user
    global status_font
    global action_couter
    scanned_text = scan_entry.get().strip()
    scan_entry.delete(0, tk.END)

    if scanned_text in hardcoded_actions:
        if hardcoded_actions[scanned_text] == "reset":
            current_user = None
            status_label.config(text="Du har scannet genstart QR koden. Scan en bruger.", font=status_font)
            return
        if hardcoded_actions[scanned_text] == "export":
            export_csv()
            return

    if scanned_text in qr_to_user:
        current_user = qr_to_user[scanned_text]
        status_label.config(text=f"Brugeren: {current_user} har scannet sit navn. Scan nu en genstand.", font=status_font)
    elif scanned_text in qr_to_item:
        if current_user:
            item = qr_to_item[scanned_text]
            if current_user not in user_actions:
                user_actions[current_user] = {a: 0 for a in qr_to_item.values()}
            user_actions[current_user][item] += 1
            refresh_table()
            status_label.config(text=f"Brugeren: {current_user} har scannet en genstanden: {item}", font=status_font)
            current_user = None
            action_couter += 1
        else:
            status_label.config(text="Scan en bruger før du scanner en genstand!", font=status_font)
    else:
        if current_user:
            status_label.config(text=f"Ukendt QR code! Brugeren {current_user} har scannet en ukendt kode. Scan en genstand nu.", font=status_font)
        else:
            status_label.config(text="Ukendt QR code! Scan et navn nu.", font=status_font)

    if action_couter >= 10:  # Auto export after every 10 actions
        export_csv()
        action_couter = 0

def refresh_table():
    """Refresh the table with the current user actions, sorted by total actions per user."""
    # Clear existing rows
    for row in tree.get_children():
        tree.delete(row)

    # Create a sorted list of users based on total actions
    # user_actions is a dict: {user_name: {action1: count1, action2: count2, ...}}
    sorted_users = sorted(
        user_actions.items(),
        key=lambda x: sum(x[1].values()),  # sum of all actions
        reverse=True                       # largest total first
    )

    # Insert rows in sorted order
    for user, actions in sorted_users:
        counts = [actions[a] for a in qr_to_item.values()]
        total = sum(counts)
        tree.insert("", "end", values=[user] + counts + [total])

def export_csv():
    """Export the user actions to a CSV file, only exporting new entries since the last export if possible."""
    global previous_user_actions
    global output_dir
    os.makedirs(output_dir, exist_ok=True)
    base_filename = os.path.join(output_dir, "user_actions.csv")
    filename = base_filename
    counter = 1

    # Loop to find a free filename
    while os.path.exists(filename):
        name, ext = os.path.splitext(base_filename)
        filename = f"{name}_{counter}{ext}"
        counter += 1
    try:
        if user_actions and previous_user_actions != {}: # Check if there is data to export and if we have a previous state to compare to
            if user_actions == previous_user_actions: # Compare current user_actions with previous_user_actions
                print("No changes since last export. Skipping export.")
            else:
                with open(filename, "w", newline="", encoding="utf-8-sig") as csvfile:
                    writer = csv.writer(csvfile)
                    header = ["User"] + list(qr_to_item.values()) + ["Total"]
                    writer.writerow(header)
                    for user, actions in user_actions.items():
                        counts = [actions[a] for a in qr_to_item.values()]
                        if user in previous_user_actions:
                            prev_counts = [previous_user_actions[user][a] for a in qr_to_item.values()]
                            counts = [curr - prev for curr, prev in zip(counts, prev_counts)]
                        total = sum(counts)
                        row = [user] + counts + [total]
                        if not all(c == 0 for c in counts):  # only write rows with non-zero counts
                            writer.writerow(row)
                print(f"Exported new entries since last export to {filename}")
                previous_user_actions = copy.deepcopy(user_actions)  # update the previous state after export
        elif user_actions: # If we have user actions but no previous state, export all data
            with open(filename, "w", newline="", encoding="utf-8-sig") as csvfile:
                writer = csv.writer(csvfile)
                header = ["User"] + list(qr_to_item.values()) + ["Total"]
                writer.writerow(header)
                for user, actions in user_actions.items():
                    counts = [actions[a] for a in qr_to_item.values()]
                    total = sum(counts)
                    row = [user] + counts + [total]
                    if not all(c == 0 for c in counts):  # only write rows with non-zero counts
                        writer.writerow(row)
            print(f"Data exported to {filename}")
            previous_user_actions = copy.deepcopy(user_actions)  # store the current state for potential future exports
        else:
            print("No data to export.")
    except Exception as e:
        print(f"Error exporting CSV: {e}")

def on_close():
    """Called when the window is closed"""
    export_csv()   # save data automatically
    root.destroy() # close the GUI

# --- GUI ---
root = tk.Tk()
root.title("Øl computeren")
root.geometry("1536x864")

# Define fonts
status_font = font.Font(family="Helvetica", size=20, weight="bold")
table_header_font = font.Font(family="Helvetica", size=18, weight="bold")
table_font = font.Font(family="Helvetica", size=16)

# Hidden entry for USB scanner
scan_entry = tk.Entry(root, font=status_font)
scan_entry.pack()
scan_entry.focus()
scan_entry.bind("<Return>", handle_scan)

# Status label
status_label = tk.Label(root, text="Scan en bruger først, og derefter en genstand.", font=status_font)
status_label.pack(pady=5)

# --- Table ---
columns = ["User"] + list(qr_to_item.values()) + ["Total"]
tree = ttk.Treeview(root, columns=columns, show="headings")

# Style fonts
style = ttk.Style()
style.configure("Treeview", font=table_font)
style.configure("Treeview.Heading", font=table_header_font)

# Set header text and initial column widths
for col in columns:
    tree.heading(col, text=col, anchor="center")
    col_width = table_header_font.measure(col)
    tree.column(col, anchor="center", width=col_width)

# Insert rows
for user, items in user_actions.items():
    row = [user] + [items.get(item, 0) for item in qr_to_item.values()] + [sum(items.values())]
    tree.insert("", "end", values=row)

# --- Resize the 'User' column ---
first_col = "User"
max_width = table_header_font.measure(first_col)

# Check all users for the widest entry in the first column
for user in qr_to_user.items():
    cell_width = table_font.measure(user[1])
    max_width = max(max_width, cell_width)

# Set the width of the first column to accommodate the widest entry
tree.column(first_col, width=max_width)

# Pack the treeview
tree.pack(fill="both", expand=True)

# Export button (optional manual export)
export_button = tk.Button(root, text="Export CSV", command=export_csv)
export_button.pack(pady=5)

# Bind the window close event
root.protocol("WM_DELETE_WINDOW", on_close)

if user_actions:
    refresh_table()  # Refresh the table with any existing data

root.mainloop()