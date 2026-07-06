import requests
import csv
import time


def get_top_sellers():
    response = requests.get('https://store.steampowered.com/api/featured/')
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return []
    data = response.json()
    items = data['large_capsules'] + data['featured_win']
    return [item['id'] for item in items]


def get_game_details(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching {app_id}: {response.status_code}")
        return None

    data = response.json()

    if not data[str(app_id)]["success"]:
        print(f"No data for app {app_id}")
        return None

    game_data = data[str(app_id)]["data"]

    # filter out hardware, DLC, and other non-game types
    if game_data.get("type") != "game":
        print(f"  ✗ Skipping {game_data.get('name')} — type: {game_data.get('type')}")
        return None

    name = game_data.get("name", "Unknown")
    price = game_data.get("price_overview", {}).get("final_formatted", "Free")
    release_date = game_data.get("release_date", {}).get("date", "Unknown")

    return {
        "name": name,
        "price": price,
        "release_date": release_date
    }


def save_to_csv(games):
    with open("steam_top_sellers.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "release_date"])
        writer.writeheader()
        writer.writerows(games)
    print(f"Saved {len(games)} games to steam_top_sellers.csv")


def main():
    print("Fetching top sellers...")
    app_ids = get_top_sellers()
    if not app_ids:
        print("No app IDs found.")
        return

    print(f"Found {len(app_ids)} games — fetching details...")
    games = []
    seen = set()

    for app_id in app_ids:
        details = get_game_details(app_id)
        if details:
            if details['name'] not in seen:
                seen.add(details['name'])
                print(f"  ✓ {details['name']} — {details['price']} — {details['release_date']}")
                games.append(details)
            else:
                print(f"  ✗ Skipping duplicate: {details['name']}")
        time.sleep(0.5)

    if games:
        save_to_csv(games)
        print("\nFinal results:")
        for game in games:
            print(f"  {game['name']} | {game['price']} | {game['release_date']}")
    else:
        print("No game data collected.")


main()