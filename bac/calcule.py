import dotenv as dotenv
import csv
import numpy as np
import matplotlib.pyplot as plt

dotenv.load_dotenv()
BINS=int(dotenv.get_key(dotenv.find_dotenv(), "HISTOGRAM_BINS")) # by default 50
ALPHA=float(dotenv.get_key(dotenv.find_dotenv(), "HISTOGRAM_ALPHA")) # by default 0.5
note = {}

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

means = [np.mean(x) for x in note.values()]
maxims = [np.max(x) for x in note.values()]
plt.bar(note.keys(), height=maxims, data=maxims, color='blue')
plt.bar(note.keys(), height=means, data=means, color='red')
plt.show()