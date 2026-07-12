import csv
import requests
import pandas as pd

URL = "https://static.evaluare.edu.ro/2025/rezultate/IS/data/candidate.json"
EXPORT_PARQUET = True # If you want to export to Parquet
PARQUET_FILE = 'en_2025.parquet'

data = requests.get(URL, timeout=10).json()
medii = [candidate["mev"] for candidate in data]

print(f"Collected {len(medii)} grades.")

if EXPORT_PARQUET:
    df = pd.DataFrame.from_dict({ "medii": medii })
    df.to_parquet(PARQUET_FILE)
else:
    with open("medii_finale_2025.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["medie_finala"])
        writer.writerows([[m] for m in medii])

    print("Saved to medii_finale_2025.csv")