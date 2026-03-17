import os
import sys
import csv
import treepoem
from PIL import Image, ImageDraw, ImageFont


# Folder to save barcode images
output_dir = "barcodes"
os.makedirs(output_dir, exist_ok=True)

# Mappings
barcode_keys_seen = set()
names_seen = set()

# --- Read Users CSV ---
users = {}
with open("users.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = row["key"].strip()
        name = row["user"].strip()
        if key in barcode_keys_seen or name in names_seen:
            print(f"Duplicate user or key found: {name} / {key}")
            sys.exit(1)
        barcode_keys_seen.add(key)
        names_seen.add(name)
        users[key] = name

# --- Read Items CSV ---
items = {}
with open("items.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = row["key"].strip()
        item = row["item"].strip()
        if key in barcode_keys_seen or item in names_seen:
            print(f"Duplicate item or key found: {item} / {key}")
            sys.exit(1)
        barcode_keys_seen.add(key)
        names_seen.add(item)
        items[key] = item

# --- Read Hardcoded Actions CSV ---
hardcoded_actions = {}
with open("no_touch/hardcoded_actions.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = row["key"].strip()
        action = row["action"].strip()
        if key in barcode_keys_seen or action in names_seen:
            print(f"Duplicate action or key found: {action} / {key}")
            sys.exit(1)
        barcode_keys_seen.add(key)
        names_seen.add(action)
        hardcoded_actions[key] = action

# --- Function to generate a barcode ---
def generate_barcode(code, name, filename):

    barcode_img = treepoem.generate_barcode(
        barcode_type="code128",
        data=code
    ).convert("RGB")

    barcode_width, barcode_height = barcode_img.size

    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        40
    )

    # Measure text
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), name, font=font)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Determine final image width
    final_width = max(barcode_width, text_width) + 20
    final_height = barcode_height + text_height + 20

    img = Image.new("RGB", (final_width, final_height), "white")
    draw = ImageDraw.Draw(img)

    # Center barcode
    barcode_x = (final_width - barcode_width) // 2
    img.paste(barcode_img, (barcode_x, 0))

    # Center text
    text_x = (final_width - text_width) // 2
    text_y = barcode_height + 10

    draw.text((text_x, text_y), name, fill="black", font=font)

    img.save(filename)

# Generate barcodes for users
for key, name in users.items():
    generate_barcode(key, name, f"barcodes/user_{name}.png")

# Generate barcodes for items
for key, name in items.items():
    generate_barcode(key, name, f"barcodes/item_{name}.png")

# Generate barcodes for hardcoded actions
for key, name in hardcoded_actions.items():
    generate_barcode(key, name, f"barcodes/hardcoded_action_{name}.png")

print(f"All barcodes saved in '{output_dir}' folder.")
