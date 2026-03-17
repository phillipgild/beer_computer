# Make leaderboard sort based on number of total actions
# QR to barcodes
# post-proccessing actions to pris, GUI med instat antal øl,cider etc. der er solgt(forsvundet) og divider indkøbs pris ud på alle genstande
# Try to add daily count(actions)

import qrcode
import csv
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Folder to save QR codes
output_dir = "qr_codes"
os.makedirs(output_dir, exist_ok=True)

# Mappings
qr_keys_seen = set()
names_seen = set()

# --- Read Users CSV ---
users = {}
with open("users.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = row["key"].strip()
        name = row["user"].strip()
        if key in qr_keys_seen or name in names_seen:
            print(f"Duplicate user or key found: {name} / {key}")
            sys.exit(1)
        qr_keys_seen.add(key)
        names_seen.add(name)
        users[key] = name

# --- Read Items CSV ---
items = {}
with open("items.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = row["key"].strip()
        item = row["item"].strip()
        if key in qr_keys_seen or item in names_seen:
            print(f"Duplicate item or key found: {item} / {key}")
            sys.exit(1)
        qr_keys_seen.add(key)
        names_seen.add(item)
        items[key] = item

# --- Read Hardcoded Actions CSV ---
hardcoded_actions = {}
with open("no_touch/hardcoded_actions.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = row["key"].strip()
        action = row["action"].strip()
        if key in qr_keys_seen or action in names_seen:
            print(f"Duplicate action or key found: {action} / {key}")
            sys.exit(1)
        qr_keys_seen.add(key)
        names_seen.add(action)
        hardcoded_actions[key] = action

# Function to generate a QR code image
def generate_qr(code, label):
    # --- Create QR code ---
    qr_img = qrcode.make(code).convert("RGB")
    qr_width, qr_height = qr_img.size

    # --- Choose font ---
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_size = 40  # adjust for larger text
    font = ImageFont.truetype(font_path, font_size)

    # --- Measure text size ---
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), label, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # --- Determine final image size ---
    final_width = max(qr_width, text_width) + 20  # add padding
    final_height = qr_height + text_height + 20

    img = Image.new("RGB", (final_width, final_height), "white")
    draw = ImageDraw.Draw(img)

    # --- Paste QR code centered ---
    qr_x = (final_width - qr_width) // 2
    img.paste(qr_img, (qr_x, 0))

    # --- Draw label centered below ---
    text_x = (final_width - text_width) // 2
    text_y = qr_height + 10
    draw.text((text_x, text_y), label, fill="black", font=font)

    # --- Save PNG ---
    filename = os.path.join(output_dir, f"{label}_{code}.png")
    img.save(filename)
    print(f"Saved QR code for {label} -> {filename}")

# Generate QR codes for users
for qr_key, name in users.items():
    generate_qr(qr_key, name)

# Generate QR codes for items
for qr_key, name in items.items():
    generate_qr(qr_key, name)

# Generate QR codes for hardcoded actions
for qr_key, name in hardcoded_actions.items():
    generate_qr(qr_key, name)

# Optional: mapping CSV (just for reference)
with open(os.path.join(output_dir, "qr_mapping.csv"), "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["QR_Code", "Type", "Name"])
    for qr_key, name in users.items():
        writer.writerow([qr_key, "User", name])
    for qr_key, name in items.items():
        writer.writerow([qr_key, "Item", name])
    for qr_key, name in hardcoded_actions.items():
        writer.writerow([qr_key, "Action", name])

print(f"All QR codes and mapping CSV saved in '{output_dir}' folder.")