import dotenv as dotenv
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import multiprocessing as mp
from itertools import chain

dotenv.load_dotenv()
BINS=int(dotenv.get_key(dotenv.find_dotenv(), "HISTOGRAM_BINS")) # by default 50
ALPHA=float(dotenv.get_key(dotenv.find_dotenv(), "HISTOGRAM_ALPHA")) # by default 0.5
note = {}

USE_PARQUET=True
PARQUET_FILE='licee.parquet'
if USE_PARQUET:
    df = pd.read_parquet(PARQUET_FILE)
    for col in df.columns:
        note[col] = []
    
    for name, column in df.items():
        note[name] = column[column != -1]

else:
    with open("licee_data.csv", "r", newline="", encoding="utf-8") as f:
        global lista_licee
        reader = csv.reader(f)
        first = True
        for row in reader:
            if first:
                lista_licee = row
                first = False
            else:
                i = 0
                for liceu in lista_licee:
                    if note.get(liceu, None) is None:
                        note[liceu] = [float(row[i])]
                    elif row[i] != '':
                        note[liceu].append(float(row[i]))
                    i = i + 1


def create_plot():
    means = [np.mean(x) for x in note.values()]
    maxims = [np.max(x) for x in note.values()]
    plt.figure(figsize=(12, 12))
    plt.bar(note.keys(), height=maxims, data=maxims, color='blue')
    plt.bar(note.keys(), height=means, data=means, color='red')
    plt.savefig('plot.png')
    plt.close()

def create_hist():
    all_grades = list(chain.from_iterable(note.values()))
    plt.figure(figsize=(8,5))
    plt.hist(all_grades, bins=BINS, alpha=ALPHA, label='Note BAC', color='orange')
    plt.xlabel('Grades')
    plt.ylabel('Frequency')
    plt.title('Histogram of BAC grades 2026')
    plt.legend()
    plt.savefig('bac_hist.png')
    plt.close()

if __name__ == '__main__':
    proc = mp.Process(target=create_plot)
    proc.start()
    proc.join()
    create_hist()
    