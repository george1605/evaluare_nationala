# Evaluare Nationala Calculator

## Statistici simple legate de mediile finale evaluare nationala judetul Iasi

Sunt folosite datele din 2026 si 2025. Datele din 2026 sunt luate folosind `beautifulsoup` iar cele din 2025 de la un API JSON. Datele sunt salvate in csv sau alternativ in Parquet folosind `pandas`. 

Datele de la BAC sunt obtinute printr-un procedeu putin mai complex care implica un request `GET` initial pentru a obtine starea unor variabile cat si numarul paginilor dupa care se fac requesturi `POST` prin care se seteaza variabilele hidden si numarul paginii. Se foloseste tot `beautifulsoup` pentru a obtine datele din tabel si nr de pagini din textul `<option>` ului.

Programul `calcule.py` genereaza histograme pentru ambii ani cat si date spre exemplu media, abaterea medie, diferentele medii de punctaj intre diferite esantioane. 

Programul `bac/calcule.py` genereaza de asemenea o histograma pentru toate datele de pe licee concatenate si flattened dar creaaza si un bar plot

Evolutii viitoare:
 - Statistici pe scoli si licee 
 - Date BAC sau alte examene
 - Simulari alocari locuri in functie de medie si alti factori. 

