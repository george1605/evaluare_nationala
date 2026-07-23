import pandas as pd
import numpy as np
from scipy.stats import t, norm

df = pd.read_csv('ac.csv')
print(df.head())

medii = []
mate = 0 # nr pers care au dat admitere la mate 
info = 0 # nr pers care au dat admitere la info
for _, row in df.iterrows():
    medii.append(row[11])
    if row[-1] == 'matematica':
        mate = mate + 1
    else:
        info = info + 1

print("Au dat admitere la mate: ", mate)
print("Au dat admitere la info: ", info)

sigma = np.std(medii)

print("Media mediilor: ", np.mean(medii))
print("Abaterea standard: ", sigma)

freqs, bin_edges = np.histogram(medii, bins=np.linspace(2, 10, num=20))
frecv_nota = bin_edges[np.argmax(freqs).min()]
print("Cea mai frecventa nota: ", frecv_nota)

# Asumand o distributie normala cautam notele din intervalul [m - sigma, m + sigma]
n1 = frecv_nota - sigma
n2 = frecv_nota + sigma
print("Frecventele medie +/- sigma din cadrul unei dist std: ", freqs[bin_edges.searchsorted(n1)], freqs[bin_edges.searchsorted(n2)])

df, loc, scale = t.fit(medii)
print("Fitare la o distributie Student(T): ", df, loc, scale)