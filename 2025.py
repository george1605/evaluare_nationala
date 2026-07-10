import csv
import requests

URL = "https://static.evaluare.edu.ro/2025/rezultate/IS/data/candidate.json"

data = requests.get(URL, timeout=10).json()
medii = [candidate["mev"] for candidate in data]

print(f"Collected {len(medii)} grades.")

with open("medii_finale_2025.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["medie_finala"])
    writer.writerows([[m] for m in medii])

print("Saved to medii_finale_2025.csv")