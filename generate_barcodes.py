import os
import sys
import csv
import treepoem

# Folder to save barcode images
output_dir = "barcodes"
os.makedirs(output_dir, exist_ok=True)

# Mappings
barcode_keys_seen = set('HA001')  # Start with hardcoded action QR key to prevent duplicates
names_seen = set('reset')  # Start with hardcoded action name to prevent duplicates

# --- Read Users CSV ---
users = {}
with open("users.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:

        barcode_key = row["key"].strip()
        user_name = row["user"].strip()

        # Check for duplicate QR keys
        if barcode_key in barcode_keys_seen:
            print(f"Duplicate barcode key found: {barcode_key}")
            sys.exit(1)
        barcode_keys_seen.add(barcode_key)

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

        barcode_key = row["key"].strip()
        action_name = row["action"].strip()

        # Check for duplicate barcode keys
        if barcode_key in barcode_keys_seen:
            print(f"Duplicate barcode key found: {barcode_key}")
            sys.exit(1)
        barcode_keys_seen.add(barcode_key)

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

# --- Function to generate a barcode ---
def generate_barcode(code, label):
    # Generate a Code128 barcode
    img = treepoem.generate_barcode(
        barcode_type='code128',  # 1D Code128 barcode
        data=code
    )
    # Convert to 1-bit black & white and save as PNG
    filename = os.path.join(output_dir, f"{label}_{code}.png")
    img.convert("1").save(filename)
    print(f"Saved barcode: {filename}")

# Generate barcodes for users
for qr_key, name in users.items():
    generate_barcode(qr_key, f"user_{name}")

# Generate barcodes for actions
for qr_key, name in actions.items():
    generate_barcode(qr_key, f"action_{name}")

print(f"All barcodes saved in '{output_dir}' folder.")
