import csv
import os
from collections import defaultdict

# Folder to save CSV files to
output_dir = "prices"

# --- Load Items from CSV ---
qr_to_item = {}
item_prices = {}
item_amounts = {}
with open("users_and_items/items.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = row["keys"].strip()
        item = row["items"].strip()
        price = float(row["price"].strip())
        amount = int(row["amount"].strip())
        if key in qr_to_item or item in qr_to_item.values() or price in item_prices.values() or amount in item_amounts.values():
            raise ValueError(f"Duplicate key or price or amount or item: {key} / {price} / {amount} / {item}")
        qr_to_item[key] = item
        item_prices[item] = price
        item_amounts[item] = amount

# Read all user_actions from all CSV files in the "exports" directory
def load_all_user_actions():
    all_user_actions = defaultdict(lambda: {a: 0 for a in qr_to_item.values()})
    try:
        for filename in os.listdir("exports"):
            if filename.endswith(".csv"):
                with open(os.path.join("exports", filename), newline="", encoding="utf-8-sig") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        user = row["User"]
                        for action in qr_to_item.values():
                            count = int(row.get(action, 0))
                            all_user_actions[user][action] += count
        return dict(all_user_actions)
    except Exception as e:
        print(f"Error loading user actions: {e}")
        return {}

all_user_actions = load_all_user_actions()

# For each user, calculate the total cost based on their actions and the item prices
def calculate_user_costs(user_actions, item_prices, item_amounts):
    user_costs = {}
    for user, actions in user_actions.items():
        total_cost = 0
        for item, count in actions.items():
            price = item_prices.get(item, 0)
            total_cost += price * count
        user_costs[user] = total_cost
    return user_costs

user_costs = calculate_user_costs(all_user_actions, item_prices, item_amounts)

# Find the difference between the amounts in item_amounts and the total counts in all_user_actions to find the remaining stock
def calculate_missing_items(all_user_actions, item_amounts):
    missing_items = {}
    for item, amount in item_amounts.items():
        total_count = sum(actions.get(item, 0) for actions in all_user_actions.values())
        missing_items[item] = amount - total_count
    return missing_items

missing_items = calculate_missing_items(all_user_actions, item_amounts)

# Find the total cost of the missing items and divide this amount evenly across the users
def calculate_cost_per_user(missing_items, user_costs):
    total_missing_cost = sum(item_prices[item] * count for item, count in missing_items.items())
    num_users = len(user_costs)
    if num_users == 0:
        return {}
    cost_per_user = total_missing_cost / num_users
    return {user: cost_per_user for user in user_costs}

# Add the cost per user for the missing items to the existing user costs to get the final cost per user
def calculate_final_user_costs(user_costs, cost_per_user):
    final_user_costs = {}
    for user in user_costs:
        final_user_costs[user] = user_costs[user] + cost_per_user.get(user, 0)
    return final_user_costs

cost_per_user = calculate_cost_per_user(missing_items, user_costs)
final_user_costs = calculate_final_user_costs(user_costs, cost_per_user)

# Export the user costs to a new CSV file
def export_user_costs(user_costs, filename="user_costs.csv"):
    global output_dir
    os.makedirs(output_dir, exist_ok=True)
    try:
        with open(os.path.join(output_dir, filename), "w", newline="", encoding="utf-8-sig") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Total Cost"])
            for user, cost in user_costs.items():
                writer.writerow([user, cost])
        print(f"Exported user costs to {os.path.join(output_dir, filename)}")
    except Exception as e:
        print(f"Error exporting user costs: {e}")

export_user_costs(final_user_costs)
