import csv
from collections import defaultdict

# Read all user_actions from all CSV files in the "exports" directory
def load_all_user_actions():
    all_user_actions = defaultdict(lambda: {a: 0 for a in qr_to_action.values()})
    try:
        for filename in os.listdir("exports"):
            if filename.endswith(".csv"):
                with open(os.path.join("exports", filename), newline="") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        user = row["User"]
                        for action in qr_to_action.values():
                            count = int(row.get(action, 0))
                            all_user_actions[user][action] += count
        return dict(all_user_actions)
    except Exception as e:
        print(f"Error loading user actions: {e}")
        return {}
