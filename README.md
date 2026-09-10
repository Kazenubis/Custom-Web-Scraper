# Steam Top Sellers Scraper

Pulls Steam's current top-seller and featured games via Steam's own public
storefront endpoints and exports name, price, and release date to CSV — no
API key, no HTML scraping.

## Example

```
$ python3 main.py
Fetching top sellers...
Found 32 games — fetching details...
  ✓ Hand of Fate: Hordes — $3.99 USD — 22 Jul, 2026
  ✓ Incrempire — $5.99 — Jul 21, 2026
  ✗ Skipping duplicate: Incrempire
  ✗ Skipping Some DLC Pack — type: dlc
  ✓ Scarlet Deer Inn — $9.89 USD — 21 Jul, 2026
  ...
Saved 24 games to steam_top_sellers.csv
```

`steam_top_sellers.csv`:

```csv
name,price,release_date
Hand of Fate: Hordes,$3.99 USD,"22 Jul, 2026"
Incrempire,$5.99,"Jul 21, 2026"
Scarlet Deer Inn,$9.89 USD,"21 Jul, 2026"
```

## Features

- Pulls the current featured/top-seller list from Steam's `api/featured` endpoint, then fetches full details for each app from `api/appdetails`
- Filters out DLC, hardware, and other non-game listings — only actual games make it into the output
- De-duplicates by name (the featured and top-seller lists overlap)
- Rate-limited with a 0.5s delay between detail requests, one app at a time
- Exports to a clean `name,price,release_date` CSV

## Tech Stack

Python 3 · `requests` · standard library `csv`

## Getting Started

```bash
git clone https://github.com/Kazenubis/Custom-Web-Scraper.git
cd Custom-Web-Scraper
pip install -r requirements.txt
python3 main.py
```

Produces `steam_top_sellers.csv` in the current directory.

## What I Learned

Steam's featured-games endpoint mixes actual games in with DLC and hardware
listings (a Steam Deck, a soundtrack), so filtering on `type != "game"` from
the per-app details endpoint was necessary — the featured list alone doesn't
say what kind of listing each entry is. The other real gotcha: the featured
and top-seller sections returned by `api/featured` overlap, so the same game
can appear twice with two different app IDs' worth of duplicate detail
fetches wasted unless results are de-duplicated by name before writing to
CSV.
