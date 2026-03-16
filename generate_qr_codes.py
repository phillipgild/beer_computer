# Make leaderboard sort based on number of total actions
# QR to barcodes
# post-proccessing actions to pris, GUI med instat antal øl,cider etc. der er solgt(forsvundet) og divider indkøbs pris ud på alle genstande
# Try to add daily count(actions)

import qrcode
import csv
import os
import sys

# Folder to save QR codes
output_dir = "qr_codes"
os.makedirs(output_dir, exist_ok=True)

# Mappings
qr_keys_seen = set('HA001')  # Start with hardcoded action QR key to prevent duplicates
names_seen = set('reset')  # Start with hardcoded action name to prevent duplicates

# --- Read Users CSV ---
users = {}
with open("users.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:

        qr_key = row["key"].strip()
        user_name = row["user"].strip()

        # Check for duplicate QR keys
        if qr_key in qr_keys_seen:
            print(f"Duplicate QR key found: {qr_key}")
            sys.exit(1)
        qr_keys_seen.add(qr_key)

        # Check for duplicate user names
        if user_name in names_seen:
            print(f"Duplicate user name found: {user_name}")
            sys.exit(1)
        names_seen.add(user_name)

        users[row["key"]] = row["user"]

# --- Read Actions CSV ---
actions = {}
with open("actions.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:

        qr_key = row["key"].strip()
        action_name = row["action"].strip()

        # Check for duplicate QR keys
        if qr_key in qr_keys_seen:
            print(f"Duplicate QR key found: {qr_key}")
            sys.exit(1)
        qr_keys_seen.add(qr_key)

        # Check for duplicate action names
        if action_name in names_seen:
            print(f"Duplicate action name found: {action_name}")
            sys.exit(1)
        names_seen.add(action_name)

        actions[row["key"]] = row["action"]

# --- Hardcoded Actions CSV ---
hardcoded_actions = {
    'HA001': 'reset',
}

# Function to generate a QR code image
def generate_qr(code, label):
    img = qrcode.make(code)
    filename = os.path.join(output_dir, f"{label}_{code}.png")
    img.save(filename)
    print(f"Saved QR code for {label} -> {filename}")

# Generate QR codes for users
for qr_key, name in users.items():
    generate_qr(qr_key, f"user_{name}")

# Generate QR codes for actions
for qr_key, name in actions.items():
    generate_qr(qr_key, f"action_{name}")

# Generate QR codes for hardcoded actions
for qr_key, name in hardcoded_actions.items():
    generate_qr(qr_key, f"action_{name}")

# Optional: mapping CSV (just for reference)
with open(os.path.join(output_dir, "qr_mapping.csv"), "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["QR_Code", "Type", "Name"])
    for qr_key, name in users.items():
        writer.writerow([qr_key, "User", name])
    for qr_key, name in actions.items():
        writer.writerow([qr_key, "Action", name])
    for qr_key, name in hardcoded_actions.items():
        writer.writerow([qr_key, "Action", name])

print(f"All QR codes and mapping CSV saved in '{output_dir}' folder.")