import pandas as pd
import numpy as np

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

print("Media mediilor: ", np.mean(medii))
print("Abaterea standard: ", np.std(medii))
