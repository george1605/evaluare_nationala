import csv
import time

import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://evaluare.edu.ro/Evaluare/CandFromJudIAD.aspx"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    )
}

EXPORT_PARQUET = True # If you want to export to Parquet
PARQUET_FILE = 'en.parquet'
all_medii = []

for page in range(1, 151):
    print(f"Page {page}")

    params = {
        "Jud": 26,
        "Poz": 0,
        "PageN": page
    }

    try:
        r = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        container = soup.find(id="ContentPlaceHolderBody_FinalDiv")
        if container is None:
            print("  FinalDiv not found.")
            continue

        table = container.find("table")
        if table is None:
            print("  Table not found.")
            continue

        rows = table.find_all("tr")[2:]
        page_count = 0

        for row in rows:
            cols = row.find_all("td")

            if len(cols) >= 15:
                medie = cols[14].get_text(strip=True)
                all_medii.append(medie)
                page_count += 1

        print(f"  Collected {page_count} grades.")

        time.sleep(0.2)

    except Exception as e:
        print(f"  Error: {e}")

print(f"\nTotal grades: {len(all_medii)}")

if EXPORT_PARQUET:
    df = pd.DataFrame.from_dict({ "medii": all_medii })
    df.to_parquet(PARQUET_FILE)
    print(f"Saved to {PARQUET_FILE}")
else:    
    with open("medii_finale_cont.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["medie_finala"])
        writer.writerows([[m] for m in all_medii])

    print("Saved to medii_finale.csv")