# pozitii, diverse
import numpy as np
import csv
import matplotlib.pyplot as plt
import multiprocessing as mp
from scipy import signal
from scipy.stats import wasserstein_distance
import pandas as pd

LOG_FILE=open("stats.log", "w") # For console you can set it to None
GENERATE_HISTOGRAMS=True
CALCULATE_CONVOLUTION=True
COMPUTE_WASSERSTEIN=True
USE_PARQUET = False # If you want to export to Parquet
PARQUET_FILE1 = 'en.parquet'
PARQUET_FILE2 = 'en_2025.parquet'

if USE_PARQUET:
    medii = []
    df1 = pd.read_parquet(PARQUET_FILE1)
    df2 = pd.read_parquet(PARQUET_FILE2)
    for _, row in df1.iterrows():
        medii.append(row)
    for _, row in df2.iterrows():
        medii.append(row)

else:
    with open("medii_finale_cont.csv", "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        medii = [float(row[0]) for row in reader if row[0]]

    with open("medii_finale_2025.csv", "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        medii_2025 = [float(row[0]) for row in reader if row[0]][0:3000] # Limit to first 3000 for comparison

print("Comparing 2026 and 2025 grades:", file=LOG_FILE)
print("\n--- 2025 Grades --- ", file=LOG_FILE)

print(f"Count: {len(medii_2025)}", file=LOG_FILE)
print(f"Mean: {np.mean(medii_2025):.2f}", file=LOG_FILE)
print(f"Median: {np.median(medii_2025):.2f}", file=LOG_FILE)
print(f"Std Dev: {np.std(medii_2025):.2f}", file=LOG_FILE)
print(f"Position of 8.82: {medii_2025.index(8.82) if 8.82 in medii_2025 else 'Not found'}", file=LOG_FILE)
print(f"Pozitia 9.05: {medii_2025.index(9.05) if 9.05 in medii_2025 else 'Not found'}", file=LOG_FILE)

print("\n--- 2026 Grades --- ", file=LOG_FILE)
print(f"Count: {len(medii)}", file=LOG_FILE)
print(f"Mean: {np.mean(medii):.2f}", file=LOG_FILE)
print(f"Median: {np.median(medii):.2f}", file=LOG_FILE)
print(f"Std Dev: {np.std(medii):.2f}", file=LOG_FILE)
print(f"Position of 8.82: {medii.index(8.82) if 8.82 in medii else 'Not found'}", file=LOG_FILE)
print(f"Nota pt 1055: {medii_2025[1055]}", file=LOG_FILE)

print("\n", file=LOG_FILE)
print(f"Grades in interval [8.6, 9.3]: {len([x for x in medii if 8.6 <= x < 9.3])} (2026), {len([x for x in medii_2025 if 8.6 <= x < 9.3])} (2025)", file=LOG_FILE)
print(f"Grades in interval [8.2, 8.82]: {len([x for x in medii if 8.2 <= x < 8.82])} (2026), {len([x for x in medii_2025 if 8.2 <= x < 8.82])} (2025)", file=LOG_FILE)

def calculate_diff():
    # Calculate mean of 75 percentile of 2025 grades
    percentile_75_2025 = np.percentile(medii_2025, 75).mean()
    percentile_75_2026 = np.percentile(medii, 75).mean()

    threshold_2025 = np.percentile(medii_2025, 90)
    threshold_2026 = np.percentile(medii, 90)

    group2_2025 = [x for x in medii_2025 if 9.30 <= x < threshold_2025]
    group2_2026 = [x for x in medii if 9.30 <= x < threshold_2026]

    print(f"Estimated change: [{np.mean(medii) - np.mean(medii_2025)}, {np.max(medii) - np.max(medii_2025)}]", file=LOG_FILE)
    print(f"Estimated change via second method: [{np.median(medii) - np.median(medii_2025)}, {percentile_75_2026 - percentile_75_2025}]", file=LOG_FILE)

    print(f"Change of mean in group2: {np.mean(group2_2026) - np.mean(group2_2025)}", file=LOG_FILE)

def calculate_freq():
    values, counts = np.unique(np.round(medii, 1), return_counts=True)
    values_2025, counts_2025 = np.unique(np.round(medii_2025, 1), return_counts=True)

    most_frequent_2025 = values_2025[np.argmax(counts_2025)]
    most_frequent = values[np.argmax(counts)]
    print(f"Most frequent grade in 2025: {most_frequent_2025}, in 2026: {most_frequent}", file=LOG_FILE)

calculate_diff()
calculate_freq()

if CALCULATE_CONVOLUTION:
    print(f"Generated convolution array: ", signal.fftconvolve(medii, medii_2025, "valid"), file=LOG_FILE)

if COMPUTE_WASSERSTEIN:
    distance = wasserstein_distance(medii_2025, medii)
    print(f"Wasserstein distance: ", distance, file=LOG_FILE)

def histogram(year=2025) -> str | None:
    if year not in [2025, 2026]:
        return "Invalid year. Please choose 2025 or 2026."
    
    if year == 2025:
        data = medii_2025
    else:
        data = medii

    try:
        plt.figure(figsize=(8, 5))
        plt.hist(data, bins=50, alpha=0.5, label=str(year), color='orange')
        plt.xlabel('Grades')
        plt.ylabel('Frequency')
        plt.title(f'Histogram of {year} Grades')
        plt.legend()
        plt.savefig(f'histogram_{year}.png')
        plt.close()

        return None

    except Exception as e:
        return f"Error generating histogram for {year}: {e}"

if __name__ == "__main__":
    if GENERATE_HISTOGRAMS:
        print("Creating histograms...")
        with mp.Pool() as pool:
            results = pool.map(histogram, [2025, 2026])

        errors = [r for r in results if r is not None]
        if errors:
            print("Errors occurred during histogram generation:", file=LOG_FILE)
            for err in errors:
                print(err, file=LOG_FILE)

    if LOG_FILE is not None:
        LOG_FILE.close()